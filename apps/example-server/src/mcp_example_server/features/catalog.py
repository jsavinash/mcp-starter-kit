"""Example read-only resource catalog and reusable prompt."""

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ResourceNotFoundError

TOPICS = {
    "architecture": (
        "Keep transport, protocol, domain logic, and infrastructure in separate layers."
    ),
    "security": "Validate inputs, authorize each operation, and treat remote content as untrusted.",
    "operations": "Use bounded timeouts, structured logs, health checks, and graceful shutdown.",
}


def register(server: MCPServer[object]) -> None:
    """Register the example resource and prompt capabilities."""

    @server.resource("starter://guide")
    async def guide() -> str:
        """Read the starter kit topic index."""
        return "Available topics: " + ", ".join(sorted(TOPICS))

    @server.resource("starter://guide/{topic}")
    async def read_topic(topic: str) -> str:
        """Read a topic from the starter kit guide."""
        if topic not in TOPICS:
            raise ResourceNotFoundError(f"No guide topic named {topic!r}.")
        return TOPICS[topic]

    @server.prompt(title="Explain a starter topic")
    async def explain_topic(topic: str, audience: str = "developer") -> str:
        """Build a concise explanation prompt from a known guide topic."""
        if topic not in TOPICS:
            raise ValueError(f"Choose one of: {', '.join(sorted(TOPICS))}")
        return f"Explain this to a {audience}. Keep it accurate and concise.\n\n{TOPICS[topic]}"
