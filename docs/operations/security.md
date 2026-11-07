# Security and operations

## OAuth configuration

Remote Streamable HTTP requires a real OAuth resource-server integration. The starter uses the official SDK's `TokenVerifier` and `AuthSettings` hooks and calls the identity provider's RFC 7662 introspection endpoint. It does not issue tokens or host a sign-in/consent flow.

Set the following environment variables from a secret manager or deployment environment:

- `MCP_AUTH_ENABLED=true`
- `MCP_AUTH_ISSUER_URL` — trusted issuer URL
- `MCP_AUTH_RESOURCE_URL` — exact public MCP resource URL requested by clients
- `MCP_AUTH_INTROSPECTION_URL` — provider introspection endpoint
- `MCP_AUTH_CLIENT_ID` and `MCP_AUTH_CLIENT_SECRET` — confidential resource-server credentials
- `MCP_AUTH_REQUIRED_SCOPES` — optional comma-separated minimum scopes
- `MCP_ALLOWED_HOSTS` — exact allowed host values; list bare host and `host:*` when both are needed
- `MCP_ALLOWED_ORIGINS` — exact browser origins when browser clients are used

Outside local development, all OAuth URLs must use HTTPS. `MCP_AUTH_RESOURCE_URL` must be the exact public MCP resource URL the client requests, including path. The SDK's `AuthSettings` advertises the issuer/resource and enforces configured required scopes.

### What the current verifier validates

`OAuthIntrospectionVerifier` sends an RFC 7662 POST using HTTP Basic client authentication, a bounded timeout, and redirects disabled. It accepts a response only when:

- the response is a JSON object with `active` exactly `true`;
- `resource` or `aud` contains the expected MCP resource URL (trailing slash is normalized for comparison);
- `client_id` is a non-empty string;
- `exp`, if present, is an integer or decimal string later than the current time;
- `scope` is a space-delimited string or a list of strings.

The verifier passes only `iss`, `sub`, and `aud` from the provider response into SDK claims and logs generic failure events without token values or response bodies. Provider transport/status/JSON errors fail closed.

**Current implementation limits:** `exp` is not required when the provider omits it, and the adapter does not independently compare the introspection `iss` claim with `MCP_AUTH_ISSUER_URL`. `issuer_url` is configured in SDK `AuthSettings`, but do not assume this makes the custom verifier validate the `iss` field. Confirm your provider's exact introspection contract and add stricter checks/tests if your policy requires them. The example also has no per-tool scope policy beyond globally configured required scopes.

Validate provider behavior in a non-production environment before public deployment. This documentation is not proof of OAuth conformance or a substitute for checking current normative MCP authorization requirements.

## Network boundary

- Keep local development bound to `127.0.0.1`.
- Put TLS termination, request rate limits, concurrency limits, and request timeouts at a trusted proxy/gateway.
- Keep `MCP_ALLOWED_HOSTS` and `MCP_ALLOWED_ORIGINS` narrow. CORS is not authentication.
- The configuration validator checks that a non-loopback host string is present; the SDK transport middleware enforces the allowed-host/origin request checks. Verify actual proxy `Host` and `Origin` behavior end to end.
- Configure trusted proxy headers only for known proxy addresses.
- Restrict outbound network access. If tools fetch URLs, block private/link-local destinations and revalidate redirects and DNS.
- Never add unrestricted shell, filesystem, or URL-fetch tools to a server exposed to untrusted clients.

## Tool design

Treat each tool as an API endpoint. Apply authorization in the domain service, validate input at the boundary, enforce output and execution budgets, and make mutations idempotent. Return anticipated recoverable tool failures with `ToolError`. Do not send stack traces or secrets to MCP clients.

Resources should expose only intended, bounded data. Treat their contents and remote upstream responses as untrusted instructions/data. Avoid putting credentials or tenant-private information into resources without access checks.

## Process and logs

For stdio, stdout is reserved for MCP frames; logs go to stderr. For HTTP, configure TLS/proxy logging in the hosting layer. The starter's structured logs omit payloads and secrets. Avoid attaching raw tool arguments, resource text, access tokens, or introspection responses to logs or traces.

The HTTP body size defaults to 4 MiB and is configurable up to 16 MiB. Raise it only when valid protocol payloads require more. The app has an optional OpenTelemetry dependency extra but does not configure an exporter or provide an observability deployment. If telemetry is enabled by deployment code, follow data minimization and retention policies.

## Deployment checklist

- [ ] OAuth verifier uses the expected issuer, audience/resource, expiry, and scopes.
- [ ] Public host and browser origin allowlists match the deployment hostname exactly.
- [ ] TLS and trusted proxy settings are verified end to end.
- [ ] Rate, concurrency, timeout, and egress policies are enforced at the service boundary.
- [ ] Secrets come from a secret manager; `.env` is never committed.
- [ ] Tool side effects are authorized, bounded, and safe to retry.
- [ ] Logs and traces contain no tokens or user payloads.
- [ ] Extensions are advertised only after negotiated implementation and conformance review.
- [ ] Verifier claim requirements (issuer, expiry, audience/resource, scopes, client identity) match provider behavior and risk policy, with automated negative tests.
- [ ] Actual app/core behavior is covered by tests; current visible tests do not exercise MCP handlers or auth middleware.
