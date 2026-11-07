"""Command-line runner for stdio and Streamable HTTP transports."""

from mcp_example_server.server import create_server
from mcp_starter_core.config import get_settings
from mcp_starter_core.logging import configure_logging
from mcp_starter_core.transport import build_transport_security


def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level, settings.log_format)
    server = create_server(settings)
    if settings.transport == "stdio":
        server.run(transport="stdio")
        return
    server.run(
        transport="streamable-http",
        host=settings.host,
        port=settings.port,
        streamable_http_path=settings.http_path,
        max_request_body_size=settings.max_request_body_size,
        transport_security=build_transport_security(settings),
        json_response=False,
    )
