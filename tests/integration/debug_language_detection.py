#!/usr/bin/env python3
import os
import sys
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.claude/scripts'))

from claude_setup.detect_language import LanguageDetector

with tempfile.TemporaryDirectory() as tmpdir:
    # Create nested structure
    backend = Path(tmpdir) / "backend" / "api"
    backend.mkdir(parents=True)
    (backend / "Cargo.toml").write_text('[package]\nname = "api"')
    
    frontend = Path(tmpdir) / "frontend" / "web"
    frontend.mkdir(parents=True)
    (frontend / "package.json").write_text('{"name": "web"}')
    
    detector = LanguageDetector()
    results = detector.detect_recursive(Path(tmpdir))
    
    print("\nResults:")
    for path, langs in results.items():
        print(f"{path}: {langs}")