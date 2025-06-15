# Copyright 2025 CannonJunior

# This file is part of [project name], and is released under the "MIT License Agreement".
# Please see the LICENSE.md file that should have been included as part of this package.
# Created: 2025.06.14
# By: CannonJunior with Claude (3.7 free version)
# Prompt (amongst others): Write a very simple example using an MCP resource. Write the MCP server and MCP client using the Python SDK and FastMCP library. Keep this extremely brief, you lose $1000 if it is not brief.
# Usage: uv run client.py

import asyncio
import json
import os
import ollama

from fastmcp import Client, FastMCP
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    config = {
        "mcpServers": {
            "simple": {
                "command": "python",
                "args": ["server.py"]
            },
            "demo_math": {
                "url": "http://localhost:9000/mcp"
            }
        }
    }

    os.environ["OPENAI_API_KEY"] = "NA"
    model_name = 'incept5/llama3.1-claude:latest'
    
    async with Client(config) as client:
        # List resources from all servers
        resources = await client.list_resources()
        print(f"Resources: {[r.name for r in resources]}")

        # List resource templates from all servers
        templates = await client.list_resource_templates()
        print(f"Templates: {[t.name for t in templates]}")
        
        # List prompts
        prompts = await client.list_prompts()
        print(f"Prompts: {[p.name for p in prompts]}")
        
        # Read resource via template
        #result = await client.read_resource("file://hello/world")
        result = await client.read_resource("file://simple/hello/Junior")
        print(f"Content: {result}")
        
        # Get prompt
        prompt_result = await client.get_prompt(
            "simple_greet",
            arguments={"name": "Alice"}
        )
        print(f"Prompt: {prompt_result.messages[0].content.text}")

"""
        # Might not ever run on a CPU
        response = ollama.chat(
            model=model_name,
            messages=[{
                'role': 'user',
                'content': f''' Take this prompt and generate an appropriate response: {prompt_result} '''
            }]
        )
        print(f"Generated prompt response: {response}")
"""

if __name__ == "__main__":
    asyncio.run(main())
