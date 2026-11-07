# Troubleshooting

## Workspace sync fails

Run `uv sync --all-packages` from the repository root. Check Python compatibility (`>=3.11`), uv availability, and that the workspace dependency metadata and `uv.lock` agree. After dependency metadata changes, run `uv lock` and commit the resulting lockfile; do not edit it by hand.

## The stdio host says the server disconnected or has no tools

Run the CLI manually to inspect stderr:

```bash
uv run --package mcp-example-server mcp-example-server
```

Confirm the host uses the repository root as its working directory and invokes the console script through `uv`. Remove startup banners or `print()` calls from stdout; stdio stdout must contain only protocol frames. Check that dependencies are installed and that host configuration points to the intended executable/arguments.

## Streamable HTTP refuses to start

- Confirm `MCP_TRANSPORT=streamable-http`.
- For local use, keep `MCP_HOST=127.0.0.1` and use the correct port/path.
- For a non-loopback host, set `MCP_AUTH_ENABLED=true`, all required issuer/resource/introspection/client credentials, and a non-loopback `MCP_ALLOWED_HOSTS` entry.
- Use HTTPS URLs outside loopback development.
- The ASGI module raises if imported with stdio transport configured.

Do not remove the fail-closed checks to make a public bind start.

## Host/origin request rejected

Confirm the request `Host` matches `MCP_ALLOWED_HOSTS` and, for browser callers, the `Origin` matches `MCP_ALLOWED_ORIGINS`. Use exact host/origin syntax for the deployed proxy path; do not add broad wildcards without review. CORS/origin acceptance does not authenticate the caller.

## OAuth returns 401

Check the provider is reachable from the server, the introspection endpoint accepts the configured client authentication, the token is active and unexpired, and its `resource` or `aud` exactly matches `MCP_AUTH_RESOURCE_URL`. Confirm the provider returns a `client_id` and a string or string-list scope value. If required scopes are configured, the SDK enforces them through `AuthSettings`.

The app logs a generic introspection failure event and intentionally avoids logging tokens or response bodies. Use provider-side diagnostics or a controlled staging environment; do not temporarily log bearer tokens.

## Compose exits during startup

Compose forces `MCP_HOST=0.0.0.0`. The checked-in `.env.example` has auth disabled and loopback-only allowlists, so this configuration is expected to fail closed. Provide complete non-production OAuth settings and an exact hostname allowlist, or use the local loopback CLI for development.

## HTTP body exceeds configured limit

Default is 4 MiB. The setting is capped at 16 MiB. Increase only when valid MCP payloads require it and align upstream proxy limits; the body cap does not replace rate/concurrency limits.

## Documentation build unavailable

Run `uv run --group docs mkdocs build --strict` from the root. The docs dependency group may need to be synchronized first. The build can require package downloads when dependencies are not cached, so verify network access and uv cache permissions.

## Issue-report checklist

Include Python/uv versions, transport, sanitized command/environment shape, server stderr, client/Inspector behavior, and exact reproduction steps. Remove tokens, client secrets, user data, and raw introspection responses before sharing logs.
