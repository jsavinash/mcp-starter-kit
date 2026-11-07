---
name: code-change-verification
description: Select and run repository checks for Python, MCP protocol, configuration, documentation, dependency, and container changes. Use before reporting implementation work complete.
---

# Code change verification

1. Read the root and nearest nested `AGENTS.md`, then inspect the changed files and their tests.
2. Select checks from `../../skills/validation.md`; match checks to the changed surface. Do not run unrelated expensive commands by default.
3. For MCP capability changes, verify handler behavior and schemas through the official SDK client where possible. For auth/HTTP changes, include failure and boundary cases using local fakes; never require production credentials.
4. Run the chosen commands and inspect all output/exit statuses. Do not edit unrelated files to silence failures.
5. Review the diff for secrets, accidental generated artifacts, incorrect cache scope, unsafe public defaults, and docs drift.
6. Report exact commands, outcomes, skipped checks/reasons, and residual risks. Never convert “not run” into “passed.”

## Current commands

- `uv run ruff check .`
- `uv run ruff format --check .`
- `uv run mypy apps libs main.py`
- `uv run pytest -q`
- `uv run pip-audit`
- `uv run --group docs mkdocs build --strict`
- `uv build --all-packages`
- `docker build -f apps/example-server/Dockerfile -t mcp-example-server:local .`
