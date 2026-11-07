#!/usr/bin/env python3
"""Read-only structural checks for this Python MCP server monorepo."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQUIRED_PATHS = (
    "pyproject.toml",
    "uv.lock",
    "apps/example-server/pyproject.toml",
    "apps/example-server/src/mcp_example_server/server.py",
    "libs/mcp-starter-core/pyproject.toml",
    "libs/mcp-starter-core/src/mcp_starter_core/config.py",
    "tests",
    "docs/architecture.md",
    "docs/operations/security.md",
    ".codex/config.toml",
    ".codex/hooks.json",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-lock",
        action="store_true",
        help="run the read-only `uv lock --check` consistency check",
    )
    args = parser.parse_args()

    failures = [path for path in REQUIRED_PATHS if not (ROOT / path).exists()]
    if failures:
        for path in failures:
            print(f"MISSING: {path}", file=sys.stderr)
        return 1

    print("MCP workspace structure: required app, core, tests, docs, and Codex files found")
    if args.check_lock:
        try:
            result = subprocess.run(
                ["uv", "lock", "--check"],
                cwd=ROOT,
                check=False,
                text=True,
            )
        except FileNotFoundError:
            print("ERROR: uv is not installed or not on PATH", file=sys.stderr)
            return 2
        return result.returncode
    print("Lockfile check skipped; pass --check-lock to run `uv lock --check`.")
    print("This doctor does not install packages, modify files, run tests, or contact services.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
