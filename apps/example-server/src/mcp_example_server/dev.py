"""Module target for ``uv run mcp dev .../dev.py`` and the MCP Inspector."""

from mcp_example_server.server import create_server

mcp = create_server()
