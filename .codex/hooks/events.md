# Codex hook event catalogue

Codex currently documents these lifecycle events. The project enables only events with a useful, bounded action for this repository; adding a hook to every event would create noise, latency, privacy exposure, or continuation loops.

| Event | Project decision | Reason |
|---|---|---|
| `SessionStart` | Enabled | Restore concise repo/security context on startup, resume, clear, fork, and after compaction. |
| `SessionEnd` | Omitted | The repo has no hook-owned process or persistent session state to clean up. |
| `UserPromptSubmit` | Enabled | Route MCP/auth/test/deployment requests to project references without logging prompt text. |
| `PreToolUse` | Enabled for `Bash` | Add advisory context for a small set of high-impact destructive command patterns; never auto-deny or grant permission. |
| `PermissionRequest` | Enabled for `Bash` | Add risk context while preserving Codex's normal user approval decision. |
| `PostToolUse` | Enabled for file edits | Flag follow-up review when edits touch auth, configuration, transport, server entry points, or deployment files. |
| `PreCompact` | Omitted | No project state needs to be saved; can allow normal compaction behavior. |
| `PostCompact` | Omitted | `SessionStart` with source `compact` already restores bounded context. |
| `SubagentStart` | Enabled | Give parallel work the same app/core boundaries and evidence requirements. |
| `SubagentStop` | Omitted | Automatic continuation can loop; the parent task should assess the returned result. |
| `Stop` | Omitted | Enforcing completion by restarting turns can loop and cannot reliably assess natural-language claims. |
| `Interrupt` | Omitted | No hook-managed child process or temporary state needs interruption cleanup. |
| `PreModelRequest` | Omitted | No model request policy is required, and request hooks can expose sensitive prompt data. |
| `PostModelRequest` | Omitted | Token/error telemetry is not part of this repo; avoid capturing private prompt or response metadata. |

Codex also supports `mcp_tool` hook handlers, which call an already-connected MCP server. This project has no scanner/quality MCP service and keeps its local example MCP server disabled by default, so no MCP tool hook is registered.

This catalogue reflects the [current Codex hooks reference](https://developers.openai.com/codex/hooks/) checked on 2026-11-07. Recheck it before adding an event or relying on a hook output field.
