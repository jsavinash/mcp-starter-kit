# Transports and entry points

The example app exposes stdio and Streamable HTTP from one `MCPServer` composition. Transport choice is controlled by `MCP_TRANSPORT` for the CLI; the ASGI module is HTTP-only.

## stdio

Use stdio when an MCP host launches the server as a child process. It is the default transport:

```bash
uv run --package mcp-example-server mcp-example-server
```

The process boundary is the trust boundary. HTTP bearer auth does not protect stdio; do not pass secrets to a server process unless the host and process environment are trusted. Stdout is reserved for MCP protocol frames, so logs and diagnostics must go to stderr.

## Streamable HTTP

For local development:

```bash
MCP_TRANSPORT=streamable-http uv run --package mcp-example-server mcp-example-server
```

The default listener is `127.0.0.1:8000`, endpoint `/mcp`. The SDK app is configured with host/origin protections, a request-body cap, and `json_response=False` in both CLI and ASGI paths.

Modern protocol requests use the current SDK's Streamable HTTP behavior, including protocol routing metadata/headers. Do not strip or rewrite MCP routing headers in a reverse proxy. See [architecture](architecture.md) for version-specific details.

## ASGI

The ASGI object is `mcp_example_server.http_app:app`:

```bash
MCP_TRANSPORT=streamable-http uv run --package mcp-example-server uvicorn mcp_example_server.http_app:app
```

The module calls `get_settings()` at import and raises if the configured transport is not Streamable HTTP. The ASGI host is responsible for process workers, TLS/proxy integration, health/readiness, and platform shutdown behavior.

## MCP Inspector

For interactive development:

```bash
uv run mcp dev apps/example-server/src/mcp_example_server/dev.py
```

This target creates the same server via `create_server()`.

## Legacy SSE

SSE is not selected by this app or its configuration. Use Streamable HTTP for new HTTP deployments. If compatibility with an older client is required, test the official SDK's compatibility behavior and document the exact supported client/protocol versions.

## No custom health RPC

The server does not register a custom health MCP tool or HTTP endpoint. Use the hosting platform's process health/readiness mechanism or add a deliberate outer ASGI health route if deployment requires one. Do not confuse an MCP capability with platform liveness.
