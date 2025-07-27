#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "anthropic",
#     "python-dotenv",
# ]
# ///

import json
from typing import Optional, Dict, Any
from .llm.anth import prompt_llm


def generate_event_summary(event_data: Dict[str, Any]) -> Optional[str]:
    """
    Generate a concise one-sentence summary of a hook event for engineers.

    Args:
        event_data: The hook event data containing event_type, payload, etc.

    Returns:
        str: A one-sentence summary, or None if generation fails
    """
    event_type = event_data.get("hook_event_type", "Unknown")
    payload = event_data.get("payload", {})
    
    # Try LLM-based summarization first
    try:
        # Convert payload to string representation
        payload_str = json.dumps(payload, indent=2)
        if len(payload_str) > 1000:
            payload_str = payload_str[:1000] + "..."

        prompt = f"""Generate a one-sentence summary of this Claude Code hook event payload for an engineer monitoring the system.

Event Type: {event_type}
Payload:
{payload_str}

Requirements:
- ONE sentence only (no period at the end)
- Focus on the key action or information in the payload
- Be specific and technical
- Keep under 15 words
- Use present tense
- No quotes or formatting
- Return ONLY the summary text

Examples:
- Reads configuration file from project root
- Executes npm install to update dependencies
- Searches web for React documentation
- Edits database schema to add user table
- Agent responds with implementation plan

Generate the summary based on the payload:"""

        summary = prompt_llm(prompt)

        # Clean up the response
        if summary:
            summary = summary.strip().strip('"').strip("'").strip(".")
            # Take only the first line if multiple
            summary = summary.split("\n")[0].strip()
            # Ensure it's not too long
            if len(summary) > 100:
                summary = summary[:97] + "..."
            return summary
    except Exception:
        pass  # Fall back to rule-based summarization
    
    # Fallback: Rule-based summarization
    try:
        tool_name = payload.get('tool_name', 'Unknown')
        
        if event_type == 'PreToolUse':
            return f"Pre-tool use event for {tool_name} tool"
        elif event_type == 'PostToolUse':
            return f"Post-tool use event for {tool_name} tool"
        elif event_type == 'Notification':
            message = payload.get('message', 'No message')
            if len(message) > 50:
                message = message[:47] + "..."
            return f"Notification: {message}"
        elif event_type == 'UserPromptSubmit':
            prompt_text = payload.get('prompt', 'No prompt')
            if len(prompt_text) > 50:
                prompt_text = prompt_text[:47] + "..."
            return f"User prompt: {prompt_text}"
        elif event_type == 'Stop':
            return "Claude Code session stopped"
        elif event_type == 'SubagentStop':
            return "Subagent task completed"
        else:
            return f"Unknown event type: {event_type}"
    except Exception:
        return None
