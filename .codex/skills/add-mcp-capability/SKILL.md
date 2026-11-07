---
name: add-mcp-capability
description: Design and implement a tool, resource, or prompt in this Python MCP server monorepo while preserving SDK, architecture, security, and test boundaries.
---

# Add an MCP capability

1. Read `apps/example-server/AGENTS.md`, `.codex/plans/add_mcp_capability.md`, and the relevant official MCP/SDK docs if protocol behavior is version-sensitive.
2. Confirm the operation belongs in the example app or a reusable core service. Capability registration belongs in a focused module under `apps/example-server/src/mcp_example_server/features/`; register once in `server.py`.
3. Define names/descriptions and typed bounded input/output schemas. Make side effects, authorization, errors, cache scope, idempotency, timeout, and output-size expectations explicit.
4. Keep handler logic thin. Place domain behavior and external I/O in a service when needed; use lifespan-managed clients and dependency injection.
5. Use SDK errors appropriate to the contract. Never turn an expected failure into a successful-looking string or expose tracebacks/upstream payloads.
6. Add tests for successful calls, input/error behavior, authorization or privacy boundaries, and relevant legacy/modern client behavior.
7. Update documentation and run the checks selected by `.codex/skills/validation.md`.

Do not advertise extensions until implemented and negotiated. Do not use public shared caching for caller-specific results.
