"""MCP lifespan utilities for shared async infrastructure."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import structlog
from mcp.server import MCPServer

from mcp_starter_core.auth import OAuthIntrospectionVerifier


@asynccontextmanager
async def server_lifespan(
    _server: MCPServer[Any], *, verifier: OAuthIntrospectionVerifier | None = None
) -> AsyncIterator[dict[str, str]]:
    """Own process-wide clients and close them cleanly when the server stops."""
    log = structlog.get_logger(__name__)
    log.info("mcp.server.starting")
    try:
        if verifier is None:
            yield {"service": "mcp-example-server"}
        else:
            async with verifier.lifespan():
                yield {"service": "mcp-example-server"}
    finally:
        log.info("mcp.server.stopping")
