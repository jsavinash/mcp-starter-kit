# Codex project setup

This page explains the project-local Codex configuration and scripts in `.codex/`. These files are specific to this Python MCP monorepo: its `uv` workspace, example server, shared core, MCP SDK line, OAuth/HTTP boundaries, CI, and documentation.

## Directory map

| Path | Purpose |
|---|---|
| `.codex/config.toml` | Project-local reasoning, sandbox, approval, and disabled example MCP-server defaults. |
| `.codex/hooks.json` | Codex lifecycle hook event registrations. |
| `.codex/hooks/dispatch.py` | Standard-library hook dispatcher; routes relevant documentation and emits bounded reminders. |
| `.codex/scripts/validate_codex.py` | Checks Codex TOML/JSON, event names, local hook paths, skill metadata, and `.codex` local links. |
| `.codex/scripts/project_doctor.py` | Read-only monorepo structure check, with optional lockfile consistency check. |
| `.codex/AGENTS.md` | Consolidated Codex-specific project rules. |
| `.codex/goals/` | Project outcomes, definitions, non-goals, and acceptance criteria. |
| `.codex/plans/` | Reusable run, feature, deployment, and SDK upgrade plans. |
| `.codex/prompts/` | Review, triage, security, protocol research, and dependency prompts. |
| `.codex/skills/` | Reusable Codex workflows and command recipes. |
| `.codex/research/` | Dated repo analysis and protocol/SDK baseline. |
| `.codex/templates/` | ADR, feature specification, and incident templates. |

For an index and guidance hierarchy, see `.codex/README.md`. For the hooks' exact behavior and limitations, see `.codex/hooks/README.md`.
The current Codex lifecycle event inventory and project selection rationale are in `.codex/hooks/events.md`.

## Hooks configured for this project

The project configures session-start/resume/compaction context, prompt-based reference routing, advisory checks for a narrow set of destructive shell commands, permission-request warnings, post-edit reminders for security-sensitive modules, and subagent package-boundary guidance.

Hooks do not run tests or format files automatically. They do not store prompt/transcript data, grant permissions, or replace the regular Codex approval flow. Other lifecycle events are deliberately omitted when they have no useful project-specific action or would add telemetry, persistent state, or automatic turn continuation.

Codex loads project hooks only for a trusted `.codex/` layer and requires review/trust of non-managed hook definitions. Inspect and approve them through Codex's hooks UI/command before relying on them. Hooks are advisory and should not be treated as a complete policy enforcement boundary.

## Validate project Codex files

From the repository root:

```bash
python3 .codex/scripts/validate_codex.py
python3 .codex/scripts/project_doctor.py
python3 .codex/scripts/project_doctor.py --check-lock
```

The first checks config syntax and internal structure. The doctor verifies the expected MCP monorepo files and optionally runs `uv lock --check`. Neither script installs packages or contacts the MCP server or identity provider.

To inspect dispatcher output without starting Codex:

```bash
python3 .codex/hooks/dispatch.py <<'JSON'
{"hook_event_name":"SessionStart","source":"startup"}
JSON
```

## AGENTS.md consolidation

Keep project-specific Codex guidance consolidated under `.codex/AGENTS.md`; do not create extra root/app/library `AGENTS.md` copies. The guidance distinguishes `apps/` responsibilities from `libs/mcp-starter-core` responsibilities. If a tool only auto-loads an `AGENTS.md` at the repository root, point that tool to this file using its supported configuration rather than duplicating the instructions.

## Maintenance

- Recheck the hook schema against the current [Codex hooks documentation](https://developers.openai.com/codex/hooks/) before adding events or changing outputs.
- Keep the project-specific MCP version and SDK APIs aligned with [MCP architecture](architecture.md) and official upstream docs.
- Update `.codex/scripts/validate_codex.py` if the hook event schema or project file structure changes.
- Do not store secrets, personal data, transcript archives, or production configuration in `.codex/`.
