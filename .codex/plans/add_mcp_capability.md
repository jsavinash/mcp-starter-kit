# Plan template: add an MCP capability

Copy this file to a task-specific plan and replace the prompts before implementation.

## Goal and contract

- Capability type: tool / resource / prompt / extension
- User problem and expected result:
- Name, description, schema, and authorization policy:
- Side effects, idempotency, retry, cache scope, and data sensitivity:
- Protocol revision and client compatibility requirements:

## Design

- Feature module and registration point:
- Domain/service dependencies:
- Configuration and secret names (never secret values):
- Input/output/resource size, time, concurrency, and network bounds:
- Expected errors and behavior for unexpected errors:
- Lifecycle, cancellation, observability, and cleanup:

## Implementation sequence

1. Confirm the contract against current official SDK/spec docs.
2. Add focused handler/service tests and negative cases.
3. Implement the capability in an isolated module and register once from `server.py`.
4. Add policy checks for authorization and side effects.
5. Update architecture, security, user docs, and samples.
6. Run relevant validation and inspect the final diff.

## Acceptance and evidence

- [ ] Correct app/core ownership.
- [ ] Schema and output behavior are tested through the SDK boundary.
- [ ] Authorization, bounds, and failure behavior are covered.
- [ ] Cache metadata matches data sensitivity.
- [ ] Tests/checks and exact outcomes recorded.
- [ ] Documentation matches actual behavior.
