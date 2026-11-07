"""Transport security construction shared by CLI and ASGI entry points."""

from mcp.server.transport_security import TransportSecuritySettings

from mcp_starter_core.config import Settings


def build_transport_security(settings: Settings) -> TransportSecuritySettings:
    """Build explicit host and origin protections for Streamable HTTP."""
    return TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=settings.allowed_hosts,
        allowed_origins=settings.allowed_origins,
    )
