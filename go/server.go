// Copyright 2025 CannonJunior
// This file is part of mcp_experiments, and is released under the "MIT License Agreement".
// Please see the LICENSE.md file that should have been included as part of this package.

// Created: 2025.06.15
// By: CannonJunior with Claude (3.7 free version)
// Prompt:
/* Rewrite this Python <program> in Go:
<program>
from fastmcp import FastMCP
mcp = FastMCP("Simple Server")
@mcp.resource("file://hello/{name}")
async def hello_resource(name: str):
    """Get a personalized hello message"""
    return f"Hello {name} from MCP resource!"
@mcp.prompt("greet")
async def greet_prompt(name: str = "World"):
    """Generate a greeting prompt"""
    return f"Please greet {name} in a friendly way."
if name == "main":
    mcp.run()
</program>
*/
// Usage: go run server.go
// Resource: GET http://localhost:8080/resource/hello/John
// Prompt: GET http://localhost:8080/prompt/greet?name=Alice
// Health: GET http://localhost:8080/health

package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"regexp"
	"strings"
)

type MCPServer struct {
	name      string
	resources map[string]ResourceHandler
	prompts   map[string]PromptHandler
}

type ResourceHandler func(params map[string]string) (string, error)
type PromptHandler func(params map[string]string) (string, error)

type MCPResponse struct {
	Content string            `json:"content"`
	Params  map[string]string `json:"params,omitempty"`
	Error   string            `json:"error,omitempty"`
}

func NewMCPServer(name string) *MCPServer {
	return &MCPServer{
		name:      name,
		resources: make(map[string]ResourceHandler),
		prompts:   make(map[string]PromptHandler),
	}
}

func (s *MCPServer) AddResource(pattern string, handler ResourceHandler) {
	s.resources[pattern] = handler
}

func (s *MCPServer) AddPrompt(name string, handler PromptHandler) {
	s.prompts[name] = handler
}

func (s *MCPServer) handleResource(w http.ResponseWriter, r *http.Request) {
	path := strings.TrimPrefix(r.URL.Path, "/resource/")
	
	for pattern, handler := range s.resources {
		if params := s.matchPattern(pattern, path); params != nil {
			result, err := handler(params)
			response := MCPResponse{
				Content: result,
				Params:  params,
			}
			if err != nil {
				response.Error = err.Error()
			}
			s.sendJSONResponse(w, response)
			return
		}
	}
	
	http.NotFound(w, r)
}

func (s *MCPServer) handlePrompt(w http.ResponseWriter, r *http.Request) {
	promptName := strings.TrimPrefix(r.URL.Path, "/prompt/")
	
	if handler, exists := s.prompts[promptName]; exists {
		params := make(map[string]string)
		
		// Parse query parameters
		for key, values := range r.URL.Query() {
			if len(values) > 0 {
				params[key] = values[0]
			}
		}
		
		result, err := handler(params)
		response := MCPResponse{
			Content: result,
			Params:  params,
		}
		if err != nil {
			response.Error = err.Error()
		}
		s.sendJSONResponse(w, response)
		return
	}
	
	http.NotFound(w, r)
}

func (s *MCPServer) matchPattern(pattern, path string) map[string]string {
	// Convert pattern like "file://hello/{name}" to regex
	// Remove the protocol part for simplicity
	if strings.HasPrefix(pattern, "file://") {
		pattern = strings.TrimPrefix(pattern, "file://")
	}
	
	// Convert {name} to named capture groups
	regexPattern := regexp.MustCompile(`\{([^}]+)\}`).ReplaceAllString(pattern, `(?P<$1>[^/]+)`)
	regexPattern = "^" + regexPattern + "$"
	
	re, err := regexp.Compile(regexPattern)
	if err != nil {
		return nil
	}
	
	matches := re.FindStringSubmatch(path)
	if matches == nil {
		return nil
	}
	
	params := make(map[string]string)
	for i, name := range re.SubexpNames() {
		if i > 0 && name != "" {
			params[name] = matches[i]
		}
	}
	
	return params
}

func (s *MCPServer) sendJSONResponse(w http.ResponseWriter, response MCPResponse) {
	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(response); err != nil {
		http.Error(w, "Failed to encode response", http.StatusInternalServerError)
	}
}

func (s *MCPServer) Run(port string) {
	if port == "" {
		port = "8080"
	}
	
	http.HandleFunc("/resource/", s.handleResource)
	http.HandleFunc("/prompt/", s.handlePrompt)
	
	// Health check endpoint
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "MCP Server '%s' is running", s.name)
	})
	
	fmt.Printf("Starting MCP Server '%s' on port %s\n", s.name, port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}

// Resource handlers
func helloResourceHandler(params map[string]string) (string, error) {
	name, exists := params["name"]
	if !exists {
		name = "World"
	}
	return fmt.Sprintf("Hello %s from MCP resource!", name), nil
}

// Prompt handlers
func greetPromptHandler(params map[string]string) (string, error) {
	name, exists := params["name"]
	if !exists {
		name = "World"
	}
	return fmt.Sprintf("Please greet %s in a friendly way.", name), nil
}

func main() {
	mcp := NewMCPServer("Simple Server")
	
	// Register the hello resource with pattern matching
	mcp.AddResource("file://hello/{name}", helloResourceHandler)
	
	// Register the greet prompt
	mcp.AddPrompt("greet", greetPromptHandler)
	
	// Start the server
	mcp.Run("8080")
}
