# Project Codex hooks

`../hooks.json` configures Codex lifecycle hooks for this MCP monorepo. The scripts use only Python's standard library. They do not persist prompt text, transcripts, tool arguments, credentials, or outputs.

See [the event catalogue](events.md) for the full current Codex lifecycle event list and why this project enables or omits each event.

## Enabled hooks

| Event | Project behavior |
|---|---|
| `SessionStart` | Adds a short workspace map and reminds the agent to preserve user changes on startup, resume, clear, fork, or compact. |
| `UserPromptSubmit` | Adds links to relevant MCP/security/validation/deployment guidance based on prompt keywords; it does not save the prompt. |
| `PreToolUse` (`Bash`) | Adds an advisory for a small set of destructive command patterns. It does not block or approve commands. |
| `PermissionRequest` (`Bash`) | Adds a warning for risky patterns and leaves the normal Codex approval decision to the user. |
| `PostToolUse` (file edits) | Reminds the agent to review focused security cases after edits to auth, configuration, transport, app entry points, or deployment files. It does not run tests. |
| `SubagentStart` | Passes package-boundary and evidence-reporting instructions to a subagent. |

## Deliberately not configured

The repo has no session-owned background process or temp state to clean up, so it does not need `SessionEnd` or `Interrupt` scripts. `Stop` and `SubagentStop` continuation hooks can create repeated turns; CI and explicit validation instructions are a better fit here. `PreModelRequest`/`PostModelRequest` could capture sensitive prompts and token-use metadata, so they are excluded. `PreCompact` does not write memory or alter compaction. Context restoration runs from `SessionStart` with source `compact`. `PostToolUse` does not auto-run the test suite after every edit. No `mcp_tool` hook is configured because the example MCP server is disabled by default and no scanner server is part of the project.

## Safety and trust

- Project hooks load only when the `.codex/` project layer is trusted and Codex has reviewed the exact hook definitions. Review changed hooks in Codex before trusting them.
- Hooks are defense-in-depth, not a security boundary. Pre-tool failures/timeouts can allow an operation to proceed; use Codex permissions, sandboxing, CI, and normal user review for enforcement.
- The permission hook makes no allow/deny decision. It never auto-approves an escalation.
- Hook handlers must remain fast, deterministic, local, and safe with malformed/missing input. Keep output concise and never print secrets.

## Run and validate manually

```bash
python3 .codex/hooks/dispatch.py <<'JSON'
{"hook_event_name":"SessionStart","source":"startup"}
JSON

python3 .codex/scripts/validate_codex.py
python3 .codex/scripts/project_doctor.py
```

Run `python3 .codex/scripts/project_doctor.py --check-lock` to also run the read-only `uv lock --check` command.
