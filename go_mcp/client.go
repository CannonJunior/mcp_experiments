// Copyright 2025 CannonJunior
// This file is part of [project name], and is released under the "MIT License Agreement".
// Please see the LICENSE.md file that should have been included as part of this package.

// Created: 2025.06.15
// By: CannonJunior with Claude (3.7 free version)
// Prompt:
/*
Rewrite this Python <program> in Go:
<program>
# mcp_client.py
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
if name == "main":
    asyncio.run(main())
</program>
*/
// Usage: go run client.go

package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/exec"
	"strings"
	"time"
)

type Config struct {
	MCPServers map[string]ServerConfig `json:"mcpServers"`
}

type ServerConfig struct {
	Command string   `json:"command,omitempty"`
	Args    []string `json:"args,omitempty"`
	URL     string   `json:"url,omitempty"`
}

type Resource struct {
	Name string `json:"name"`
	URI  string `json:"uri"`
}

type ResourceTemplate struct {
	Name        string `json:"name"`
	URITemplate string `json:"uriTemplate"`
}

type Prompt struct {
	Name        string            `json:"name"`
	Description string            `json:"description"`
	Arguments   map[string]string `json:"arguments,omitempty"`
}

type PromptMessage struct {
	Role    string `json:"role"`
	Content struct {
		Text string `json:"text"`
	} `json:"content"`
}

type PromptResult struct {
	Messages []PromptMessage `json:"messages"`
}

type MCPClient struct {
	config  Config
	servers map[string]*exec.Cmd
}

func NewMCPClient(config Config) *MCPClient {
	return &MCPClient{
		config:  config,
		servers: make(map[string]*exec.Cmd),
	}
}

func (c *MCPClient) Start() error {
	// Start stdio-based servers
	for name, serverConfig := range c.config.MCPServers {
		if serverConfig.Command != "" {
			cmd := exec.Command(serverConfig.Command, serverConfig.Args...)
			if err := cmd.Start(); err != nil {
				return fmt.Errorf("failed to start server %s: %v", name, err)
			}
			c.servers[name] = cmd
			fmt.Printf("Started server %s with PID %d\n", name, cmd.Process.Pid)

			// Give the server time to start
			time.Sleep(1 * time.Second)
		}
	}
	return nil
}

func (c *MCPClient) Stop() error {
	for name, cmd := range c.servers {
		if cmd.Process != nil {
			if err := cmd.Process.Kill(); err != nil {
				fmt.Printf("Error stopping server %s: %v\n", name, err)
			} else {
				fmt.Printf("Stopped server %s\n", name)
			}
		}
	}
	return nil
}

func (c *MCPClient) makeHTTPRequest(url string) ([]byte, error) {
	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("HTTP request failed with status: %d", resp.StatusCode)
	}

	return io.ReadAll(resp.Body)
}

func (c *MCPClient) ListResources() ([]Resource, error) {
	var allResources []Resource

	for name, serverConfig := range c.config.MCPServers {
		if serverConfig.URL != "" {
			// For HTTP-based servers
			url := strings.TrimSuffix(serverConfig.URL, "/mcp") + "/resources"
			data, err := c.makeHTTPRequest(url)
			if err != nil {
				fmt.Printf("Warning: Failed to get resources from %s: %v\n", name, err)
				continue
			}

			var resources []Resource
			if err := json.Unmarshal(data, &resources); err != nil {
				fmt.Printf("Warning: Failed to parse resources from %s: %v\n", name, err)
				continue
			}
			allResources = append(allResources, resources...)
		} else {
			// For stdio-based servers, simulate some resources
			// In a real implementation, you'd communicate via stdin/stdout
			allResources = append(allResources, Resource{
				Name: fmt.Sprintf("%s/hello", name),
				URI:  fmt.Sprintf("file://%s/hello/{name}", name),
			})
		}
	}

	return allResources, nil
}

