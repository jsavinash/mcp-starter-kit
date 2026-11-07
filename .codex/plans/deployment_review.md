# Plan template: remote deployment review

Do not use this as a deployment command checklist alone. It is a design review that must be completed for the actual target platform.

## Deployment facts

- Platform/region/network ingress:
- Public resource URL and path:
- TLS termination and certificate ownership:
- Reverse proxy/load balancer and trusted forwarded headers:
- Identity provider, issuer, resource/audience, introspection, scopes:
- Secret manager and rotation procedure:
- Rate/concurrency/request timeout and body size limits:
- Egress allowlist and DNS/redirect policy:
- Logs/traces retention and access:

## Required checks

- [ ] Non-loopback bind has OAuth verifier and explicit narrow host allowlist.
- [ ] Resource URL, issuer, introspection URL, scopes, and clients match the provider contract.
- [ ] TLS and proxy headers cannot be spoofed from untrusted sources.
- [ ] Browser origins are exact; CORS is not treated as auth.
- [ ] Rate, concurrency, timeouts, egress, and body limits are enforced.
- [ ] Tool actions have principal-aware authorization and idempotency.
- [ ] No tokens or user payloads enter logs/traces.
- [ ] Health/readiness uses platform conventions and does not expose sensitive details.
- [ ] Rollout, rollback, backup/state migration, and incident contacts are known.

## Evidence

Record environment, redacted configuration shape, checks performed, owners, and unresolved risks. Never copy credential values into this file.
