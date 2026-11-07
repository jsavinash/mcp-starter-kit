# Validation recipe

Use the narrowest checks that cover the change, then run broader checks when relevant. These commands are documented by the repository's root `Makefile` and `pyproject.toml`.

## Setup

```bash
uv sync --all-packages
```

## Checks

```bash
make lint
make format-check
make typecheck
make test
make security
make docs
```

Run `make docker-build` when the container or runtime packaging changed. Run `make run-stdio` or `make run-http` for a manual startup check when a change affects server composition, CLI, transport, or lifecycle. HTTP remote-bind behavior requires valid OAuth introspection settings and a host allowlist; do not weaken these settings to make a local check pass.

## Selection and reporting

- For docs-only changes, review links and formatting; do not run the full Python suite without a reason.
- For package/config changes, include workspace sync/lock consistency and relevant checks.
- For tool/resource/prompt behavior, run focused tests and then the full suite when practical.
- For auth, HTTP security, or lifecycle changes, cover negative cases and boundary conditions explicitly.
- Report each command run with its actual result. List skipped checks and explain why. A command that was not run must not be described as passing.
- Do not automatically fix unrelated failures or rewrite the lockfile without a dependency change.
