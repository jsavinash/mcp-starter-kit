# Project acceptance criteria

Use these criteria for reviewing a material project change. Tailor them to each feature; they are not a requirement to run every check for every docs-only edit.

## Architecture

- Code is owned by the correct app or shared library and dependency direction remains app → core → SDK.
- Startup/transport side effects remain outside import-time business modules where practical.
- Configuration is typed, documented, validated at startup, and has a safe default.

## MCP behavior

- Tool/resource/prompt names, descriptions, input/output schemas, errors, and side effects are explicit.
- Modern and legacy behavior is intentional and follows the supported SDK API; protocol code is not reimplemented unnecessarily.
- Public cache metadata is used only when data is identical across all authorized callers.
- Extensions are negotiated and advertised only when implemented.

## Security and reliability

- Remote HTTP remains protected by OAuth verification and host/origin controls; secrets and bearer tokens do not appear in output or telemetry.
- Inputs, request bodies, outputs, network calls, retries, and concurrency have appropriate bounds.
- Mutations have authorization and defined idempotency/retry semantics.
- Resources and upstream responses are treated as untrusted content.
- Lifespan-managed dependencies are closed deterministically.

## Delivery evidence

- Tests cover changed behavior and important negative/security cases.
- Relevant lint, format, type, test, packaging, docs, or container checks have actual recorded outcomes.
- User/developer docs match effective configuration and do not promise unverified behavior.
