# Copyright 2025 CannonJunior

# This file is part of mcp_experiments, and is released under the "MIT License Agreement".
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
            "greeting": {
                "command": "python",
                "args": ["greeting_server.py"]
            },
            "finance": {
                "command": "python",
                "args": ["finance_server.py"]
            },
            "kafka": {
                "command": "python",
                "args": ["kafka_mcp_server.py"]
            },
            "math": {
                "command": "python",
                "args": ["math_server.py"]
            }
        }
    }

    # config['mcpServers']['_server'] = { "url": "http://localhost:9000/mcp" }

    os.environ["OPENAI_API_KEY"] = "NA"
    model_name = 'incept5/llama3.1-claude:latest'
 
    async with Client(config) as client:
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
        
        # Read resource via template
        result = await client.read_resource("file://greeting/hello/Junior")
        print(f"Content: {result}")
        
        # Get prompt
        prompt_result = await client.get_prompt(
            "greeting_greet",
            arguments={"name": "Alice"}
        )
        print(f"Prompt: {prompt_result.messages[0].content.text}")

        symbol = "AAPL"
        finance_response = await client.call_tool("finance_get_quote", {
            "symbol": symbol
        })
        print(f"finance_get_quote: {finance_response}")

        math_request = (
            "math_server_multiply",
            {"a": 1337, "b": 251}
        )
        math_response = await client.call_tool("math_multiply", {
            "a": 1337,
            "b": 251
        })
        print(f"math_multiply: {math_response}")

        # AI delegation
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

"""
        # Consume messages from a topic
        #messages = await kafka_consume_messages(
        messages = await client.call_tool("kafka_kafka_consume_messages", {
            "topic": "user-events",
            "bootstrap_servers": "localhost:9092",
            "max_messages": 10
        })
        print(messages)

        # Peek at latest messages without committing
        #peek_messages = await kafka_peek_messages(
        peek_messages = await client.call_tool("kafka_kafka_peek_messages", {
            "topic": "user-events",
            "offset": "latest",
            "max_messages": 5
        })

        # List available topics
        #topics = await kafka_list_topics(bootstrap_servers="localhost:9092")
        topics = await client.call_tool("kafka_kafka_list_topics", {
            "bootstrap_servers": "localhost:9092"
        })
"""

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
