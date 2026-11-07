# Development guide

## Install the workspace

From the repository root:

```bash
uv sync --all-packages
```

This installs both workspace packages and the root default development group. The root project sets Ruff to a 100-character line limit and Python 3.11 target; MyPy uses strict mode across `apps`, `libs`, and `main.py`.

## Common commands

| Command | Purpose |
|---|---|
| `make install` | Sync all workspace packages and root dev tools. |
| `make run-stdio` | Run example over stdio. |
| `make run-http` | Run local Streamable HTTP. |
| `make lint` / `make format` | Ruff lint / apply Ruff formatting. |
| `make format-check` | Check formatting without modifying files. |
| `make typecheck` | Strict MyPy over `apps libs main.py`. |
| `make test` | Run pytest quietly. |
| `make security` | Audit resolved Python dependencies with pip-audit. |
| `make docs` / `make docs-serve` | Build or serve MkDocs. |
| `make docker-build` | Build local example image. |
| `make hooks-install` | Install pre-commit hooks. |
| `make clean` | Remove Python caches and generated build/doc/test output listed by the Makefile. |

The equivalent raw commands are in the root `Makefile`. Use `make format` only when you intend formatting edits.

## Add a deployable service

1. Create `apps/<service>/pyproject.toml` and a `src/<package>/` tree.
2. Add the app to the root uv workspace pattern (currently `apps/*`) and declare a workspace source for shared core dependencies.
3. Keep a single server composition root that wires capabilities, typed settings, auth, cache policy, and lifespan.
4. Add a CLI for supported transports and an ASGI object if that deployment style is needed.
5. Keep cross-service infrastructure in `libs/mcp-starter-core`; do not move app capabilities into core.
6. Add tests and docs. Update CI/package/container coverage only where needed for the app.
7. Run `uv lock` after dependency metadata changes; never hand-edit `uv.lock`.

## Add an MCP capability

Add a focused feature module with `register(server)` and wire it once in the app composition root. Use typed parameters and Pydantic constraints, declare side effects, bound external calls and outputs, and use SDK errors correctly. See [Capabilities](capabilities.md) and the [feature plan](../.codex/plans/add_mcp_capability.md).

## Dependencies and optional features

- Root dependency groups: `dev` and `docs`.
- App runtime dependency: shared `mcp-starter-core` workspace package.
- Core runtime dependencies: official `mcp`, `httpx`, `pydantic-settings`, and `structlog`.
- App optional extra `observability`: OpenTelemetry SDK and OTLP exporter packages. Installing the extra alone does not configure or export telemetry; deployment code must configure providers/exporters.

Keep dependency bounds and Python support deliberate. After editing package metadata, run `uv lock`, then verify `uv sync --all-packages --locked` and relevant checks.

## Code conventions and boundaries

- The root `.codex/AGENTS.md` is the consolidated project instruction file; do not add duplicate per-folder instruction copies.
- App capabilities belong in the app; reusable infrastructure belongs in core.
- Keep stdout clean for stdio, avoid logging arguments/payloads/tokens, and fail closed on invalid remote config.
- Document externally visible configuration, behavior, compatibility, and operational assumptions.
- Preserve unrelated workspace changes; review `git status` before staging.

## Pre-commit

`.pre-commit-config.yaml` runs Ruff with auto-fix, Ruff format, trailing whitespace/EOF/YAML/TOML/merge-conflict checks, and private-key detection. The root dependency groups do not currently include the `pre-commit` runner, while `make hooks-install` assumes `pre-commit` is available to `uv run`; install/provide that command separately or add it to the dev group before relying on this target. CI does not currently run pre-commit. CI remains authoritative for the workflow commands it runs.
