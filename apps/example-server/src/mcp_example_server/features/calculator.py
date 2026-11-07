"""Side-effect-free example tools with typed, schema-derived inputs."""

import math
from typing import Annotated, Literal

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import Field

Operation = Literal["add", "subtract", "multiply", "divide"]
FiniteNumber = Annotated[float, Field(ge=-1e12, le=1e12, allow_inf_nan=False)]


def register(server: MCPServer[object]) -> None:
    """Register the calculator capability set."""

    @server.tool(title="Calculate")
    async def calculate(operation: Operation, left: FiniteNumber, right: FiniteNumber) -> float:
        """Perform one basic arithmetic operation on two finite numbers."""
        if operation == "add":
            result = left + right
        elif operation == "subtract":
            result = left - right
        elif operation == "multiply":
            result = left * right
        else:
            if right == 0:
                raise ToolError("Division by zero is undefined. Supply a non-zero right operand.")
            result = left / right
        if not math.isfinite(result):
            raise ToolError("The result is outside the supported numeric range.")
        return result
