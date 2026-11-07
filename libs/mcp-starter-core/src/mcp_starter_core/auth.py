"""OAuth 2.1 resource-server token verification via RFC 7662 introspection."""

from __future__ import annotations

import logging
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import httpx
from mcp.server.auth.provider import AccessToken, TokenVerifier
from pydantic import SecretStr

logger = logging.getLogger(__name__)


class OAuthIntrospectionVerifier(TokenVerifier):
    """Validate bearer tokens against an authorization server's introspection endpoint.

    The HTTP client is opened by the MCP server lifespan and reused across calls. Only
    allowlisted claims are attached to the SDK token context, and token values are never logged.
    """

    def __init__(
        self,
        *,
        introspection_url: str,
        client_id: str,
        client_secret: SecretStr,
        expected_resource: str,
        timeout_seconds: float = 3.0,
    ) -> None:
        self.introspection_url = introspection_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.expected_resource = expected_resource.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self._client: httpx.AsyncClient | None = None

    @asynccontextmanager
    async def lifespan(self) -> AsyncIterator[None]:
        async with httpx.AsyncClient(
            auth=httpx.BasicAuth(self.client_id, self.client_secret.get_secret_value()),
            timeout=httpx.Timeout(self.timeout_seconds),
            follow_redirects=False,
        ) as client:
            self._client = client
            try:
                yield
            finally:
                self._client = None

    async def verify_token(self, token: str) -> AccessToken | None:
        if self._client is None:
            logger.error("oauth.introspection_client_unavailable")
            return None
        try:
            response = await self._client.post(self.introspection_url, data={"token": token})
            response.raise_for_status()
            payload: Any = response.json()
        except (httpx.HTTPError, ValueError):
            logger.warning("oauth.introspection_failed")
            return None

        if not isinstance(payload, dict) or payload.get("active") is not True:
            return None

        resource = _matching_resource(payload, self.expected_resource)
        if resource is None:
            return None

        client_id = payload.get("client_id")
        if not isinstance(client_id, str) or not client_id:
            return None

        expires_at = _integer_claim(payload.get("exp"))
        if "exp" in payload and expires_at is None:
            return None
        if expires_at is not None and expires_at <= int(time.time()):
            return None

        raw_scopes = payload.get("scope", "")
        if isinstance(raw_scopes, str):
            scopes = raw_scopes.split()
        elif isinstance(raw_scopes, list) and all(isinstance(item, str) for item in raw_scopes):
            scopes = raw_scopes
        else:
            return None

        safe_claims = {
            key: payload[key]
            for key in ("iss", "sub", "aud")
            if key in payload and isinstance(payload[key], (str, list))
        }
        subject = payload.get("sub")
        return AccessToken(
            token=token,
            client_id=client_id,
            scopes=scopes,
            resource=resource,
            subject=subject if isinstance(subject, str) else None,
            expires_at=expires_at,
            claims=safe_claims,
        )


def _matching_resource(payload: dict[str, Any], expected: str) -> str | None:
    resource = payload.get("resource")
    if isinstance(resource, str) and resource.rstrip("/") == expected:
        return resource
    audience = payload.get("aud")
    if isinstance(audience, str) and audience.rstrip("/") == expected:
        return audience
    if isinstance(audience, list):
        for item in audience:
            if isinstance(item, str) and item.rstrip("/") == expected:
                return item
    return None


def _integer_claim(value: object) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdecimal():
        return int(value)
    return None
