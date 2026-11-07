# Testing and CI

## Local commands

```bash
make lint
make format-check
make typecheck
make test
make security
make docs
```

Run the relevant subset for a focused change. For app startup or transport changes, also run a local stdio/HTTP smoke check. Do not point test or smoke commands at a production identity provider or service.

## Current coverage status

At the time this guide was written, the visible root test suite contains `tests/test_main.py`, which tests only the compatibility helper `main.build_welcome_message()`. It does not yet provide visible tests for the MCP tool/resource/prompt handlers, server composition, settings validation, OAuth introspection verifier, lifecycle cleanup, HTTP host/origin protections, CLI transport selection, or ASGI behavior.

The examples in this repository describe intended behavior, but the missing app/core tests mean that behavior is not fully demonstrated by automated tests today. Treat this as a starter-suite gap, not an assurance of protocol or security conformance.

## Recommended coverage for new behavior

- **Capabilities:** exercise through the official SDK client; cover success, invalid input, expected errors, unknown resources/prompts, and output schemas.
- **Configuration:** test defaults, `.env` and environment parsing, bounds, malformed URLs, HTTPS rules, auth completeness, and rejection of non-loopback unauthenticated binds.
- **Verifier:** use a local mocked HTTP transport for inactive, malformed, expired, wrong-resource, bad-scope, timeout, redirect, and valid claims. Assert logs never include the raw bearer token or provider response body.
- **HTTP boundary:** test allowed/disallowed host and origin behavior and request-body limits; do not assume in-process SDK tests exercise HTTP middleware.
- **Lifecycle/CLI:** verify client setup/cleanup and transport selection without opening public listeners.
- **Cache:** assert shared/public hints only for caller-invariant data.

These are recommendations for future tests; they are not currently present.

## CI workflow

`.github/workflows/ci.yml` runs on pushes and pull requests targeting `main`, plus manual dispatch. It has three jobs:

1. **quality** on Python 3.12: locked workspace sync, Ruff lint/format check, strict MyPy, pip-audit, and `uv build --all-packages`.
2. **test** matrix on Python 3.11, 3.12, and 3.13: locked workspace sync and `pytest -q`.
3. **docker** after quality and test succeed: build the example image without pushing it.

The workflow has read-only `contents` permissions and cancels older runs for the same ref. MkDocs build, live transport interoperability, OAuth provider integration, and deployment validation are not currently visible CI steps.

## Interpreting results

A passing lint/type/test job is not MCP conformance or deployment certification. Report checks actually executed, distinguish skipped checks, and state when network/IdP/proxy behavior was not exercised.
