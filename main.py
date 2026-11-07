"""Repository convenience entry point; installed apps use their own console scripts."""

from __future__ import annotations


def build_welcome_message() -> str:
    """Retained compatibility helper for the original repository smoke check."""
    return "Hello from mcp-starter-kit!"


def main() -> None:
    """Run the example MCP server configured by environment variables."""
    from mcp_example_server.cli import main as run_server

    run_server()


if __name__ == "__main__":
    main()
