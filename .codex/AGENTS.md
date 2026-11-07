# Codex guidance for this repository

This is the single consolidated `AGENTS.md` for the repository. Keep project instructions here instead of adding root, app, or library copies. Codex project hooks and workflows are indexed in `.codex/README.md` and documented for contributors in `docs/codex.md`.

## Repository shape

- This is a Python `uv` workspace monorepo. Deployable MCP servers live in `apps/`; shared runtime code lives in `libs/`.
- The official Python MCP SDK is pinned to the v2 API line. Do not introduce FastMCP v1 imports or APIs into production code without an explicit migration decision; see `docs/architecture.md` for the selected protocol and SDK target.
- Keep protocol registration at the application edge and reusable configuration, auth, lifecycle, logging, and transport security in `mcp-starter-core`.

## Package boundaries

- `apps/<service>/` owns the service package, composition root, capability registrations, CLI, and ASGI boundary. The current example package is `mcp-example-server`.
- `libs/mcp-starter-core` owns only reusable infrastructure: settings, OAuth verification, lifespan helpers, structured logging, and HTTP transport policy. It must not import app packages or own service-specific tools/resources/prompts.
- Add features as focused modules under `apps/<service>/src/<package>/features/`, export `register(server)`, and wire each module once from the composition root.
- Keep handlers typed, bounded, and small. Move business rules and external I/O into services when introduced.

## Development commands

- Install: `uv sync --all-packages`
- Run example over stdio: `uv run --package mcp-example-server mcp-example-server`
- Run local Streamable HTTP: `make run-http`
- Lint/format: `make lint` and `make format-check`
- Type check: `make typecheck`
- Tests: `make test`
- Dependency audit/docs/container: `make security`, `make docs`, `make docker-build`
- Refresh dependency resolution after metadata edits: `uv lock`; never edit `uv.lock` manually.

## Change boundaries

- Treat `.codex/goals/`, `.codex/plans/`, `.codex/prompts/`, and `.codex/skills/` as project guidance and reusable recipes, not as executable automation.
- Never place credentials, access tokens, or production secrets in project files. Use environment variables and document variable names only.
- Preserve fail-closed remote HTTP security. Never make an unauthenticated public bind the default.
- Use SDK `ToolError` for expected, recoverable tool failures and `ResourceNotFoundError` for missing resource instances. Never leak exception details or upstream response bodies.
- Public cache hints are valid only for identical data shared across callers; keep user/tenant-specific data private or uncached.
- Keep stdio stdout reserved for protocol traffic; logs belong on stderr. Do not advertise extensions unless implemented and negotiated.
- Update architecture/security/operations docs when protocol, configuration, auth, transport, or deployment guarantees change.
- Do not claim a command succeeded unless it was run and its result inspected. Prefer the commands in `.codex/skills/validation.md`.
- Database migration guidance is currently prospective: this repository has no database or migration framework.

## Codex MCP integration

- The project MCP server in `config.toml` is disabled by default. Enable it locally only when you intend Codex to connect to the example server.
- Review a server's tools and effects before enabling it. Keep approval prompts for tools that can change external state.
- Project hooks are advisory and must never auto-approve a permission request. They do not replace sandboxing, user approval, CI, or application security controls.
