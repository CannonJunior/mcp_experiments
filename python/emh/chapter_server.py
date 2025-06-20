# Copyright 2025 CannonJunior
  
# This file is part of mcp_experiments, and is released under the "MIT License Agreement".
# Please see the LICENSE.md file that should have been included as part of this package.
# Created: 2025.06.20
# By: CannonJunior
# Supporting Prompt: What does it take to make a successful fiction chapter?
# Usage: called by chapter_client.py
# Alternate usage: uv run chapter_server.py

from fastmcp import FastMCP

mcp = FastMCP("Greeting Server")

@mcp.resource("file://hello/{name}")
async def hello_resource(name: str):
    """Get a personalized hello message"""
    return f"Hello {name} from MCP resource!"

@mcp.prompt("chapter_hook")
async def chapter_hook(premise: str = "It was a dark and stormy night."):
    """Generate a chapter hook"""
    return f"Write the opening hook to a chapter. The chapter is about {premise}. Start with something that pulls readers in immediately, whether it's action, dialogue, or an intriguing situation. End with a question, revelation, or tension that makes readers want to continue. After the hook, the chapter will progress by providing clear purpose and momentum to advance the story in a meaningful way. The hook should naturally lead into such progression. Keep the hook as brief as possible. You lose $1000 if it is not brief."

if __name__ == "__main__":
    mcp.run()