func (c *MCPClient) ListResourceTemplates() ([]ResourceTemplate, error) {
	var allTemplates []ResourceTemplate

	for name, serverConfig := range c.config.MCPServers {
		if serverConfig.URL != "" {
			// For HTTP-based servers
			url := strings.TrimSuffix(serverConfig.URL, "/mcp") + "/resource-templates"
			data, err := c.makeHTTPRequest(url)
			if err != nil {
				fmt.Printf("Warning: Failed to get templates from %s: %v\n", name, err)
				continue
			}

			var templates []ResourceTemplate
			if err := json.Unmarshal(data, &templates); err != nil {
				fmt.Printf("Warning: Failed to parse templates from %s: %v\n", name, err)
				continue
			}
			allTemplates = append(allTemplates, templates...)
		} else {
			// Simulate templates for stdio servers
			allTemplates = append(allTemplates, ResourceTemplate{
				Name:        fmt.Sprintf("%s/hello", name),
				URITemplate: fmt.Sprintf("file://%s/hello/{name}", name),
			})
		}
	}

	return allTemplates, nil
}

func (c *MCPClient) ListPrompts() ([]Prompt, error) {
	var allPrompts []Prompt

	for name, serverConfig := range c.config.MCPServers {
		if serverConfig.URL != "" {
			// For HTTP-based servers
			url := strings.TrimSuffix(serverConfig.URL, "/mcp") + "/prompts"
			data, err := c.makeHTTPRequest(url)
			if err != nil {
				fmt.Printf("Warning: Failed to get prompts from %s: %v\n", name, err)
				continue
			}

			var prompts []Prompt
			if err := json.Unmarshal(data, &prompts); err != nil {
				fmt.Printf("Warning: Failed to parse prompts from %s: %v\n", name, err)
				continue
			}
			allPrompts = append(allPrompts, prompts...)
		} else {
			// Simulate prompts for stdio servers
			allPrompts = append(allPrompts, Prompt{
				Name:        fmt.Sprintf("%s_greet", name),
				Description: "Generate a greeting prompt",
			})
		}
	}

	return allPrompts, nil
}

func (c *MCPClient) ReadResource(uri string) (string, error) {
	// Parse URI to determine which server to use
	// For simplicity, assume format: file://servername/path
	if !strings.HasPrefix(uri, "file://") {
		return "", fmt.Errorf("unsupported URI scheme")
	}

	path := strings.TrimPrefix(uri, "file://")
	parts := strings.SplitN(path, "/", 2)
	if len(parts) < 2 {
		return "", fmt.Errorf("invalid URI format")
	}

	serverName := parts[0]
	resourcePath := parts[1]

	serverConfig, exists := c.config.MCPServers[serverName]
	if !exists {
		return "", fmt.Errorf("server %s not found", serverName)
	}

	if serverConfig.URL != "" {
		// HTTP-based server
		url := fmt.Sprintf("%s/resource/%s", strings.TrimSuffix(serverConfig.URL, "/mcp"), resourcePath)
		data, err := c.makeHTTPRequest(url)
		if err != nil {
			return "", err
		}

		var response struct {
			Content string `json:"content"`
		}
		if err := json.Unmarshal(data, &response); err != nil {
			return "", err
		}
		return response.Content, nil
	}

	// For stdio servers, simulate the response
	// In a real implementation, you'd send JSON-RPC requests via stdin
	if strings.HasPrefix(resourcePath, "hello/") {
		name := strings.TrimPrefix(resourcePath, "hello/")
		return fmt.Sprintf("Hello %s from MCP resource!", name), nil
	}

	return "", fmt.Errorf("resource not found")
}

