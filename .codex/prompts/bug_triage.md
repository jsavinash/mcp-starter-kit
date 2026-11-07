# Bug triage prompt

Triage the reported issue using repository evidence. Preserve the report's observed behavior; do not assume the cause.

## Workflow

1. Restate expected versus observed behavior and identify the affected app, transport, and capability.
2. Trace the path from CLI/ASGI entry point through server composition, feature code, shared core, and SDK boundary.
3. Check settings, environment variables, logs, and existing tests. Redact tokens, secrets, personal data, and sensitive payloads from any diagnostic output.
4. Form the smallest plausible root-cause hypothesis and identify evidence that would confirm or reject it.
5. Reproduce with the narrowest safe command or focused test. Avoid public network calls or production mutations unless explicitly authorized.
6. Fix the root cause, add a regression case, and update docs if the contract or configuration changed.
7. Run relevant checks from `.codex/skills/validation.md` and report exact results.

## MCP-specific checks

- Confirm transport and SDK version, including whether the issue is stdio or Streamable HTTP.
- For HTTP auth issues, inspect token verifier configuration, issuer/introspection reachability, audience/resource, scopes, host allowlist, and origin behavior without printing credentials.
- For tool issues, inspect input validation, timeout/cancellation, dependency lifecycle, output shape, and recoverable error behavior.
- Separate protocol errors from application errors and transport/security middleware failures.

## Triage output

Include impact/severity, reproduction, evidence, suspected cause, proposed fix, and checks run or still needed. Mark uncertain conclusions as hypotheses.
