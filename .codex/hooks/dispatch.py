#!/usr/bin/env python3
"""Small, privacy-preserving dispatcher for this MCP monorepo's Codex hooks."""

from __future__ import annotations

import json
import re
import sys
from typing import Any


PROJECT_CONTEXT = (
    "Project: Python 3.11+ uv monorepo. Deployable MCP apps are under apps/; reusable "
    "configuration, OAuth verification, lifecycle, logging, and HTTP security belong in "
    "libs/mcp-starter-core. Current server uses the official MCP Python SDK v2 API (MCPServer), "
    "stdio and Streamable HTTP. Check docs/architecture.md and docs/operations/security.md "
    "for protocol and remote deployment constraints. Preserve existing user changes."
)

ROUTING = (
    (
        re.compile(r"\b(auth|oauth|token|issuer|audience|scope|security|host|origin|ssrf)\b", re.I),
        "Relevant project references: docs/operations/security.md, "
        ".codex/prompts/security_review.md, and libs/mcp-starter-core/AGENTS.md.",
    ),
    (
        re.compile(r"\b(mcp|protocol|sdk|transport|streamable|stdio|extension|cache)\b", re.I),
        "Relevant project references: docs/architecture.md and "
        ".codex/research/mcp_spec_baseline.md. Check current official spec/SDK docs for "
        "version-sensitive behavior.",
    ),
    (
        re.compile(r"\b(test|tests|lint|typecheck|format|validation|ci|pytest)\b", re.I),
        "Relevant project recipe: .codex/skills/validation.md. Report only checks actually run.",
    ),
    (
        re.compile(r"\b(deploy|deployment|production|docker|compose|remote|http)\b", re.I),
        "Relevant project references: docs/operations/security.md and "
        ".codex/plans/deployment_review.md. Remote binds require configured OAuth and an "
        "explicit host allowlist.",
    ),
    (
        re.compile(r"\b(add|create|new)\b.{0,35}\b(server|app|tool|resource|prompt|capability)\b", re.I),
        "Keep registrations in apps/<service>/features and wire them from the app composition "
        "root. See .codex/plans/add_mcp_capability.md or the add-server-app skill.",
    ),
)

RISKY_COMMANDS = (
    (re.compile(r"\bgit\s+reset\s+--hard\b", re.I), "hard git reset"),
    (re.compile(r"\bgit\s+clean\b[^\n]*(?:\s-[a-z]*f|\s--force)", re.I), "forced git clean"),
    (re.compile(r"\bgit\s+push\b[^\n]*(?:--force(?:-with-lease)?|-f\b)", re.I), "force push"),
    (re.compile(r"\brm\s+(?:-[^\n]*r[^\n]*f|-[^\n]*f[^\n]*r)\s+/(?:\s|$)", re.I), "root filesystem deletion"),
    (re.compile(r"\b(?:drop\s+database|truncate\s+table)\b", re.I), "destructive database operation"),
    (re.compile(r"\bdocker\s+compose\s+down\b[^\n]*\s-v(?:\s|$)", re.I), "volume deletion"),
    (re.compile(r"\bterraform\s+destroy\b|\bkubectl\s+delete\s+namespace\b", re.I), "infrastructure deletion"),
)

SECURITY_FILE = re.compile(
    r"(?:mcp_starter_core/(?:auth|config|transport|lifecycle)\.py|"
    r"mcp_example_server/(?:server|http_app|cli)\.py|Dockerfile|docker-compose\.yml|"
    r"docs/operations/security\.md)"
)


def _emit(payload: dict[str, Any] | None) -> None:
    if payload:
        sys.stdout.write(json.dumps(payload, separators=(",", ":")) + "\n")


def _additional_context(event: str, text: str) -> dict[str, Any]:
    return {
        "hookSpecificOutput": {
            "hookEventName": event,
            "additionalContext": text,
        }
    }


def _risky_reason(command: str) -> str | None:
    for pattern, label in RISKY_COMMANDS:
        if pattern.search(command):
            return label
    return None


def handle(payload: dict[str, Any]) -> dict[str, Any] | None:
    event = payload.get("hook_event_name")
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        tool_input = {}

    if event == "SessionStart":
        return _additional_context(event, PROJECT_CONTEXT)

    if event == "SubagentStart":
        return _additional_context(
            event,
            "Subtask boundaries: preserve app/core ownership, inspect relevant AGENTS.md files, "
            "do not overwrite unrelated user changes, and report evidence and checks precisely. "
            + PROJECT_CONTEXT,
        )

    if event == "UserPromptSubmit":
        prompt = payload.get("prompt")
        if not isinstance(prompt, str) or not prompt:
            return None
        matched = [guidance for pattern, guidance in ROUTING if pattern.search(prompt)]
        if not matched:
            return None
        # Prompt text is used only in memory for keyword routing and is never written to disk.
        return _additional_context(event, " ".join(dict.fromkeys(matched)))

    if event in {"PreToolUse", "PermissionRequest"} and payload.get("tool_name") == "Bash":
        command = tool_input.get("command")
        if not isinstance(command, str):
            return None
        reason = _risky_reason(command)
        if reason is None:
            return None
        message = (
            f"The command appears to include {reason}. Inspect its exact target and scope, "
            "preserve user data, and follow the normal Codex approval flow. This project hook "
            "is advisory and does not grant permission."
        )
        if event == "PreToolUse":
            return {
                "hookSpecificOutput": {
                    "hookEventName": event,
                    "additionalContext": message,
                }
            }
        # No decision means Codex retains its normal user approval prompt.
        return {"systemMessage": message}

    if event == "PostToolUse" and payload.get("tool_name") in {"apply_patch", "Edit", "Write"}:
        patch_text = tool_input.get("command")
        if isinstance(patch_text, str) and SECURITY_FILE.search(patch_text):
            return {
                "hookSpecificOutput": {
                    "hookEventName": event,
                    "additionalContext": (
                        "This edit may affect MCP auth, transport, server composition, or container "
                        "security. Review negative cases and update security docs; run focused "
                        "checks before claiming verification."
                    ),
                }
            }

    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return 0
    if not isinstance(payload, dict):
        return 0
    try:
        _emit(handle(payload))
    except Exception:
        # Hooks are advisory. A dispatcher error must not break an unrelated tool call.
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
