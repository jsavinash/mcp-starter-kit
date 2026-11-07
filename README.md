# MCP Starter Kit

A Python monorepo starter for building and deploying modular Model Context Protocol servers with the official Python SDK, `uv`, and a reusable core package.

> **SDK API note:** This repository targets the official Python SDK v2 API line and MCP `2026-07-28`. Its high-level server is `MCPServer`; `FastMCP` is the SDK v1 API. See [Architecture and protocol](docs/architecture.md#sdk-and-specification-versioning) for the version choice.

## Quick start

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --all-packages
cp .env.example .env
uv run --package mcp-example-server mcp-example-server
```

That starts stdio mode, which is the right transport for a local MCP host that launches the process. To run Streamable HTTP locally:

```bash
MCP_TRANSPORT=streamable-http uv run --package mcp-example-server mcp-example-server
```

The endpoint is `http://127.0.0.1:8000/mcp`. Use the Inspector during development:

```bash
uv run mcp dev apps/example-server/src/mcp_example_server/dev.py
```

To host the ASGI app with uvicorn:

```bash
MCP_TRANSPORT=streamable-http uv run --package mcp-example-server uvicorn mcp_example_server.http_app:app
```

Remote HTTP binds require OAuth introspection configuration and an explicit host allowlist. A boolean setting alone never enables authentication. See [deployment and security](docs/operations/security.md).

## Workspace map

```text
apps/
└── example-server/                  # Deployable service, CLI, ASGI app, capabilities
    └── src/mcp_example_server/
        ├── server.py                # Composition root
        ├── cli.py                   # stdio and HTTP runner
        ├── http_app.py              # uvicorn/ASGI entry point
        └── features/                # tools, resources, prompts
libs/
└── mcp-starter-core/                # Reusable config, auth, lifecycle, logging
    └── src/mcp_starter_core/
docs/
├── architecture.md
└── operations/security.md
```

Each deployable MCP server belongs under `apps/`. Cross-service configuration, OAuth resource-server integration, lifecycle, and transport security belong in `libs/mcp-starter-core`. Keep business logic in feature/service modules; keep MCP registration and transport setup at the app edge.

## Included capabilities

- **Tools:** typed schema-driven calculator example with an expected `ToolError` for recoverable failures.
- **Resources:** static guide resource and URI-template resource with typed not-found errors.
- **Prompts:** user-invoked topic explanation prompt.
- **Transports:** stdio and Streamable HTTP; SSE is legacy and not selected for new services.
- **OAuth resource server:** optional RFC 7662 introspection verifier using the SDK's `TokenVerifier` and `AuthSettings` hooks. It checks active status, expiration, scope shape, and resource/audience, and never logs bearer tokens.
- **Runtime:** typed environment config, lifespan-managed HTTP client, JSON/console structured logs to stderr, request body limit, DNS rebinding/host/origin protection, Docker image, and CI workflows.
- **Protocol:** the SDK owns JSON-RPC dispatch, compatibility, per-request metadata, routing headers, and OpenTelemetry spans. Stable demo listings/read resources declare short-lived public cache hints.

MCP Tasks, Apps, and other extensions are opt-in. This starter does not advertise extensions it has not implemented.

## Common commands

```bash
make install          # sync all workspace projects and root dev tools
make run-stdio        # launch the example over stdio
make run-http         # launch local Streamable HTTP
make lint             # Ruff lint
make format           # Ruff format
make typecheck        # MyPy
make test             # Pytest
make security         # pip-audit
make docs             # build the MkDocs site
make docker-build     # build the example server image
```

`docker compose up` is a protected remote-bind template. It fails closed until `.env` contains
complete OAuth introspection settings and a host allowlist for the deployment.

Configuration is documented in [.env.example](.env.example) and the [configuration reference](docs/configuration.md). Start at the [documentation site](docs/index.md) for the complete guides. The protocol and implementation decisions are in [Architecture](ARCHITECTURE.md). Operational guidance is in [Security](docs/operations/security.md) and [Deployment](docs/operations/deployment.md).
