#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "pyttsx3",
# ]
# ///

"""
pyttsx3 Text-to-Speech for Claude Code hooks.
Works in WSL with PortAudio backend.
"""

import sys
import pyttsx3
import os


def text_to_speech(text: str):
    """
    Convert text to speech using pyttsx3.
    
    Args:
        text: The text to convert to speech
    """
    try:
        # Initialize the TTS engine
        engine = pyttsx3.init()
        
        # Configure voice settings
        engine.setProperty('rate', 150)    # Speed of speech
        engine.setProperty('volume', 0.8)  # Volume (0.0 to 1.0)
        
        # Try to set a good voice
        voices = engine.getProperty('voices')
        if voices:
            # Prefer female voices if available
            for voice in voices:
                if 'female' in voice.name.lower() or 'samantha' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
            else:
                # Use first available voice
                engine.setProperty('voice', voices[0].id)
        
        # Convert text to speech
        engine.say(text)
        engine.runAndWait()
        
    except Exception as e:
        # Fail silently - don't break the hook if TTS fails
        print(f"TTS Error: {e}", file=sys.stderr)


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python pyttsx3_tts.py <text>", file=sys.stderr)
        sys.exit(1)
    
    # Get text from command line arguments
    text = " ".join(sys.argv[1:])
    
    if text.strip():
        text_to_speech(text)


if __name__ == "__main__":
    main() 