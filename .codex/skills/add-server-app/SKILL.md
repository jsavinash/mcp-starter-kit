---
name: add-server-app
description: Add a new deployable MCP server to the uv monorepo while preserving app/core package ownership, transport security, workspace configuration, and CI coverage.
---

# Add a server app

1. Read `CONTRIBUTING.md`, root `AGENTS.md` if present, `.codex/research/project_structure.md`, and `.codex/plans/architectural_vibe.md`.
2. Confirm there is a real second service/use case; do not create an empty app just to prove the monorepo can contain multiple apps.
3. Create `apps/<service>/` with package metadata, `src/<package>/`, a composition root, and an intentional CLI/ASGI surface. Add a service-local `AGENTS.md` only when its rules differ materially from root guidance.
4. Depend on `mcp-starter-core` through the uv workspace. Keep service capabilities and business rules in the app; move infrastructure into core only when reusable.
5. Use typed settings and fail-closed configuration. Preserve stdio/Streamable HTTP semantics and require OAuth plus explicit host controls for non-loopback HTTP.
6. Add unit/SDK-boundary tests, docs, workspace source entries, CI coverage, and container support only when the app needs them.
7. Regenerate the lockfile through `uv lock`, validate the workspace, and check that all app metadata and command examples resolve.

Do not assume that running multiple stateless MCP workers makes downstream state safe; document persistence, idempotency, and principal binding where relevant.
