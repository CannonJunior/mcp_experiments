# Copyright 2025 CannonJunior
  
# This file is part of mcp_experiments, and is released under the "MIT License Agreement".
# Please see the LICENSE.md file that should have been included as part of this package.
# Created: 2025.06.14
# By: CannonJunior with Claude (3.7 free version)
#Prompt (amongst others): Write a very simple example using an MCP resource. Write the MCP server and MCP client using the Python SDK and FastMCP library. Keep this extremely brief, you lose $1000 if it is not brief.
# Usage: called by client.py
# Alternate usage: uv run greeting_server.py

from fastmcp import FastMCP

mcp = FastMCP("Greeting Server")

@mcp.resource("file://hello/{name}")
async def hello_resource(name: str):
    """Get a personalized hello message"""
    return f"Hello {name} from MCP resource!"

@mcp.prompt("greet")
async def greet_prompt(name: str = "World"):
    """Generate a greeting prompt"""
    return f"Please greet {name} in a friendly way."

if __name__ == "__main__":
    mcp.run()
