# Plan template: MCP specification or SDK upgrade

Use this before changing the `mcp` major range, protocol revision, capability API, or advertised extension behavior.

## Discovery

- Current SDK version/constraint and lockfile resolution:
- Current protocol target:
- Proposed SDK/protocol target and official release notes:
- Breaking/deprecated API and wire changes:
- Compatibility promises for old MCP clients:
- Security/auth/transport/cache changes:

## Migration map

| Surface | Current behavior/API | Proposed behavior/API | Required action | Test evidence |
|---|---|---|---|---|
| Server API | | | | |
| Client/transport | | | | |
| Auth | | | | |
| Tools/resources/prompts | | | | |
| Extensions | | | | |
| Packaging/deployment | | | | |

## Safe sequence

1. Read normative spec and official SDK migration documentation; do not rely on blog summaries alone.
2. Pin the target SDK range and update the lockfile through `uv`.
3. Migrate app/core imports and call signatures as a cohesive change.
4. Add compatibility tests for every connection era/client version the project claims to support.
5. Verify HTTP headers, cache metadata, auth metadata, and error semantics at the wire boundary.
6. Update architecture/security docs, README, examples, and release notes.
7. Run full quality, test, package, and transport checks; record unsupported cases.

## Exit criteria

No mixed SDK API generation remains; the selected protocol behavior is verified; compatibility claims have evidence; deployment security has been re-reviewed.
