# Repository structure and architecture review

**Reviewed:** 2026-11-07
**Scope:** tracked/untracked source tree, project metadata, tests, CI, docs, container, and existing Codex guidance. This is a snapshot, not a claim that later changes were reviewed.

## Executive summary

The repository is a small Python `uv` workspace organized as a deployable example server plus a shared infrastructure library. It already has a clear composition root, stdio and Streamable HTTP entry points, typed tool examples, environment-driven configuration, an OAuth introspection adapter, transport security, Docker hardening, CI, and architecture/security documentation.

The most important next architectural investment is executable coverage of the actual MCP application and security boundaries. At review time, the visible test suite consists of a test for the legacy root `main.py`; it does not visibly test MCP tool/resource/prompt contracts, settings validation, OAuth claims, lifecycle cleanup, HTTP host/origin policy, or process startup. A starter kit should demonstrate those safeguards rather than only document them.

## Observed structure

```text
apps/example-server/          Deployable MCP server, CLI, ASGI app, features
libs/mcp-starter-core/        Shared settings, auth, lifecycle, logs, HTTP policy
tests/                        Root workspace tests (currently only legacy main smoke test)
docs/                         Architecture, operations/security, MkDocs home
.github/workflows/ci.yml      Quality, Python 3.11–3.13 tests, Docker build
.codex/                       Codex config, goals, plans, prompts, recipes, research
```

### Runtime path

`cli.main()` loads `Settings`, configures stderr logging, creates the MCP server, then chooses stdio or Streamable HTTP. `server.create_server()` wires shared auth/lifespan and static tool/resource/prompt registrations. `http_app.py` creates the ASGI HTTP app from the same composition function. This is a useful transport-independent seam for tests and future app-specific services.

### Package ownership

- `mcp-example-server` owns protocol capability registration, settings-to-server wiring, CLI, ASGI setup, and its container entry point.
- `mcp-starter-core` owns shared settings, RFC 7662 introspection, lifespan helper, structured logs, and transport security construction.
- The root project owns workspace membership, lockfile, tooling, and shared commands.

### Security posture visible in code/docs

- Defaults use stdio and loopback HTTP.
- Non-loopback HTTP settings require OAuth and at least one non-loopback allowlisted host.
- OAuth introspection uses Basic client authentication, bounded timeout, no redirects, and a safe claim projection; token/body failures do not expose provider response text.
- The server app configures SDK host/origin protections and a bounded HTTP request body.
- The container uses a non-root user, read-only root filesystem, dropped capabilities, no-new-privileges, and loopback host port publishing in compose.
- Documentation warns that stdio trusts the launching process and that CORS is not authentication.

These are design observations, not a penetration test or deployment review.

## Important current-state findings

1. **Test coverage does not yet prove the starter's advertised behavior.** `tests/test_main.py` checks only `main.py`; add focused suites for settings, verifier, feature handlers, server wiring/cache scopes, CLI, and transport policy before presenting these as verified behavior.
2. **Root legacy app is outside the documented monorepo boundaries.** Root `main.py` and its test still exist even though README/architecture describe app packages under `apps/`. Decide whether to remove them or formally document the root module; do not silently grow it into a second app.
3. **Shared lifespan currently reports a fixed service name.** `server_lifespan` yields `{"service": "mcp-example-server"}` even though `server_name` is configurable. If multiple apps consume the core, pass app identity into the lifespan factory or remove app-specific identity from core.
4. **Version-controlled change set is broader than `.codex/`.** At review time, the workspace has pre-existing edits/deletions from its conversion to the MCP monorepo. Keep those distinct from this agent-guidance work; never revert or stage them as a side effect.
5. **CI quality and test jobs differ.** The quality job checks lint/format/types/dependencies/build; the matrix tests Python 3.11–3.13; container build waits on both. Documentation build and runtime transport integration are not visibly part of CI.
6. **Operational limits have gateway responsibilities.** App code limits HTTP request bodies and protects host/origin; deployment docs place rate, concurrency, TLS, timeouts, and egress controls at a trusted edge. Confirm the deployment platform actually supplies these controls.
7. **Version-sensitive protocol guidance needs scheduled review.** The repository intentionally targets MCP `2026-07-28` and SDK v2. Keep the latest protocol claims linked to official source docs and review on SDK/spec changes.

## Strengths to preserve

- One app composition root and explicit capability registration.
- Shared core is infrastructure-only and import direction is clear.
- Stdio/HTTP use the same server definition.
- Public remote bind fails closed rather than treating a boolean as authentication.
- Logs go to stderr, protecting stdio protocol output.
- Cache hints are explicit and only public for static identical data.
- Optional OpenTelemetry dependencies avoid burdening every local install.
- Deployment docs state limits instead of pretending app middleware is a full edge security layer.

## Suggested sequence

1. Add app/core tests, especially negative security tests and direct SDK client tests for tool, resource, prompt, and discovery/list behavior.
2. Decide the fate of root `main.py` and remove obsolete starter-kit residue if it has no supported purpose.
3. Make service identity in core lifecycle caller-configurable or generic.
4. Add contract/conformance and local transport smoke checks where SDK test harnesses make them stable.
5. Add docs build and package build checks to CI if the runtime budget permits.
6. Add release/deployment automation only after the supported hosting and versioning model is explicit.

## Source files consulted

`README.md`, root and nested `AGENTS.md`, `pyproject.toml`, app/core `pyproject.toml`, app entry points and features, core modules, tests, `Makefile`, CI, Dockerfile, Compose file, `.env.example`, architecture/security docs, and MkDocs navigation.
