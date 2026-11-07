# Code review prompt

Review the current diff as a senior Python and MCP engineer. Report actionable findings first, ordered by severity, with file and line references. Do not report style preferences unless they create a concrete maintenance or correctness problem.

## Review for

1. **Correctness:** broken behavior, edge cases, concurrency, lifecycle cleanup, cancellation, timeouts, and error mapping.
2. **MCP contract:** accurate tool/resource/prompt schemas and descriptions; valid SDK usage; compatibility with the documented specification target; no unsupported capability claims.
3. **Security:** auth bypasses, unsafe HTTP binding, SSRF or DNS rebinding exposure, missing host/origin checks, unbounded input/output, secret leakage, unsafe file/process/network access, and overly broad permissions.
4. **Architecture:** app/core ownership, unwanted dependency direction, unnecessary abstractions, hidden global state, and duplicate implementations.
5. **Operations:** configuration validation, observability without sensitive data, deterministic startup/shutdown, packaging, container, and docs consistency.
6. **Tests:** missing coverage for changed public behavior, regressions, error cases, and security boundaries.

## Output format

- Findings: `[P0–P3]` title, file:line, impact, and a concrete fix.
- Questions or assumptions that block a confident review.
- If there are no actionable findings, say so and mention important areas not verified.

Do not claim tests or commands were run unless their output is available. Distinguish verified defects from potential risks.
