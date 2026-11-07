# Proposed engineering roadmap

**Status:** proposed, not an active run. Priorities should be adjusted to user-facing goals and issue tracking.

## Phase 1 — Prove existing contracts

- Add tests for Settings parsing and invalid remote deployment combinations.
- Test OAuth verifier with a mock transport: inactive, expired, malformed, wrong audience/resource, valid scopes, timeout/redirect/error, and secret-safe logs.
- Exercise tool/resource/prompt calls through the official SDK client and assert structured errors and schemas.
- Test CLI transport selection, lifecycle cleanup, cache scopes, and HTTP security settings.
- Keep auth tests entirely local; never require a live identity provider in CI.

## Phase 2 — Close architecture drift

- Decide whether root `main.py` remains supported; remove it and its smoke test if legacy-only, or define its package ownership clearly.
- Make `server_lifespan` service identity generic/configurable instead of embedding the example app name in shared core.
- Confirm MkDocs navigation, in-text anchors, README commands, CI, and Makefile targets agree.

## Phase 3 — Add conformance and operations evidence

- Add a protocol/transport integration suite for modern discovery and target revision metadata/cache behavior, plus legacy peer behavior if promised.
- Add docs build and package build checks to CI; evaluate time and maintenance cost.
- Define health/readiness at the hosting layer rather than adding a non-standard MCP health method.
- Document a concrete supported deployment target and verified proxy header/TLS behavior before adding deployment automation.

## Phase 4 — Multi-app scalability

- Add a second small sample service only when needed to prove the shared core contract.
- Validate per-app settings and lifespan isolation, dependency metadata, lockfile behavior, and Docker build boundaries.
- Extract additional core abstractions only after there is a second real consumer.

## Phase 5 — Release maturity

- Choose package/release versioning and compatibility policy for app and core packages.
- Add changelog/release automation, artifact provenance, vulnerability response, and deployment rollout/rollback procedures as the repository's distribution model becomes known.

## Exit criteria

Each phase should produce reviewed code/docs, focused automated coverage, recorded validation evidence, and a clear statement of remaining risks. Do not mark a phase complete because a checklist was copied or because its files exist.
