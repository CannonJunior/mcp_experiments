# Copyright 2025 CannonJunior

# This file is part of mcp_experiments, and is released under the "MIT License Agreement".
# Please see the LICENSE.md file that should have been included as part of this package.
# Created: 2025.06.20
# By: CannonJunior 
# Usage: uv run chapter_client.py

import asyncio
import json
import os
import ollama

from fastmcp import Client, FastMCP
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def mcp_list(client):
    # List tools from all servers
    tools = await client.list_tools()
    print(f"Tools: {[t.name for t in tools]}")

    # List resources from all servers
    resources = await client.list_resources()
    print(f"Resources: {[r.name for r in resources]}")

    # List resource templates from all servers
    templates = await client.list_resource_templates()
    print(f"Templates: {[t.name for t in templates]}")

    # List prompts
    prompts = await client.list_prompts()
    print(f"Prompts: {[p.name for p in prompts]}")

async def main():
    config = {
        "mcpServers": {
            "chapter": {
                "command": "python",
                "args": ["chapter_server.py"]
            }
        }
    }

    # config['mcpServers']['_server'] = { "url": "http://localhost:9000/mcp" }

    os.environ["OPENAI_API_KEY"] = "NA"
    #model_name = 'incept5/llama3.1-claude:latest'
    model_name = 'qwen2.5:3b'
 
    async with Client(config) as client:
        await mcp_list(client)

        # Get prompt: Hook
        prompt_result = await client.get_prompt(
            "chapter_opening_hook",
            arguments={"premise": "Alice"}
        )
        print()
        print(f"Prompt: {prompt_result.messages[0].content.text}")
        print()
        print(f"prompt results: {prompt_result}")

        # Use prompt with ollama model
        response = ollama.chat(
            model=model_name,
            messages=[{
                'role': 'user',
                'content': f''' Take this prompt and generate an appropriate response: {prompt_result} '''
            }]
        )
        print()
        print(f"Generated prompt response: {response}")
        print()

        #text_response = await client.call_tool("text_chapter_hook", {
        #    "": symbol
        #})
        #print(f"finance_get_quote: {finance_response}")

        '''
        # AI delegation
        resources = await client.list_resources()
        print(f"resources {resources}")
        resources_list = [r.uri for r in resources]
        print(resources_list)
        query = "Get error logs for troubleshooting"
        delegation = ollama.generate(
        model=model_name,
            prompt=f"Pick one from {resources_list} for: {query}. Return only the URI."
        )
        chosen = delegation['response'].strip()
        if chosen in resources_list:
            result = await session.read_resource(chosen)
            print(f"\nAI chose {chosen}:\n{result.contents[0].text[:200]}...")
        '''

if __name__ == "__main__":
    asyncio.run(main())
