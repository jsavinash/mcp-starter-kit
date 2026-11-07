# Python package reference

This page maps the supported source modules to their responsibilities. It is a navigation reference, not a stable public API promise; package exports and compatibility guarantees should be documented if these packages are published externally.

## `mcp-example-server`

Package source: `apps/example-server/src/mcp_example_server/`.

| Module | Responsibility |
|---|---|
| `cli.main()` | Loads settings, configures logging, creates the server, then runs stdio or Streamable HTTP. |
| `server.create_server(settings=None)` | Composition root; builds auth configuration, SDK cache hints, lifespan, and registers capability modules. |
| `http_app.app` | HTTP-only ASGI app; validates transport on import, configures logging, and creates the SDK ASGI app. |
| `dev.mcp` | Object target used by `mcp dev` and the Inspector. |
| `features.calculator.register(server)` | Registers the side-effect-free calculator tool. |
| `features.catalog.register(server)` | Registers guide resources and the topic explanation prompt. |

Console script: `mcp-example-server`. The app package version is currently `0.1.0`.

## `mcp-starter-core`

Package source: `libs/mcp-starter-core/src/mcp_starter_core/`.

| Module/symbol | Responsibility |
|---|---|
| `config.Settings` | Pydantic settings model, environment parsing, and deployment validation. |
| `config.get_settings()` | Cached settings loader (`lru_cache(maxsize=1)`). |
| `auth.OAuthIntrospectionVerifier` | SDK `TokenVerifier` implementation backed by RFC 7662 HTTP introspection. |
| `lifecycle.server_lifespan` | Structured start/stop logs and verifier HTTP-client lifespan. |
| `logging.configure_logging(level, output)` | Configures structlog output to stderr in console or JSON format. |
| `transport.build_transport_security(settings)` | Builds SDK DNS-rebinding, host, and origin protection settings. |

Core package version is currently `0.1.0`. There are no documented semver guarantees for an independently published package yet.

## External SDK surfaces used

- `mcp.server.MCPServer`, `CacheHint`
- SDK auth `AuthSettings`, `TokenVerifier`, and `AccessToken`
- SDK transport security settings and `ToolError` / `ResourceNotFoundError`

The code targets the SDK v2 major line. Recheck the [official SDK migration guide](https://py.sdk.modelcontextprotocol.io/migration/) before changing these imports or the version constraint.
