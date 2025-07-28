#!/usr/bin/env python3
"""
Pattern Matcher - Analyzes code context and suggests appropriate design patterns.

This script is used by agents to:
1. Analyze the current code context
2. Match against known design patterns for the language
3. Suggest the most appropriate patterns for the situation
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional


class PatternMatcher:
    """Matches code contexts to appropriate design patterns."""
    
    def __init__(self, language: str):
        self.language = language.lower()
        self.patterns = self._load_patterns()
        
    def _load_patterns(self) -> Dict[str, Any]:
        """Load patterns for the specified language."""
        patterns_dir = Path(__file__).parent.parent / "knowledge" / "patterns"
        pattern_file = patterns_dir / f"{self.language}-patterns.json"
        
        if not pattern_file.exists():
            print(f"Warning: No patterns found for {self.language}", file=sys.stderr)
            return {}
            
        with open(pattern_file, 'r') as f:
            data = json.load(f)
            return data.get('patterns', {})
    
    def analyze_context(self, code_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze code context and suggest appropriate patterns.
        
        Args:
            code_context: Dictionary containing:
                - file_content: Current file content
                - file_path: Path to the file
                - task_description: What the developer is trying to achieve
                - existing_patterns: Patterns already in use
        
        Returns:
            List of suggested patterns with relevance scores
        """
        suggestions = []
        
        file_content = code_context.get('file_content', '')
        task_desc = code_context.get('task_description', '').lower()
        existing = set(code_context.get('existing_patterns', []))
        
        # Keywords that might indicate pattern usage
        pattern_indicators = {
            'singleton': ['instance', 'global', 'single', 'shared'],
            'factory': ['create', 'instantiate', 'build', 'construct'],
            'observer': ['notify', 'subscribe', 'event', 'listener', 'watch'],
            'strategy': ['algorithm', 'policy', 'behavior', 'switch'],
            'builder': ['configure', 'option', 'parameter', 'construct'],
            'iterator': ['traverse', 'iterate', 'collection', 'sequence'],
            'decorator': ['wrap', 'enhance', 'extend', 'modify'],
            'adapter': ['convert', 'adapt', 'interface', 'compatibility'],
            'command': ['execute', 'undo', 'queue', 'operation'],
            'repository': ['database', 'storage', 'persist', 'query'],
            'middleware': ['chain', 'pipeline', 'intercept', 'filter'],
            'error': ['error', 'exception', 'failure', 'handle'],
        }
        
        # Score patterns based on context
        for pattern_name, pattern_info in self.patterns.items():
            if pattern_name in existing:
                continue
                
            score = 0
            reasons = []
            
            # Check task description
            if pattern_name in pattern_indicators:
                for keyword in pattern_indicators[pattern_name]:
                    if keyword in task_desc:
                        score += 20
                        reasons.append(f"Task mentions '{keyword}'")
            
            # Check when to use
            when_to_use = pattern_info.get('whenToUse', '').lower()
            task_words = set(task_desc.split())
            when_words = set(when_to_use.split())
            common_words = task_words & when_words
            if common_words:
                score += 10 * len(common_words)
                reasons.append(f"Matches use case: {', '.join(common_words)}")
            
            # Language-specific checks
            if self.language == 'go':
                if pattern_name == 'functional_options' and 'option' in task_desc:
                    score += 30
                    reasons.append("Go idiomatic for optional parameters")
                elif pattern_name == 'error_wrapping' and 'error' in task_desc:
                    score += 25
                    reasons.append("Go idiomatic error handling")
            elif self.language == 'rust':
                if pattern_name == 'builder' and 'optional' in task_desc:
                    score += 25
                    reasons.append("Rust idiomatic for complex construction")
                elif pattern_name == 'typestate' and 'state' in task_desc:
                    score += 30
                    reasons.append("Rust compile-time state validation")
            
            # Add suggestion if score is significant
            if score > 0:
                suggestions.append({
                    'pattern': pattern_name,
                    'score': score,
                    'reasons': reasons,
                    'description': pattern_info.get('description', ''),
                    'example': pattern_info.get('example', '')
                })
        
        # Sort by score
        suggestions.sort(key=lambda x: x['score'], reverse=True)
        return suggestions[:5]  # Return top 5 suggestions
    
    def get_pattern_example(self, pattern_name: str) -> Optional[str]:
        """Get the example code for a specific pattern."""
        pattern = self.patterns.get(pattern_name)
        if pattern:
            return pattern.get('example', '')
        return None
    
    def get_pattern_info(self, pattern_name: str) -> Optional[Dict[str, Any]]:
        """Get full information about a specific pattern."""
        return self.patterns.get(pattern_name)


def main():
    """CLI interface for pattern matching."""
    if len(sys.argv) < 2:
        print("Usage: pattern_matcher.py <language> [command] [args...]", file=sys.stderr)
        print("Commands:", file=sys.stderr)
        print("  analyze <task_description> - Suggest patterns for a task", file=sys.stderr)
        print("  example <pattern_name> - Get example code for a pattern", file=sys.stderr)
        print("  list - List all patterns for the language", file=sys.stderr)
        sys.exit(1)
    
    language = sys.argv[1]
    matcher = PatternMatcher(language)
    
    if len(sys.argv) < 3:
        command = "list"
    else:
        command = sys.argv[2]
    
    if command == "analyze":
        if len(sys.argv) < 4:
            print("Error: analyze requires task description", file=sys.stderr)
            sys.exit(1)
        
        task_desc = " ".join(sys.argv[3:])
        context = {"task_description": task_desc}
        suggestions = matcher.analyze_context(context)
        
        print(json.dumps(suggestions, indent=2))
        
    elif command == "example":
        if len(sys.argv) < 4:
            print("Error: example requires pattern name", file=sys.stderr)
            sys.exit(1)
        
        pattern_name = sys.argv[3]
        example = matcher.get_pattern_example(pattern_name)
        if example:
            print(example)
        else:
            print(f"No example found for pattern '{pattern_name}'", file=sys.stderr)
            sys.exit(1)
            
    elif command == "list":
        patterns = list(matcher.patterns.keys())
        print(json.dumps(patterns, indent=2))
        
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()