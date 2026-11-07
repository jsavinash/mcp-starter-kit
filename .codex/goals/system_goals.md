# System goals

## Project purpose

Provide a secure, maintainable Python monorepo starter for building MCP servers with the official Python SDK, `uv`, and a reusable core library.

## Active goals

These are ongoing project goals, not a claim that every item is complete. Track implementation status in pull requests and the repository issue tracker.

1. Keep the example server runnable over stdio and Streamable HTTP.
2. Keep shared configuration, lifecycle, logging, OAuth resource-server support, and HTTP hardening in `libs/mcp-starter-core`.
3. Demonstrate MCP tools, resources, and prompts with typed inputs and safe error behavior.
4. Maintain a reproducible workspace and lockfile, CI checks, container build, and operator documentation.
5. Keep remote HTTP deployment fail-closed: require configured authentication and explicit host allowlisting.
6. Track changes to the MCP specification and official Python SDK; document compatibility and migration choices before changing the SDK major version or advertised capabilities.
7. Add production features as opt-in modules with explicit configuration, tests, and security documentation; avoid speculative defaults.

## Completion criteria for a feature

- The feature has a clear owner module and documented configuration.
- Public MCP behavior is covered by tests and described in the docs.
- Security, transport, errors, lifecycle, and observability implications are addressed.
- Relevant quality checks pass, or remaining failures are reported with evidence.
