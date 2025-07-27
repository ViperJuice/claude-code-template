#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "elevenlabs",
#     "playsound",
# ]
# ///

"""
ElevenLabs Text-to-Speech for Claude Code hooks.
Works in WSL by saving audio to file and playing it.
"""

import sys
import os
import tempfile
from elevenlabs import generate, save, set_api_key
from elevenlabs import voices


def text_to_speech(text: str, voice_name: str = "Rachel"):
    """
    Convert text to speech using ElevenLabs API.
    
    Args:
        text: The text to convert to speech
        voice_name: The voice to use (default: Rachel)
    """
    try:
        # Set API key
        api_key = os.getenv('ELEVENLABS_API_KEY')
        if not api_key:
            print("ELEVENLABS_API_KEY not set", file=sys.stderr)
            return
        
        set_api_key(api_key)
        
        # Generate audio
        audio = generate(
            text=text,
            voice=voice_name,
            model="eleven_monolingual_v1"
        )
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            temp_path = temp_file.name
            save(audio, temp_path)
        
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
        print(f"ElevenLabs TTS Error: {e}", file=sys.stderr)


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python elevenlabs_tts.py <text> [voice_name]", file=sys.stderr)
        sys.exit(1)
    
    # Get text from command line arguments
    text = " ".join(sys.argv[1:-1]) if len(sys.argv) > 2 else sys.argv[1]
    voice_name = sys.argv[-1] if len(sys.argv) > 2 else "Rachel"
    
    if text.strip():
        text_to_speech(text, voice_name)


if __name__ == "__main__":
    main() 