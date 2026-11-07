"""Typed configuration and fail-closed deployment checks."""

from __future__ import annotations

import ipaddress
from functools import lru_cache
from typing import Annotated, Literal

from pydantic import AnyHttpUrl, Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    """Service settings sourced from environment variables prefixed with ``MCP_``."""

    model_config = SettingsConfigDict(
        env_prefix="MCP_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        enable_decoding=False,
    )

    server_name: str = "example-server"
    server_version: str | None = None
    server_instructions: str = "A modular example Model Context Protocol server."
    transport: Literal["stdio", "streamable-http"] = "stdio"
    host: str = "127.0.0.1"
    port: int = Field(default=8000, ge=1, le=65535)
    http_path: str = "/mcp"
    max_request_body_size: int = Field(default=4 * 1024 * 1024, ge=1024, le=16 * 1024 * 1024)
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_format: Literal["console", "json"] = "console"
    allowed_hosts: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["localhost:*", "127.0.0.1:*", "[::1]:*"]
    )
    allowed_origins: Annotated[list[str], NoDecode] = Field(default_factory=list)

    auth_enabled: bool = False
    auth_issuer_url: AnyHttpUrl | None = None
    auth_resource_url: AnyHttpUrl | None = None
    auth_introspection_url: AnyHttpUrl | None = None
    auth_client_id: str | None = None
    auth_client_secret: SecretStr | None = None
    auth_required_scopes: Annotated[list[str], NoDecode] = Field(default_factory=list)
    auth_timeout_seconds: float = Field(default=3.0, gt=0, le=30)

    @field_validator("http_path")
    @classmethod
    def validate_http_path(cls, value: str) -> str:
        if not value.startswith("/") or "?" in value or "#" in value:
            raise ValueError(
                "MCP_HTTP_PATH must be a path beginning with '/' and contain no query/fragment"
            )
        return value

    @field_validator("log_level", mode="before")
    @classmethod
    def normalize_log_level(cls, value: object) -> object:
        return value.upper() if isinstance(value, str) else value

    @field_validator("allowed_hosts", "allowed_origins", "auth_required_scopes", mode="before")
    @classmethod
    def parse_comma_separated_values(cls, value: object) -> object:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @model_validator(mode="after")
    def validate_deployment(self) -> Settings:
        if self.auth_enabled:
            if self.transport != "streamable-http":
                raise ValueError(
                    "OAuth resource-server auth is only available over Streamable HTTP"
                )
            missing = [
                name
                for name, value in (
                    ("MCP_AUTH_ISSUER_URL", self.auth_issuer_url),
                    ("MCP_AUTH_RESOURCE_URL", self.auth_resource_url),
                    ("MCP_AUTH_INTROSPECTION_URL", self.auth_introspection_url),
                    ("MCP_AUTH_CLIENT_ID", self.auth_client_id),
                    ("MCP_AUTH_CLIENT_SECRET", self.auth_client_secret),
                )
                if value is None
            ]
            if missing:
                missing_values = ", ".join(missing)
                raise ValueError(
                    f"OAuth auth is enabled but settings are missing: {missing_values}"
                )
            auth_urls = (
                self.auth_issuer_url,
                self.auth_resource_url,
                self.auth_introspection_url,
            )
            for value in auth_urls:
                if (
                    value is not None
                    and value.scheme != "https"
                    and not _is_loopback(value.host or "")
                ):
                    raise ValueError("OAuth URLs must use HTTPS outside local development")

        if self.transport == "streamable-http" and not _is_loopback(self.host):
            if not self.auth_enabled:
                raise ValueError("Non-loopback Streamable HTTP requires OAuth resource-server auth")
            public_hosts = [
                host
                for host in self.allowed_hosts
                if not host.startswith(("localhost", "127.", "[::1]"))
            ]
            if not public_hosts:
                raise ValueError(
                    "Set MCP_ALLOWED_HOSTS to the exact public hostname(s) for remote deployment"
                )
        return self


def _is_loopback(host: str) -> bool:
    if host.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Load and validate process settings once per worker process."""
    return Settings()
