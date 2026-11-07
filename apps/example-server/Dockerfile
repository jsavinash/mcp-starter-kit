FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS build
WORKDIR /workspace
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./
COPY apps/example-server/pyproject.toml apps/example-server/pyproject.toml
COPY libs/mcp-starter-core/pyproject.toml libs/mcp-starter-core/pyproject.toml
RUN uv sync --frozen --no-dev --package mcp-example-server --no-install-workspace

COPY apps/example-server/src apps/example-server/src
COPY libs/mcp-starter-core/src libs/mcp-starter-core/src
RUN uv sync --frozen --no-dev --package mcp-example-server

FROM python:3.12-slim-bookworm AS runtime
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
RUN useradd --system --uid 10001 --create-home mcp
COPY --from=build --chown=10001:10001 /workspace/.venv /app/.venv
USER 10001:10001
ENTRYPOINT ["mcp-example-server"]
