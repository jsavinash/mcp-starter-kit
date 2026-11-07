# MCP Starter Kit documentation

This site documents the current repository: a Python `uv` monorepo with an example MCP server, shared core library, CI, container template, and Codex project workflows.

## Start here

- [Getting started](getting-started.md) — install and run the server.
- [Project structure](project-structure.md) — package boundaries and entry points.
- [Architecture and MCP protocol](architecture.md) — protocol baseline and design decisions.
- [Configuration reference](configuration.md) — all current `MCP_*` settings.

## Build and operate

- [Example capabilities](capabilities.md)
- [Transports and entry points](transports.md)
- [Security and operations](operations/security.md)
- [Deployment](operations/deployment.md)
- [Development guide](development.md)
- [Testing and CI](testing.md)
- [Troubleshooting](troubleshooting.md)
- [Python package reference](api-reference.md)
- [Codex project setup](codex.md)

## Project scope

The example is a starter, not a fully tested production deployment. The visible automated test suite currently covers only the legacy root helper. Review [Testing and CI](testing.md) for the present coverage and recommended test plan, and complete the deployment/security review for your actual environment.
