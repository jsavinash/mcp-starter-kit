# Example MCP capabilities

The example server registers three capabilities from focused modules under `apps/example-server/src/mcp_example_server/features/`. `server.py` creates the MCP server and registers each module once. The examples are deliberately deterministic and do not call external services or mutate data.

## Tool: `calculate`

Registered by `features/calculator.py`.

| Input | Type | Constraint |
|---|---|---|
| `operation` | string enum | `add`, `subtract`, `multiply`, `divide` |
| `left` | finite number | inclusive range `-1e12` to `1e12` |
| `right` | finite number | inclusive range `-1e12` to `1e12` |

Returns the numeric result. Division by zero raises SDK `ToolError` with a model-readable recovery message. Non-finite results (such as arithmetic overflow) also raise `ToolError`. It is side-effect free.

## Resources

Registered by `features/catalog.py`.

| URI | Result |
|---|---|
| `starter://guide` | Static index of available topics. |
| `starter://guide/{topic}` | Static text for a known topic. |

Current topic names are `architecture`, `security`, and `operations`. Unknown topic instances raise `ResourceNotFoundError`; resource data is static and contains no caller-specific information.

## Prompt: `explain_topic`

The `Explain a starter topic` prompt takes `topic` and an optional `audience` string (default `developer`). It returns a short prompt composed from the topic text and audience. Recognized topics are the same three listed above. This prompt is a user-invoked template, not an authorization or policy mechanism.

## Adding a capability

1. Define the public MCP contract: name, description, schema, errors, side effects, authorization, data sensitivity, cache scope, and bounds.
2. Add a focused module under `features/` and export `register(server)`.
3. Keep domain behavior and external I/O out of the registration module when complexity grows; inject service dependencies through the app composition/lifespan.
4. Register the feature exactly once in `server.py`.
5. Add SDK-boundary tests and relevant security/negative cases.
6. Update this page and the relevant API/security/configuration docs.

The SDK owns schema generation, protocol dispatch, and transport response framing. Do not hand-build JSON-RPC responses inside a capability handler. Review [architecture and protocol](architecture.md) for error and cache semantics.
