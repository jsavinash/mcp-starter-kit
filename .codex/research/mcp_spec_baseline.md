# MCP specification and SDK baseline

**Reviewed:** 2026-11-07
**Protocol baseline:** MCP `2026-07-28`
**Python SDK baseline:** official SDK v2 (`mcp>=2,<3`)

This note records the spec properties that materially affect this starter. Consult official spec and SDK docs again before changing dependencies or wire behavior; this file is a snapshot, not a replacement for normative text.

## Protocol model

MCP is JSON-RPC-based. A host contains the client integration; the server offers capabilities. Server primitives have distinct intent:

- **Tools** are operations the model may select; treat them as API endpoints with bounded schemas, explicit side effects, authorization, and safe error semantics.
- **Resources** expose addressable context. Keep content bounded and apply caller/tenant access checks where content is private.
- **Prompts** are user-invoked templates. They are not authorization or policy enforcement.

The protocol standardizes context and tool interaction, not the service's business logic, identity provider, deployment topology, or model vendor.

## Changes important to this repository's target revision

- The `2026-07-28` modern protocol path is stateless: it removes the old initialize/initialized handshake and HTTP session identifier. Each request carries protocol/client metadata as defined by the spec; `server/discover` supports capability discovery.
- Multi-round-trip requests provide a portable way for tools to ask for user input or other client-mediated responses without relying on the old server-push interaction model.
- Streamable HTTP adds `Mcp-Method` and `Mcp-Name` routing headers. Gateways can route/meter without parsing the JSON body; SDK and deployment layers must preserve these headers.
- List/read results carry cache guidance (`ttlMs`, `cacheScope`). Cache scope must match authorization and data-sharing boundaries. User-specific or tenant-specific results must not be shared publicly.
- Tasks moved into an extension; do not assume the former experimental core task protocol.
- Extensions, including MCP Apps, are optional and separately negotiated. Do not advertise unsupported capabilities.
- Authorization was hardened, including issuer validation guidance and a move away from DCR toward Client ID Metadata Documents. A server's authorization design must follow the current normative authorization section and IdP behavior; the starter's RFC 7662 adapter is resource-server token verification, not a complete OAuth authorization server.
- The release introduced a formal deprecation policy. Follow official lifecycle notices rather than assuming a date-stamped spec is permanently frozen.

## SDK choices and migration implications

The current official Python SDK documentation identifies v2 as the stable line. Its high-level server is `MCPServer`; `FastMCP` was the SDK v1 class/import. Do not combine v1 names/imports with the v2 dependency range. The v2 line speaks the `2026-07-28` revision and retains compatibility paths for older peers, but old connection behaviors may require explicitly selecting legacy mode.

The repo currently uses the high-level SDK server and lets it own JSON-RPC dispatch, schemas, errors, routing headers, and cache fields. Prefer SDK APIs over hand-crafted wire behavior. Use low-level APIs only where a documented requirement cannot be expressed by `MCPServer`.

## Architectural implications

1. Protocol-level statelessness permits ordinary HTTP load balancing; it does not make application state, tool side effects, or downstream dependencies stateless.
2. If an app keeps workflow state, use explicit opaque handles, authenticate and authorize every retrieval, bind handles to a principal, expire them, and use shared durable storage when traffic can land on any replica.
3. Make mutations idempotent or define retry semantics; clients and gateways may retry independently of a server process.
4. Use SDK-produced cache metadata; scope and TTL are security decisions as well as performance settings.
5. Never use a capability listing, prompt, or resource as an authorization boundary.
6. HTTP transport security and OAuth validation are complementary. Host/origin checks prevent DNS rebinding/browser abuse; OAuth establishes identity/authorization.
7. Stdio uses an OS process boundary, not HTTP bearer authorization.

## Fit to this repository

The app already targets `MCPServer`, has stdio and Streamable HTTP, uses typed example capabilities, sets cache hints for static public data, and keeps Tasks/Apps opt-in. The core implements an introspection verifier and passes it to SDK auth hooks. These align with the high-level target but need tests that assert behavior through SDK clients and HTTP/stdio boundaries.

Do not claim full MCP conformance from architecture documentation alone. Conformance requires testing actual request/response behavior, errors, metadata, transport behavior, and negotiated capabilities against the target SDK/spec.

## Official sources

- [MCP specification, 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28)
- [2026-07-28 release notes](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [Official Python SDK v2 docs](https://py.sdk.modelcontextprotocol.io/v2/)
- [What's new in Python SDK v2](https://py.sdk.modelcontextprotocol.io/whats-new/)
- [Python SDK v1-to-v2 migration guide](https://py.sdk.modelcontextprotocol.io/migration/)
- [Python SDK authorization](https://py.sdk.modelcontextprotocol.io/run/authorization/)
- [Python SDK deployment and scaling](https://py.sdk.modelcontextprotocol.io/run/deploy/)

Research performed 2026-11-07 against the sources above. Recheck source currency before changing this baseline.
