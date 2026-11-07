# Definitions and project contracts

## Workspace terms

| Term | Definition |
|---|---|
| App | A deployable MCP server under `apps/`, with its own package metadata and composition root. |
| Core library | Reusable infrastructure under `libs/mcp-starter-core`; it must not own app-specific business behavior. |
| Feature | A cohesive MCP capability such as tools, resources, or prompts, registered at the app edge. |
| stdio | Local process transport intended for an MCP host that launches the server. stdout is reserved for protocol traffic. |
| Streamable HTTP | The supported remote-capable HTTP transport, served locally at `/mcp`; public deployment requires auth and host controls. |

## Current stack

- Python: `>=3.11` (root `pyproject.toml`)
- Workspace/dependency manager: `uv`
- MCP library: official `mcp` Python package, v2 major line
- Quality tools: Ruff, MyPy, Pytest, pip-audit, MkDocs
- Current demo package: `mcp-example-server`

The repository's architecture documentation is the authority for exact MCP specification version and SDK API decisions. Update that document when they change.

## Runtime and security contracts

- Environment configuration is parsed and validated by the shared core settings layer.
- Remote authorization uses OAuth 2.0 access-token verification through RFC 7662 introspection where configured; bearer tokens must never be logged.
- HTTP bind host/origin controls and request size limits remain enabled. Public exposure must be explicitly configured.
- Keep secrets outside committed files. `.env.example` contains placeholders only.
- MCP tools must have bounded inputs, predictable outputs, and clear recoverable errors. Do not imply that a read-only operation is side-effect free unless its implementation guarantees that.

## Source-of-truth map

- Project shape and architecture: `ARCHITECTURE.md`, `docs/architecture.md`
- Operational security: `docs/operations/security.md`
- Contribution and local commands: `CONTRIBUTING.md`, `Makefile`
- Environment variables: `.env.example`
