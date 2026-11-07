# Scope and non-goals

## In scope

- A reusable Python monorepo pattern for multiple MCP services.
- The official Python `mcp` SDK, with the supported major/API choice documented centrally.
- Secure local stdio and remote-capable Streamable HTTP examples.
- Shared infrastructure that genuinely has multiple app consumers or a stable cross-app contract.
- Tools, resources, prompts, configuration, tests, packaging, CI, containerization, and operational docs.
- Optional capabilities added behind explicit configuration and protocol negotiation where required.

## Non-goals unless a concrete use case is approved

- Building an identity provider, login UI, or token issuer. The server is a resource server.
- Shipping a database or migration framework before a persistence feature exists.
- Supporting every experimental MCP extension in the starter by default.
- Making the server an unrestricted shell, filesystem, browser, or arbitrary URL proxy.
- Hiding app-specific domain logic in the shared core package.
- Supporting SDK v1 `FastMCP` and SDK v2 `MCPServer` simultaneously in production code.
- Claiming conformance, security certification, or production readiness based only on a template or a passing unit suite.
- Reintroducing unrelated web frontend, education, or generic app starter content without a clear MCP project reason.
