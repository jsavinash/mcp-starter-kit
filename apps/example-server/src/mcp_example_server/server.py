"""MCP server composition root."""

from __future__ import annotations

from functools import partial
from typing import Any

from mcp.server import CacheHint, MCPServer
from mcp.server.auth.settings import AuthSettings

from mcp_example_server import __version__
from mcp_example_server.features import calculator, catalog
from mcp_starter_core.auth import OAuthIntrospectionVerifier
from mcp_starter_core.config import Settings, get_settings
from mcp_starter_core.lifecycle import server_lifespan


def create_server(settings: Settings | None = None) -> MCPServer[Any]:
    """Create the server and register each capability module once."""
    config = settings or get_settings()
    verifier = _make_verifier(config)
    auth = None
    if verifier is not None:
        assert config.auth_issuer_url is not None
        assert config.auth_resource_url is not None
        auth = AuthSettings(
            issuer_url=config.auth_issuer_url,
            resource_server_url=config.auth_resource_url,
            required_scopes=config.auth_required_scopes,
            validate_token_resource=True,
        )

    server = MCPServer(
        name=config.server_name,
        version=config.server_version or __version__,
        instructions=config.server_instructions,
        lifespan=partial(server_lifespan, verifier=verifier),
        cache_hints={
            "server/discover": CacheHint(ttl_ms=60_000, scope="public"),
            "tools/list": CacheHint(ttl_ms=60_000, scope="public"),
            "resources/list": CacheHint(ttl_ms=60_000, scope="public"),
            "resources/templates/list": CacheHint(ttl_ms=60_000, scope="public"),
            "resources/read": CacheHint(ttl_ms=30_000, scope="public"),
            "prompts/list": CacheHint(ttl_ms=60_000, scope="public"),
        },
        token_verifier=verifier,
        auth=auth,
    )
    calculator.register(server)
    catalog.register(server)
    return server


def _make_verifier(settings: Settings) -> OAuthIntrospectionVerifier | None:
    if not settings.auth_enabled:
        return None
    assert settings.auth_introspection_url is not None
    assert settings.auth_resource_url is not None
    assert settings.auth_client_id is not None
    assert settings.auth_client_secret is not None
    return OAuthIntrospectionVerifier(
        introspection_url=str(settings.auth_introspection_url),
        client_id=settings.auth_client_id,
        client_secret=settings.auth_client_secret,
        expected_resource=str(settings.auth_resource_url),
        timeout_seconds=settings.auth_timeout_seconds,
    )