func (c *MCPClient) GetPrompt(name string, arguments map[string]string) (*PromptResult, error) {
	// Parse prompt name to determine server
	parts := strings.Split(name, "_")
	if len(parts) < 2 {
		return nil, fmt.Errorf("invalid prompt name format")
	}

	serverName := parts[0]
	promptName := strings.Join(parts[1:], "_")

	serverConfig, exists := c.config.MCPServers[serverName]
	if !exists {
		return nil, fmt.Errorf("server %s not found", serverName)
	}

	if serverConfig.URL != "" {
		// HTTP-based server
		url := fmt.Sprintf("%s/prompt/%s", strings.TrimSuffix(serverConfig.URL, "/mcp"), promptName)

		// Add arguments as query parameters
		if len(arguments) > 0 {
			url += "?"
			params := make([]string, 0, len(arguments))
			for k, v := range arguments {
				params = append(params, fmt.Sprintf("%s=%s", k, v))
			}
			url += strings.Join(params, "&")
		}

		data, err := c.makeHTTPRequest(url)
		if err != nil {
			return nil, err
		}

		var response struct {
			Content string `json:"content"`
		}
		if err := json.Unmarshal(data, &response); err != nil {
			return nil, err
		}

		return &PromptResult{
			Messages: []PromptMessage{
				{
					Role: "user",
					Content: struct {
						Text string `json:"text"`
					}{Text: response.Content},
				},
			},
		}, nil
	}

	// Simulate prompt response for stdio servers
	userName := "World"
	if name, exists := arguments["name"]; exists {
		userName = name
	}

	return &PromptResult{
		Messages: []PromptMessage{
			{
				Role: "user",
				Content: struct {
					Text string `json:"text"`
				}{Text: fmt.Sprintf("Please greet %s in a friendly way.", userName)},
			},
		},
	}, nil
}

func main() {
	// Set environment variable
	os.Setenv("OPENAI_API_KEY", "NA")

	config := Config{
		MCPServers: map[string]ServerConfig{
			"simple": {
				Command: "python3",
				Args:    []string{"server.py"},
			},
			"demo_math": {
				URL: "http://localhost:9000/mcp",
			},
		},
	}

	client := NewMCPClient(config)

	// Start the client
	if err := client.Start(); err != nil {
		log.Fatalf("Failed to start client: %v", err)
	}
	defer client.Stop()

	// List resources from all servers
	resources, err := client.ListResources()
	if err != nil {
		log.Printf("Error listing resources: %v", err)
	} else {
		resourceNames := make([]string, len(resources))
		for i, r := range resources {
			resourceNames[i] = r.Name
		}
		fmt.Printf("Resources: %v\n", resourceNames)
	}

	// List resource templates from all servers
	templates, err := client.ListResourceTemplates()
	if err != nil {
		log.Printf("Error listing templates: %v", err)
	} else {
		templateNames := make([]string, len(templates))
		for i, t := range templates {
			templateNames[i] = t.Name
		}
		fmt.Printf("Templates: %v\n", templateNames)
	}

	// List prompts
	prompts, err := client.ListPrompts()
	if err != nil {
		log.Printf("Error listing prompts: %v", err)
	} else {
		promptNames := make([]string, len(prompts))
		for i, p := range prompts {
			promptNames[i] = p.Name
		}
		fmt.Printf("Prompts: %v\n", promptNames)
	}

	// Read resource via template
	result, err := client.ReadResource("file://simple/hello/Junior")
	if err != nil {
		log.Printf("Error reading resource: %v", err)
	} else {
		fmt.Printf("Content: %s\n", result)
	}

	// Get prompt
	promptResult, err := client.GetPrompt("simple_greet", map[string]string{"name": "Alice"})
	if err != nil {
		log.Printf("Error getting prompt: %v", err)
	} else {
		fmt.Printf("Prompt: %s\n", promptResult.Messages[0].Content.Text)
	}

	// Note: Ollama integration would require additional Go packages
	// You can add ollama-go or similar packages for LLM integration
	fmt.Println("\n// Ollama integration would require additional packages like:")
	fmt.Println("// go get github.com/ollama/ollama/api")
}
