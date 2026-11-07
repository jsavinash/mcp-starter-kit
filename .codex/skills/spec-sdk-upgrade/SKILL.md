---
name: mcp-spec-sdk-upgrade
description: Plan or perform an MCP specification or official Python SDK upgrade, including API migration, transport/auth compatibility, and protocol-level regression coverage.
---

# MCP specification and SDK upgrade

1. Read `.codex/plans/sdk_upgrade.md` and `.codex/research/mcp_spec_baseline.md`.
2. Browse the normative MCP spec and official Python SDK release/migration docs for the proposed target. Do not use third-party summaries for normative behavior.
3. Inventory imports and surfaces across apps, core, tests, docs, examples, CI, packaging, and deployment.
4. Produce a before/after migration map for server API, protocol lifecycle, transport headers/session behavior, authorization, errors, cache metadata, extensions, and peer compatibility.
5. Update dependency constraints and regenerate `uv.lock` through `uv`; do not hand-edit the lock.
6. Migrate code in a focused patch and add wire/client tests for the target revision and each compatibility mode the project promises.
7. Update the research snapshot with check date and primary source links, then update user-facing docs.
8. Run full relevant verification and report compatibility limits and unverified behavior.

Do not broaden supported versions accidentally or advertise a new extension as part of the core protocol.
