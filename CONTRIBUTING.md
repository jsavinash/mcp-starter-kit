# Contributing

## Workspace

This repository uses a uv workspace. Deployable MCP services live in `apps/`; reusable cross-service infrastructure belongs in `libs/`. Do not put application-specific handlers into the shared core package.

```bash
uv sync --all-packages
uv run ruff check .
uv run ruff format --check .
uv run mypy apps libs main.py
uv run pytest
```

## Adding a server app

1. Create `apps/<service>/pyproject.toml` and add it to the uv workspace pattern.
2. Depend on `mcp-starter-core` through a workspace source.
3. Keep `server.py` as the composition root and register capability modules there.
4. Add a CLI entry point for stdio/HTTP and an ASGI app factory if needed.
5. Require OAuth verification and explicit host allowlists before allowing non-loopback HTTP.
6. Update docs and the CI matrix when the new service needs separate build or deployment coverage.

Use typed input schemas and keep tool handlers small. Raise SDK `ToolError` for recoverable execution failures; never leak secrets or internal exception details. Advertise an extension only when it is implemented and negotiated.

## Changes and review

Use focused commits with conventional commit subjects. Before opening a PR, run the relevant lint, type-check, and test commands. Dependency upgrades should update `uv.lock` and be reviewed against the official MCP SDK migration notes.
