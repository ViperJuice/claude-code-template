#!/usr/bin/env python3
"""
A standalone Tree-sitter based code analyzer for interface extraction.
This can be used for ad-hoc analysis or integrated into agents.
This script is a simplified version of what the `treesitter-chunker` library provides.
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Any
# This script requires `tree-sitter` and language-specific grammars to be installed.
# e.g., pip install tree-sitter tree-sitter-languages
from tree_sitter import Language, Parser
from tree_sitter_languages import get_language, get_parser

class CodebaseAnalyzer:
    """Analyzes codebases using tree-sitter."""

    def __init__(self):
        """Initializes the analyzer."""
        self.parsers = {}

    def _get_parser(self, language_name: str) -> Parser | None:
        """Initializes and returns a parser for a given language."""
        if language_name in self.parsers:
            return self.parsers[language_name]
        
        try:
            language = get_language(language_name)
            parser = get_parser(language_name)
            self.parsers[language_name] = parser
            return parser
        except Exception:
            # Language not supported or grammar not found
            return None

    def extract_from_file(self, file_path: str) -> Dict[str, Any]:
        """Extracts interfaces, classes, and functions from a single file."""
        language = self._detect_language(file_path)
        parser = self._get_parser(language)
        if not parser:
            return {}

        with open(file_path, 'rb') as f:
            content = f.read()
        
        tree = parser.parse(content)
        return self._extract_by_language(tree, language, content)

    def _extract_by_language(self, tree, language: str, content: bytes) -> Dict[str, Any]:
        """Language-specific extraction logic."""
        # This is where you would put language-specific queries
        # For simplicity, we'll use a generic approach
        results = {"classes": [], "functions": []}
        
        # Example query for Python functions
        if language == 'python':
            query = get_language(language).query("(function_definition name: (identifier) @name)")
            captures = query.captures(tree.root_node)
            for node, name in captures:
                if name == 'name':
                    results["functions"].append({
                        'name': content[node.start_byte:node.end_byte].decode('utf-8'),
                        'start': node.start_point,
                        'end': node.end_point
                    })
        return results

    def analyze_codebase(self, root_path: str) -> Dict[str, Any]:
        """Analyzes an entire codebase directory."""
        all_results = {"files": {}}
        for file_path in Path(root_path).rglob('*'):
            if file_path.is_file() and self._is_source_file(file_path):
                relative_path = str(file_path.relative_to(root_path))
                file_results = self.extract_from_file(str(file_path))
                if file_results:
                    all_results['files'][relative_path] = file_results
        return all_results

    def _detect_language(self, file_path: str) -> str:
        """Detects programming language from file extension."""
        ext_map = {
            '.ts': 'typescript', '.tsx': 'typescript',
            '.js': 'javascript', '.jsx': 'javascript',
            '.go': 'go', '.rs': 'rust', '.py': 'python',
            '.java': 'java', '.cpp': 'cpp', '.c': 'c'
        }
        ext = Path(file_path).suffix
        return ext_map.get(ext, 'unknown')

    def _is_source_file(self, file_path: Path) -> bool:
        """Checks if a file is a recognized source code file."""
        source_extensions = {'.ts', '.js', '.py', '.go', '.rs', '.java', '.cpp', '.c', '.h'}
        return file_path.suffix in source_extensions

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python tree_sitter_analyzer.py <project_root>")
        sys.exit(1)
    
    project_root = sys.argv[1]
    analyzer = CodebaseAnalyzer()
    results = analyzer.analyze_codebase(project_root)
    
    output_path = '.claude/state/manual-tree-sitter-analysis.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Analysis complete. Results saved to {output_path}")
