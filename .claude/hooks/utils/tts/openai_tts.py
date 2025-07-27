#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "openai",
#     "playsound",
# ]
# ///

"""
OpenAI Text-to-Speech for Claude Code hooks.
Works in WSL by saving audio to file and playing it.
"""

import sys
import os
import tempfile
import openai


def text_to_speech(text: str, voice: str = "alloy"):
    """
    Convert text to speech using OpenAI TTS API.
    
    Args:
        text: The text to convert to speech
        voice: The voice to use (alloy, echo, fable, onyx, nova, shimmer)
    """
    try:
        # Set API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("OPENAI_API_KEY not set", file=sys.stderr)
            return
        
        client = openai.OpenAI(api_key=api_key)
        
        # Generate audio
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            temp_path = temp_file.name
            temp_file.write(response.content)
        
        # Play the audio file
        try:
            from playsound import playsound
            playsound(temp_path)
        except ImportError:
            # Fallback to system command
            import subprocess
            subprocess.run(['mpg123', temp_path], capture_output=True, timeout=10)
        except Exception:
            # Try other audio players
            for player in ['aplay', 'paplay', 'ffplay']:
                try:
                    subprocess.run([player, temp_path], capture_output=True, timeout=10)
                    break
                except (subprocess.SubprocessError, FileNotFoundError):
                    continue
        
        # Clean up temporary file
        try:
            os.unlink(temp_path)
        except:
            pass
            
    except Exception as e:
        # Fail silently - don't break the hook if TTS fails
        print(f"OpenAI TTS Error: {e}", file=sys.stderr)


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python openai_tts.py <text> [voice]", file=sys.stderr)
        sys.exit(1)
    
    # Get text from command line arguments
    text = " ".join(sys.argv[1:-1]) if len(sys.argv) > 2 else sys.argv[1]
    voice = sys.argv[-1] if len(sys.argv) > 2 else "alloy"
    
    if text.strip():
        text_to_speech(text, voice)


if __name__ == "__main__":
    main() 