#!/usr/bin/env python3
"""Integration tests for language detection functionality"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.claude/scripts'))

from claude_setup.detect_language import LanguageDetector

def test_single_language_detection():
    """Test detection of single language projects"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create Rust project
        cargo_toml = Path(tmpdir) / "Cargo.toml"
        cargo_toml.write_text('[package]\nname = "test"\nversion = "0.1.0"')
        
        src_dir = Path(tmpdir) / "src"
        src_dir.mkdir()
        (src_dir / "main.rs").write_text('fn main() { println!("Hello"); }')
        
        detector = LanguageDetector()
        results = detector.detect_single_directory(Path(tmpdir))
        
        assert 'rust' in results
        assert results['rust'] >= 0.9
        print("✓ Single language detection passed")

def test_multi_language_detection():
    """Test detection of multi-language projects"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create Go service
        go_dir = Path(tmpdir) / "service-a"
        go_dir.mkdir()
        (go_dir / "go.mod").write_text('module service-a\n\ngo 1.21')
        (go_dir / "main.go").write_text('package main\n\nfunc main() {}')
        
        # Create Python service
        py_dir = Path(tmpdir) / "service-b"
        py_dir.mkdir()
        (py_dir / "requirements.txt").write_text('fastapi==0.100.0')
        (py_dir / "main.py").write_text('def main(): pass')
        
        # Create TypeScript service
        ts_dir = Path(tmpdir) / "service-c"
        ts_dir.mkdir()
        (ts_dir / "package.json").write_text('{"name": "service-c"}')
        (ts_dir / "index.ts").write_text('export function main() {}')
        
        detector = LanguageDetector()
        results = detector.detect_recursive(Path(tmpdir))
        
        all_languages = set()
        for langs in results.values():
            all_languages.update(langs.keys())
        
        assert 'go' in all_languages
        assert 'python' in all_languages
        assert 'typescript' in all_languages or 'javascript' in all_languages
        print("✓ Multi-language detection passed")

def test_nested_project_detection():
    """Test detection in nested directory structures"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create nested structure
        # Create first project
        proj1 = Path(tmpdir) / "project1"
        proj1.mkdir()
        (proj1 / "Cargo.toml").write_text('[package]\nname = "project1"')
        (proj1 / "src").mkdir()
        (proj1 / "src" / "main.rs").write_text('fn main() {}')
        
        # Create second project
        proj2 = Path(tmpdir) / "project2"
        proj2.mkdir()
        (proj2 / "go.mod").write_text('module project2\n\ngo 1.21')
        (proj2 / "main.go").write_text('package main')
        
        detector = LanguageDetector()
        results = detector.detect_recursive(Path(tmpdir))
        
        # Get all detected languages
        all_languages = set()
        for langs in results.values():
            all_languages.update(langs.keys())
        
        assert len(results) >= 2  # At least two projects detected
        assert 'rust' in all_languages
        assert 'go' in all_languages
        print("✓ Nested project detection passed")

def test_confidence_scoring():
    """Test confidence scoring for language detection"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create project with strong language indicators
        proj = Path(tmpdir) / "proj"
        proj.mkdir()
        (proj / "go.mod").write_text('module test')
        (proj / "main.go").write_text('package main')
        
        # Create project with weaker/mixed indicators
        mixed = Path(tmpdir) / "mixed"
        mixed.mkdir()
        (mixed / "script.txt").write_text('// Some code')
        
        detector = LanguageDetector()
        
        # Test strong indicators
        strong_results = detector.detect_single_directory(proj)
        assert 'go' in strong_results
        assert strong_results['go'] >= 0.9
        
        # Test weak indicators
        weak_results = detector.detect_single_directory(mixed)
        assert len(weak_results) == 0 or all(conf < 0.9 for conf in weak_results.values())
        print("✓ Confidence scoring passed")

if __name__ == "__main__":
    print("Running language detection integration tests...")
    
    try:
        test_single_language_detection()
        test_multi_language_detection()
        test_nested_project_detection()
        test_confidence_scoring()
        print("\n✅ All tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)