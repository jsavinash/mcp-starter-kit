---
name: release-readiness
description: Prepare a reviewable release of this Python MCP workspace by checking versions, locked dependencies, package artifacts, docs, CI evidence, and security/deployment notes.
---

# Release readiness

1. Confirm the intended release scope and supported app/library packages. This repository's release policy may still need to be chosen; do not invent publishing credentials or publish automatically.
2. Inspect git status and diff; preserve unrelated user changes. Review version metadata, changelog/release notes, README, docs navigation, and migration notes.
3. Confirm dependency changes are reflected in `uv.lock`; verify workspace sync with `--locked`.
4. Run relevant lint, formatting, type, test, audit, documentation, and package build checks from `.codex/skills/validation.md`.
5. Build the container if runtime packaging changed. Inspect image entrypoint, user, environment, filesystem/network assumptions, and compose exposure.
6. Confirm OAuth/security docs, supported Python versions, SDK/spec baseline, and compatibility statements are accurate.
7. Report blockers, exact check evidence, artifact names, and release notes required. Do not tag, publish, deploy, or push unless separately authorized.
