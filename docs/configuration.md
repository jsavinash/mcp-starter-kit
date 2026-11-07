# Configuration reference

The shared `Settings` class reads variables prefixed with `MCP_` from the process environment and a UTF-8 `.env` file in the current working directory. Real environment variables override `.env` values. Unknown `MCP_` variables are ignored. List settings accept comma-separated values. Settings are validated at startup and cached once per process by `get_settings()`.

The tracked [.env.example](../.env.example) contains safe local defaults and placeholders. Copy it to `.env` for local changes; never commit secret values.

## Service and transport settings

| Variable | Type / default | Constraints and behavior |
|---|---|---|
| `MCP_SERVER_NAME` | string / `example-server` | Server identity reported by the SDK. |
| `MCP_SERVER_VERSION` | optional string / unset | Uses package version `0.1.0` when unset. |
| `MCP_SERVER_INSTRUCTIONS` | string / `A modular example Model Context Protocol server.` | Instructions supplied to MCP clients. |
| `MCP_TRANSPORT` | `stdio` / `stdio` | Allowed values: `stdio`, `streamable-http`. |
| `MCP_HOST` | string / `127.0.0.1` | HTTP bind host. Non-loopback hosts require OAuth enabled and an explicit non-loopback host allowlist. |
| `MCP_PORT` | integer / `8000` | Range: 1–65535. Used by the HTTP CLI runner. |
| `MCP_HTTP_PATH` | string / `/mcp` | Must begin with `/`; query strings and fragments are rejected. |
| `MCP_MAX_REQUEST_BODY_SIZE` | integer / `4194304` | 1 KiB through 16 MiB. Applies to the SDK Streamable HTTP app. |
| `MCP_LOG_LEVEL` | enum / `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`; input is uppercased. |
| `MCP_LOG_FORMAT` | enum / `console` | `console` or `json`; logs go to stderr. |

## HTTP host and browser origin settings

| Variable | Type / default | Behavior |
|---|---|---|
| `MCP_ALLOWED_HOSTS` | comma-separated strings / `localhost:*`, `127.0.0.1:*`, `[::1]:*` | Passed to SDK DNS-rebinding/host protection. Use exact public host patterns needed by deployment. |
| `MCP_ALLOWED_ORIGINS` | comma-separated strings / empty | Passed to SDK origin protection. Add exact browser origins only when needed. CORS/origin checks do not authenticate callers. |

## OAuth resource-server settings

| Variable | Type / default | Behavior |
|---|---|---|
| `MCP_AUTH_ENABLED` | boolean / `false` | Enables the verifier only for Streamable HTTP. It does not create an identity provider or issue tokens. |
| `MCP_AUTH_ISSUER_URL` | HTTP(S) URL / unset | Trusted authorization server issuer used by the SDK auth metadata. HTTPS required outside loopback development. |
| `MCP_AUTH_RESOURCE_URL` | HTTP(S) URL / unset | Exact public MCP resource URL, including path; used for token resource validation. HTTPS required outside loopback development. |
| `MCP_AUTH_INTROSPECTION_URL` | HTTP(S) URL / unset | RFC 7662 introspection endpoint. HTTPS required outside loopback development. |
| `MCP_AUTH_CLIENT_ID` | string / unset | Resource-server client identity for provider introspection. |
| `MCP_AUTH_CLIENT_SECRET` | secret / unset | Resource-server credential; inject from a secret manager or local environment, not source control. |
| `MCP_AUTH_REQUIRED_SCOPES` | comma-separated strings / empty | All configured scopes are supplied to SDK `AuthSettings` as required scopes. |
| `MCP_AUTH_TIMEOUT_SECONDS` | float / `3.0` | Greater than 0 and at most 30 seconds. Applies to introspection HTTP calls. |

When auth is enabled, all issuer/resource/introspection URLs and client ID/secret are required. Auth enabled with stdio is invalid. A non-loopback Streamable HTTP bind is invalid without auth and at least one non-loopback allowed host. No production IdP is configured by this starter.

## Local HTTP example

```dotenv
MCP_TRANSPORT=streamable-http
MCP_HOST=127.0.0.1
MCP_PORT=8000
MCP_ALLOWED_HOSTS=127.0.0.1:8000,localhost:8000
MCP_AUTH_ENABLED=false
```

This is loopback development only. For remote deployment, see [Deployment](operations/deployment.md) and [Security](operations/security.md).

## Configuration source of truth

The field names, types, and validation rules are defined in `libs/mcp-starter-core/src/mcp_starter_core/config.py`. If changing a setting, update `.env.example`, this page, the security/operations docs as needed, and tests for both valid and invalid combinations.
