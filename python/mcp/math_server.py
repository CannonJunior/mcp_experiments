# Copyright 2025 CannonJunior
  
# This file is part of mcp_experiments, and is released under the "MIT License Agreement".
# Please see the LICENSE.md file that should have been included as part of this package.
# Created: 2025.06.17
# By: CannonJunior with Google search
#Prompt: multiplication model context protocol python example
# Usage: called by client.py
# Alternate usage: uv run math_server.py

from fastmcp import FastMCP

mcp = FastMCP("Math Server")

@mcp.tool(name="multiply", description="Multiplies two numbers")
def multiply(a: float, b: float) -> float:
    return a * b

if __name__ == "__main__":
    mcp.run()
