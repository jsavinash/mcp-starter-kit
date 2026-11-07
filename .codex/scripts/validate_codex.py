#!/usr/bin/env python3
"""Validate the project-specific Codex config, hooks, skills, and local Markdown links."""

from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CODEX = ROOT / ".codex"
KNOWN_EVENTS = {
    "SessionStart",
    "SessionEnd",
    "UserPromptSubmit",
    "PreToolUse",
    "PermissionRequest",
    "PostToolUse",
    "PreCompact",
    "PostCompact",
    "SubagentStart",
    "SubagentStop",
    "Stop",
    "Interrupt",
    "PreModelRequest",
    "PostModelRequest",
}


def validate() -> list[str]:
    errors: list[str] = []
    config_path = CODEX / "config.toml"
    hooks_path = CODEX / "hooks.json"
    try:
        tomllib.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        errors.append(f"Invalid Codex TOML ({config_path.relative_to(ROOT)}): {exc}")

    try:
        hooks_doc = json.loads(hooks_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Invalid hook JSON ({hooks_path.relative_to(ROOT)}): {exc}")
        hooks_doc = {}

    hooks = hooks_doc.get("hooks", {}) if isinstance(hooks_doc, dict) else {}
    if not isinstance(hooks, dict):
        errors.append("hooks.json must contain a hooks object")
        hooks = {}

    for event, groups in hooks.items():
        if event not in KNOWN_EVENTS:
            errors.append(f"Unknown Codex hook event: {event}")
            continue
        if not isinstance(groups, list):
            errors.append(f"Hook event {event} must contain a list of matcher groups")
            continue
        for group in groups:
            if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
                errors.append(f"Hook event {event} has a malformed matcher group")
                continue
            for handler in group["hooks"]:
                if not isinstance(handler, dict) or handler.get("type") != "command":
                    errors.append(f"Hook event {event} must use a command handler")
                    continue
                command = handler.get("command", "")
                if ".codex/hooks/dispatch.py" not in command:
                    errors.append(f"Hook event {event} does not point to the project dispatcher")
                if not (CODEX / "hooks/dispatch.py").is_file():
                    errors.append("Missing .codex/hooks/dispatch.py")
                timeout = handler.get("timeout", 600)
                if not isinstance(timeout, (int, float)) or timeout <= 0 or timeout > 600:
                    errors.append(f"Hook event {event} has an invalid timeout")

    for skill_path in sorted((CODEX / "skills").rglob("SKILL.md")):
        body = skill_path.read_text(encoding="utf-8")
        frontmatter = re.match(r"\A---\s*\n(.*?)\n---\s*\n", body, re.S)
        if frontmatter is None:
            errors.append(f"Skill is missing YAML frontmatter: {skill_path.relative_to(ROOT)}")
            continue
        metadata = frontmatter.group(1)
        for field in ("name", "description"):
            if not re.search(rf"^{field}:\s*\S", metadata, re.M):
                errors.append(f"Skill lacks {field}: {skill_path.relative_to(ROOT)}")

    link_pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    for markdown in sorted(CODEX.rglob("*.md")):
        for target in link_pattern.findall(markdown.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            local_target = (markdown.parent / target.split("#", 1)[0]).resolve()
            if not local_target.exists():
                errors.append(
                    f"Broken local link in {markdown.relative_to(ROOT)}: {target}"
                )
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    hook_events = json.loads((CODEX / "hooks.json").read_text(encoding="utf-8"))["hooks"]
    skills = list((CODEX / "skills").rglob("SKILL.md"))
    print(f"Codex project files valid: {len(hook_events)} hook events, {len(skills)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
