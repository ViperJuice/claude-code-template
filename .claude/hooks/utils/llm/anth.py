#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "anthropic>=0.18.0",
# ]
# ///

"""
Anthropic LLM integration for Claude Code hooks.
"""

import os
import sys
import json
from typing import Optional
from anthropic import Anthropic


def prompt_llm(prompt: str, model: str = "claude-3-haiku-20240307") -> Optional[str]:
    """
    Send a prompt to Anthropic's Claude and return the response.
    
    Args:
        prompt: The prompt to send to Claude
        model: The model to use (default: claude-3-haiku-20240307)
        
    Returns:
        The response from Claude, or None if the request fails
    """
    try:
        # Get API key from environment
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            print("Warning: ANTHROPIC_API_KEY not set, skipping LLM summarization", file=sys.stderr)
            return None
            
        # Initialize Anthropic client
        client = Anthropic(api_key=api_key)
        
        # Send message to Claude
        response = client.messages.create(
            model=model,
            max_tokens=150,
            temperature=0.1,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Extract and return the response content
        if response.content and len(response.content) > 0:
            return response.content[0].text
        else:
            return None
            
    except Exception as e:
        # Don't print authentication errors to avoid spam
        if "authentication_error" not in str(e) and "invalid x-api-key" not in str(e):
            print(f"Error calling Anthropic API: {e}", file=sys.stderr)
        return None 