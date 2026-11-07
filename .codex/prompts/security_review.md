# MCP security review prompt

Review the change and its deployment context as an application security engineer familiar with MCP. Use actual code paths and configuration; do not infer that a documented safeguard is enforced unless verified.

Prioritize:

- Authentication and per-tool/resource authorization; principal/tenant binding.
- OAuth issuer, audience/resource, expiry, scope, metadata, introspection, redirect, timeout, and secret handling.
- Host/origin validation, DNS rebinding, proxy headers, TLS, and public bind defaults.
- Tool side effects, confused-deputy risks, idempotency, replay/retry, and confirmation for consequential operations.
- Prompt injection and untrusted content from tool inputs/resources/upstream services.
- SSRF, file/process access, egress, path traversal, and resource exhaustion.
- Input/output/body limits, timeouts, concurrency, retries, cache privacy, and error disclosure.
- Logs, traces, and audit data minimization.

Return actionable findings ordered by severity, with file/line, attack preconditions, impact, and concrete remediation. Clearly label assumptions and unverified deployment controls. If no finding is supported, state which threat surfaces were not tested. Do not claim certification or complete conformance.
