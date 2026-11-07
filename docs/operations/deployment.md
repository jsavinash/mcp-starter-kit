# Deployment guide

This page describes the deployment surfaces present in the repository and the controls that must be supplied by a real hosting environment. The repo provides a container build and a protected local Compose template; it does not include a cloud deployment manifest, IdP setup, TLS proxy, rate limiter, or production health check.

## Choose a deployment surface

- Use **stdio** for local MCP hosts that launch the process.
- Use **Streamable HTTP** with the CLI for a direct listener or **ASGI** under a server such as Uvicorn for an ASGI platform.
- Use the included Dockerfile when deploying the example container.

See [Transports](../transports.md) for entry point commands.

## Container image

Build from the repository root:

```bash
docker build -f apps/example-server/Dockerfile -t mcp-example-server:local .
```

The multi-stage build uses `uv` to install the locked `mcp-example-server` workspace package and its runtime dependencies, then copies the virtual environment into a Python 3.12 slim runtime image. The runtime executes as UID 10001, uses an exec-form entrypoint, and sets unbuffered/no-bytecode Python environment flags.

The Dockerfile itself does not declare a health check, TLS, OAuth provider, public host allowlist, rate limit, or egress policy. Add those at the platform/proxy layer and maintain parity with the security guide.

## Docker Compose template

The current Compose service:

- builds the image locally from the example Dockerfile;
- reads `.env` and forces `MCP_TRANSPORT=streamable-http`, `MCP_HOST=0.0.0.0`;
- publishes container port 8000 only on host `127.0.0.1`;
- uses a read-only root filesystem, a 16 MiB no-exec/no-suid `/tmp`, drops Linux capabilities, enables `no-new-privileges`, and restarts unless stopped.

Run with:

```bash
cp .env.example .env
docker compose up --build
```

As copied, the `.env.example` defaults are not sufficient for the forced non-loopback container bind: application startup fails closed until OAuth introspection values and a non-loopback allowed host are configured. In production, use a secret manager, a real TLS-enabled public resource URL, exact host/origin values, and a deployment-specific Compose/platform configuration. Host loopback port publishing is a local-only boundary and is not a substitute for remote deployment security.

## Reverse proxy and platform responsibilities

Configure and test at the trusted edge:

- TLS termination and strict upstream connectivity;
- exact routing to the MCP path while preserving required MCP headers;
- rate and concurrency limits, request/response timeouts, and connection budgets;
- egress controls and SSRF protections for any future URL-fetching capability;
- trusted proxy headers from known proxy IPs only;
- readiness/liveness, graceful process termination, resource limits, and log retention.

Do not add a generic `/health` MCP tool. Use platform process probes or a carefully isolated outer ASGI health route.

## OAuth prerequisites

The app validates access tokens as an OAuth resource server. The identity provider must issue tokens for the exact configured resource/audience and support the RFC 7662 introspection contract used by the adapter. The application does not provide login, consent, token issuance, client registration, or key rotation for the provider.

Complete [Security and operations](security.md) and a deployment-specific review before allowing public ingress. Confirm real provider claim shapes and scopes with a non-production integration environment.

## Rollout

The repository does not prescribe a release platform or automated rollout. Before production rollout, identify an owner, verify rollback, review compatibility with clients, ensure no app state assumes sticky sessions, and document how secrets and service identity are rotated. Protocol statelessness does not remove the need for durable shared storage when future app behavior stores workflow state.
