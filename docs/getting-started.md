# Getting started

This guide gets the example MCP server running locally. The repository is a Python `uv` workspace with an example app and a shared infrastructure package.

## Requirements

- Python 3.11 or later (the repository's `.python-version` currently selects 3.12).
- [uv](https://docs.astral.sh/uv/) for environment and workspace management.
- Git for checkout and change tracking.
- Docker only if you want to build or run the container image.

The project uses the official Python `mcp` SDK v2 API line. Install from the repo root:

```bash
uv sync --all-packages
```

The root project is a workspace/tooling project rather than an installable application package. `uv sync --all-packages` installs the example service, shared core, and default development tools.

## Run over stdio

The default transport is stdio, intended for an MCP host that launches the process:

```bash
uv run --package mcp-example-server mcp-example-server
```

Configure the MCP host to run `uv` with arguments `run --package mcp-example-server mcp-example-server` and the repository root as its working directory. The host and server communicate over stdin/stdout. Do not print banners or diagnostics to stdout; application logs use stderr.

To run through Python's module entry point instead:

```bash
uv run --package mcp-example-server python -m mcp_example_server
```

## Run local Streamable HTTP

```bash
MCP_TRANSPORT=streamable-http uv run --package mcp-example-server mcp-example-server
```

The default address is `http://127.0.0.1:8000/mcp`. It is loopback-only and uses no OAuth authentication by default. This is for local development; public deployment is a separate configuration path. See [Configuration](configuration.md), [Transports](transports.md), and [Security](operations/security.md).

The Make target is equivalent:

```bash
make run-http
```

## Explore with the MCP Inspector

The development dependency group includes the SDK CLI:

```bash
uv run mcp dev apps/example-server/src/mcp_example_server/dev.py
```

The dev module creates the same server composition as the CLI. Use the Inspector to discover the server and exercise the example tool, resources, and prompt.

## Run the ASGI app

For an ASGI host such as Uvicorn:

```bash
MCP_TRANSPORT=streamable-http uv run --package mcp-example-server uvicorn mcp_example_server.http_app:app
```

The ASGI module validates transport configuration during import. It raises unless `MCP_TRANSPORT=streamable-http` is set.

## Next steps

- Review the [repository structure](project-structure.md) and [architecture](architecture.md).
- Explore [example capabilities](capabilities.md) and [transport choices](transports.md).
- Set runtime values using the [configuration reference](configuration.md).
- Read [security and operations](operations/security.md) before exposing HTTP beyond loopback.
- Use the [development guide](development.md) and [testing guide](testing.md) before contributing.
