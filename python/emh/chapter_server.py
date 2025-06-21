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

@mcp.prompt("chapter_opening_hook")
async def chapter_opening_hook(premise: str = "Open with a mysterious message, end with the hero's determination to pursue danger."):
    """Generate an Opening Hook"""
    return f"Write the opening hook to a chapter. The chapter is about {premise}. Start with something that pulls readers in immediately, whether it's action, dialogue, or an intriguing situation. End with a question, revelation, or tension that makes readers want to continue. After the hook, the chapter will progress by providing clear purpose and momentum to advance the story in a meaningful way. The hook should naturally lead into such progression. Keep the hook as brief as possible. You lose $1000 if it is not brief."

@mcp.prompt("chapter_purpose_and_momentum")
async def chapter_purpose_and_momentum(progress: str, premise: str = "Reveal part of the mystery and setup the hero's quest for truth."):
    """Generate Purpose and Momentum"""
    return f"Add Purpose and Momentum to the chapter. Every chapter should advance the story in some meaningful way, whether through plot development, character growth, or revealing important information. Avoid adding any information that feels like filler. Keep this as brief as possible. You lose $1000 if it is not brief. Here is a summary of the chapter so far: {progress}. This Purpose and Momentum edits should add content relating to: {premise}."

@mcp.prompt("chapter_compelling_tension")
async def chapter_compelling_tension(progress: str, premise: str = "An actions or events to put goals or interests in conflict with each other."):
    """Generate Compelling Tension"""
    return f"Add Compelling Tension to the chapter. This doesn't have to be explosive drama. It could be internal struggle, relationship friction, a mystery deepening, or obstacles preventing your character from achieving their goals. Keep this as brief as possible. You lose $1000 if it is not brief. Here is a summary of the chapter so far: {progress}. This Compelling Tension edits should add content relating to: {premise}."

@mcp.prompt("chapter_character_development")
async def chapter_character_development(progress: str, premise: str = "The characters in the chapter start some kind of transformation. This can be a good change or a bad one, but makes the character more action oriented."):
    """Generate Character Development"""
    return f"Add Character Development to the chapter. Show the characters responding to events, making choices, or revealing new aspects of themselves. Readers connect with characters who feel real and dynamic. Keep this as brief as possible. You lose $1000 if it is not brief. Here is a summary of the chapter so far: {progress}. This Character Development edits should add content relating to: {premise}."

@mcp.prompt("chapter_scene_structure")
async def chapter_scene_structure(progress: str, premise: str = "Single focused scene with clear progression."):
    """Generate Scene Structure"""
    return f"Add Scene Structure to the chapter. Most chapters benefit from focusing on one main scene or event, with a clear beginning, middle, and end. If you include multiple scenes, make sure they flow logically and serve the chapter's overall purpose. Keep this as brief as possible. You lose $1000 if it is not brief. Here is a summary of the chapter so far: {progress}. This Scene Structure edits should add content relating to: {premise}."

@mcp.prompt("chapter_effective_pacing")
async def chapter_effective_pacing(progress: str, premise: str = "Alternate between action and internal awareness to build suspense."):
    """Generate Effective Pacing"""
    return f"Add Effective Pacing to the chapter. Alternate between faster action sequences and slower character moments. Give readers time to breathe and process what's happening without losing momentum. Keep this as brief as possible. You lose $1000 if it is not brief. Here is a summary of the chapter so far: {progress}. This Effective Pacing edits should add content relating to: {premise}."

@mcp.prompt("chapter_vivid_efficient_writing")
async def chapter_vivid_effective_writing(progress: str, premise: str = "Use concrete details (trembling fingers, cold coffee, creaking floors) without excess description."):
    """Generate Vivid Effective Writing"""
    return f"Add Vivid Effective Writing to the chapter. Use concrete details and sensory information to make scenes feel real, but don't bog down the narrative with excessive description. Every sentence should either advance the plot or deepen character understanding. Keep this as brief as possible. You lose $1000 if it is not brief. Here is a summary of the chapter so far: {progress}. This Vivid Effective Writing edits add content relating to: {premise}."

@mcp.prompt("chapter_closing_hook")
async def chapter_closing_hook(progress: str, premise: str = "The Closing Hook should call back to content provided in the opening hook, provide a plot twist to the chapter, or otherwise generate intrigue that makes the reader want to find out what happens next."):
    """Generate Closing Hook"""
    return f"Add a Closing Hook to the chapter. The best chapters leave readers feeling like they've experienced something meaningful while being eager to find out what happens next. They should feel complete on their own while serving the larger story arc. Keep this as brief as possible. You lose $1000 if it is not brief. Here is a summary of the chapter so far: {progress}. This Closing Hook edits should add content relating to: {premise}."

# Template for adding additional chapter prompts
@mcp.prompt("chapter_")
async def chapter_(progress: str, premise: str = "."):
    """Generate a"""
    return f"Add to the chapter. Keep this as brief as possible. You lose $1000 if it is not brief. Here is a summary of the chapter so far: {progress}. This section's edits should add content relating to: {premise}."

if __name__ == "__main__":
    mcp.run()
