# Architecture and specification deep dive

This monorepo targets the MCP `2026-07-28` specification and the official Python SDK v2. It separates reusable server infrastructure from deployable server applications and keeps the SDK responsible for protocol framing and dispatch.

## Protocol architecture

MCP is a JSON-RPC 2.0 protocol with three participants: a **host** (the LLM application), an embedded **client** (the host's MCP integration), and a **server** (capability provider). MCP standardizes access to context and tools; it does not prescribe the model provider or application business logic.

Servers expose three core primitives:

- **Tools** are model-selected operations and may have side effects. Each call needs clear input constraints, authorization, budgets, and retry semantics.
- **Resources** are application-selected context reads. Keep them bounded, deterministic, and read-only where possible.
- **Prompts** are user-selected templates. They should help users invoke a workflow and must not be used as hidden security policy.

The SDK derives tool JSON Schemas from typed function signatures, validates inputs, performs JSON-RPC dispatch, and wraps results. Use the low-level server only when the high-level `MCPServer` cannot express a required wire-level behavior.

## SDK and specification versioning

The current official Python SDK v2 supports MCP `2026-07-28` and compatible legacy peers. Its high-level server class is `MCPServer`; `FastMCP` is the SDK 1.x name. This repo follows the current SDK and pins its major range to `mcp[cli]>=2,<3`. See [SDK v2](https://py.sdk.modelcontextprotocol.io/), [What's new in v2](https://py.sdk.modelcontextprotocol.io/whats-new/), and the [migration guide](https://py.sdk.modelcontextprotocol.io/migration/).

The 2026 revision retires the `initialize`/`initialized` handshake and the Streamable HTTP `Mcp-Session-Id` on the modern path. Requests carry protocol/client metadata and capabilities as appropriate; `server/discover` provides capability discovery. Independent requests can be load-balanced without protocol-session affinity. Stateful applications should use explicit opaque handles, bind them to an authenticated principal, and expire them.

Streamable HTTP uses `Mcp-Method` and `Mcp-Name` headers for request routing and metering. List and read responses include cache guidance. Servers should return stable capability catalogs so clients can safely cache them. The official SDK manages these headers and cache fields; do not handcraft them in tools.

The SDK's safe default cache hint is immediately stale and private. The demo overrides it only for its static, identical-for-every-caller catalogs and resources: one minute for discovery/listings and 30 seconds for resource reads. If a future service filters capabilities or resources by user or tenant, use private scope or no shared caching for those results.

Tool `inputSchema` and `outputSchema` use JSON Schema 2020-12 in the current revision. Keep schemas bounded in depth and validation cost, and avoid untrusted external `$ref` resolution. A missing resource is reported using the standardized invalid-params error. Error text for an expected tool failure should be returned as an `isError` tool result; the high-level SDK's `ToolError` provides that behavior.

## Workspace boundaries

```text
apps/example-server       Deployable service: composition root, features, CLI, ASGI app
        │
        ▼
libs/mcp-starter-core      Shared config, OAuth verifier, lifecycle, transport policy, logs
        │
        ▼
official mcp SDK          Protocol models, validation, dispatch, transports, tracing hooks
```

A new deployable MCP service belongs in `apps/<service>`. Each app has its own project metadata and console script. `libs/mcp-starter-core` contains only infrastructure multiple services can share; it should not gain app-specific resources or tools. The root project manages the workspace lockfile and development tools.

`apps/example-server/src/mcp_example_server/server.py` is the composition root. Capability modules export `register(server)` and do not start a transport. `cli.py` owns process startup, while `http_app.py` is the ASGI boundary. This makes the same server definition reusable for stdio, a direct HTTP listener, or an ASGI host.

## Capability and failure patterns

Python annotations and Pydantic `Field` constraints produce tool input schemas. Validation happens before the handler. In handlers:

- Use `ToolError` when execution failed in a way the model can understand and correct (for example, division by zero).
- Use `MCPError` only when the request itself should fail at the protocol layer and the model should not receive a tool result.
- Use `ResourceNotFoundError` for a URI-template instance that does not exist.
- Let unexpected exceptions reach the SDK sanitizer; do not return tracebacks or raw upstream errors to clients.

Keep handlers thin. Put database queries, remote API calls, policy, and idempotency in application services; pass service handles through `Context`/lifespan as the app grows.

## Authentication architecture

On Streamable HTTP, the MCP service is an OAuth 2.1 **resource server**. The identity provider owns login, consent, client registration, and token issuance. The service validates tokens on every HTTP request. This repo implements a reusable RFC 7662 introspection adapter through the SDK's `TokenVerifier` interface and configures it with `AuthSettings`.

The verifier uses client authentication, bounded timeouts, disables redirects, checks `active`, validates `exp` when present, checks scope shape and client identity, and matches the expected resource/audience. It projects only a small safe claim allowlist and does not log credentials or token bodies. The current adapter does not require `exp` to be present and does not independently compare the `iss` claim to the configured issuer; see [Security and operations](operations/security.md#what-the-current-verifier-validates). The SDK publishes Protected Resource Metadata and applies the auth middleware. `MCP_AUTH_ENABLED` is not a fake token switch: missing verifier settings fail application configuration. Non-loopback binds require OAuth, HTTPS endpoints outside local development, and an explicit public host allowlist.

Stdio does not carry HTTP bearer credentials. Its trust boundary is the OS process and the host that launches it. Do not treat stdio auth settings as protection from a malicious local process.

## Transport and deployment choices

- **stdio** is the default for local hosts that spawn the MCP process. Stdout is reserved for protocol frames, so logs go to stderr.
- **Streamable HTTP** is used for remote services. Keep DNS-rebinding protection on, configure exact hosts and browser origins, and put TLS at the edge. A reverse proxy must sanitize and forward only trusted headers.
- **SSE** is a legacy transport and should not be selected for new services.

The HTTP server caps request bodies at 4 MiB by default (configurable up to 16 MiB). Apply rate and concurrency limits, timeouts, and egress controls at a trusted gateway or service layer. The starter avoids inventing a protocol health route; use the hosting platform's process health/readiness mechanism or a deliberately designed outer ASGI app.

Protocol statelessness does not make application state or downstream dependencies stateless. Use bounded connection pools, timeouts, retry budgets with jitter, circuit breaking where appropriate, and graceful shutdown. Make mutations idempotent and bind records/handles to the authenticated subject. Avoid in-memory state if requests may land on different replicas.

## Observability

The app has an optional `observability` extra containing OpenTelemetry packages, but this repository does not configure a provider/exporter or include a telemetry deployment. The shared logging helper emits structured console or JSON logs to stderr. Keep tool parameters, resources, credentials, and upstream response bodies out of logs and traces. Record operation name, latency, outcome, and approved correlation/principal identifiers only when a deployment explicitly adds telemetry.

## Extensions

Tasks, MCP Apps, and other extensions are independent opt-in capabilities, not automatic consequences of using the latest core spec. Add extension code behind explicit negotiation, keep its data types isolated, and advertise only capabilities the server fully implements. For shared state across replicas, use durable backing services and the extension's documented persistence/bus contract.

## Sources

- [MCP specification](https://modelcontextprotocol.io/specification/2026-07-28)
- [Official Python SDK](https://py.sdk.modelcontextprotocol.io/)
- [Python SDK authorization](https://py.sdk.modelcontextprotocol.io/run/authorization/)
- [Python SDK deployment and scaling](https://py.sdk.modelcontextprotocol.io/run/deploy/)
- [Python SDK tool errors](https://py.sdk.modelcontextprotocol.io/servers/handling-errors/)
