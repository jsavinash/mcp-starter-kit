# Current run plan

No implementation run is active by default. Copy this checklist into a task-specific plan or issue and update it when work begins.

## Start checklist

- [ ] State the user-visible outcome and acceptance criteria.
- [ ] Inspect root and nearest nested `AGENTS.md`, project docs, and relevant tests.
- [ ] Identify affected app/library boundaries and MCP protocol surface.
- [ ] Check current MCP specification and official SDK docs if protocol behavior may have changed.
- [ ] Record security, compatibility, configuration, and migration implications.

## Implementation checklist

- [ ] Make the smallest cohesive change in the correct workspace package.
- [ ] Add or update focused tests for changed behavior.
- [ ] Update operator or architecture docs when behavior/configuration changes.
- [ ] Review diff for secrets, unsafe defaults, accidental broad scope, and generated artifacts.

## Closeout checklist

- [ ] Run only the requested or relevant checks from `.codex/skills/validation.md`.
- [ ] Record exact commands and outcomes; include skipped checks and reasons.
- [ ] Summarize files changed, behavior, risks, and remaining work.

This is a reusable template. Checkboxes are not evidence that work has been performed.
