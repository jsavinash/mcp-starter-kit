"""ASGI entry point for deployments using uvicorn or another ASGI host."""

from mcp_example_server.server import create_server
from mcp_starter_core.config import get_settings
from mcp_starter_core.logging import configure_logging
from mcp_starter_core.transport import build_transport_security

settings = get_settings()
if settings.transport != "streamable-http":
    raise RuntimeError("Set MCP_TRANSPORT=streamable-http when serving the ASGI app")
configure_logging(settings.log_level, settings.log_format)
server = create_server(settings)
app = server.streamable_http_app(
    host=settings.host,
    streamable_http_path=settings.http_path,
    max_request_body_size=settings.max_request_body_size,
    transport_security=build_transport_security(settings),
    json_response=False,
)
