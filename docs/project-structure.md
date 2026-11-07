# Project structure

The repository is a monorepo managed by one root `uv` workspace and one `uv.lock` file.

```text
.
├── apps/
│   └── example-server/
│       ├── pyproject.toml
│       ├── Dockerfile
│       └── src/mcp_example_server/
│           ├── cli.py              # stdio / Streamable HTTP runner
│           ├── http_app.py         # ASGI entry point
│           ├── dev.py              # MCP Inspector target
│           ├── server.py           # composition root
│           └── features/           # tools, resources, prompts
├── libs/
│   └── mcp-starter-core/
│       ├── pyproject.toml
│       └── src/mcp_starter_core/
│           ├── config.py           # typed environment settings
│           ├── auth.py             # RFC 7662 token verifier
│           ├── lifecycle.py        # shared async startup/shutdown
│           ├── logging.py          # structured stderr logs
│           └── transport.py        # HTTP host/origin protections
├── tests/                          # root workspace tests
├── docs/                           # MkDocs site source
├── .github/workflows/ci.yml        # quality, tests, Docker build
├── .codex/                         # project Codex settings and workflows
├── pyproject.toml                  # root tooling and workspace config
├── uv.lock                         # resolved workspace dependencies
├── Makefile                        # common development commands
├── docker-compose.yml              # local container template
└── main.py                         # compatibility convenience entry point
```

## Package ownership

### `apps/example-server`

Owns the runnable `mcp-example-server` package: capability registrations, MCP server construction, command-line startup, ASGI app, and service-specific behavior. New deployable services belong in `apps/<service>/` and should declare their own package metadata and console command.

### `libs/mcp-starter-core`

Owns infrastructure intended to be shared across apps: typed settings, OAuth token verification, lifecycle helpers, structured logs, and transport security configuration. It must not import app packages or contain example tools/resources/prompts.

### Root workspace

The root `pyproject.toml` manages workspace members, shared quality tooling, and dependency sources. Keep dependency resolution in the committed root `uv.lock`; regenerate it with `uv` after metadata changes.

## Dependency direction

```text
apps/<service>  →  mcp-starter-core  →  official mcp SDK
       └────────────────────────────→ official mcp SDK
```

The app is the composition edge: it binds core services/settings to capability modules and the SDK. Core should depend on the SDK only for shared MCP infrastructure interfaces, not on app implementation.

## Entry points

| Entry point | Use |
|---|---|
| `mcp-example-server` | Installed CLI; selects stdio or Streamable HTTP from settings. |
| `python -m mcp_example_server` | Equivalent module entry point. |
| `mcp_example_server.http_app:app` | ASGI deployment; requires Streamable HTTP settings before import. |
| `mcp_example_server.dev:mcp` | SDK CLI / Inspector development target. |
| `main.py` | Compatibility convenience entry point retained from the source starter; installed apps use the app console script. |

## Codex instructions

Project-specific instructions are consolidated in `.codex/AGENTS.md`. This repository intentionally has no root or per-package `AGENTS.md` copies. Consult [Codex project setup](codex.md) for the setup and hook behavior. Some agent clients only auto-load a root `AGENTS.md`; follow the client-specific supported mechanism to include the centralized file rather than copying its contents into several files.
