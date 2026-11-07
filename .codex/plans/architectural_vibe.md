# Architectural guidelines

## Shape

- Use a modular monorepo: deployable services under `apps/`, reusable cross-service infrastructure under `libs/`.
- Keep app composition at the edge. Feature modules define capability behavior; server setup binds features, settings, dependencies, and lifecycle.
- Keep domain behavior independent of MCP transport details where practical. Translate domain results/errors into MCP contracts in the feature or adapter layer.
- Prefer explicit dependency injection and typed settings over hidden global state.

## Boundaries

- `apps/example-server` owns its CLI, ASGI app, composition root, and example capabilities.
- `libs/mcp-starter-core` owns reusable settings, auth, lifecycle, logging, and transport security.
- Avoid importing app code from the core library or coupling one app to another app's internals.
- Avoid premature plugin registries or abstractions for one implementation. Add an abstraction when there are multiple real consumers or a clear stable contract.

## MCP design

- Advertise only capabilities implemented and supported by the selected SDK/spec target.
- Give tools focused names, descriptions, bounded typed inputs, stable outputs, and explicit side-effect behavior.
- Model resources as addressable context and prompts as user-invoked templates; do not disguise actions as either.
- Preserve cancellation, progress, request metadata, and lifecycle semantics provided by the SDK rather than reimplementing protocol dispatch.
- Use Streamable HTTP for new HTTP deployments; treat legacy SSE as compatibility-only.

## Production posture

- Secure defaults, least privilege, bounded resource use, structured diagnostics, and deterministic shutdown.
- Never emit secrets or bearer tokens in logs, tool output, or errors.
- Public network exposure requires authentication and explicit host/origin controls.
- Optional capabilities must remain opt-in and documented; fail closed on incomplete security configuration.
