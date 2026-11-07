# Codex project kit

This directory contains project-local Codex configuration, durable guidance, architecture research, repeatable workflows, and templates. It complements the root and nested `AGENTS.md` files; it does not replace them.

## Start here

| Need | Read |
|---|---|
| Understand repository layout and current gaps | [Project structure research](research/project_structure.md) |
| Review MCP protocol and SDK assumptions | [MCP baseline](research/mcp_spec_baseline.md) |
| Understand goals and project vocabulary | `goals/`, `definitions.md` |
| Plan work or change architecture | `plans/` |
| Review or debug changes | `prompts/` |
| Run a repeatable workflow | `skills/` |
| Start an ADR, feature spec, or incident record | `templates/` |
| Understand or validate Codex hooks and scripts | `hooks/README.md`, `scripts/`, and [the docs page](../docs/codex.md) |

## Guidance hierarchy

1. System/developer/user instructions for the active task.
2. Root `AGENTS.md`, then the nearest app/library `AGENTS.md`.
3. Relevant architecture, security, goal, and workflow references in this directory.
4. Current official MCP/SDK documentation when protocol behavior or an SDK surface may have changed.

Do not load every file for every task. Select only the files relevant to the code being changed. Markdown files in `.codex/skills/` are reusable workflow documentation; packaged `SKILL.md` folders are the discoverable skill form.

## Status discipline

Research describes the observed repository at the time it was written. Plans are proposed unless marked active. A checklist is not evidence of completion. Update status and evidence when implementation work actually occurs. Keep credentials and private production details out of this directory.
