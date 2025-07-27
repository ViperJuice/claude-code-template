#!/usr/bin/env python3
"""Detect programming languages in a project directory."""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import click
from rich.console import Console
from rich.table import Table

# Handle both module and direct execution
if __name__ == '__main__' and __package__ is None:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from claude_setup.utils.colors import Colors, print_banner
    from claude_setup.utils.file_utils import find_files, get_project_root
else:
    from .utils.colors import Colors, print_banner
    from .utils.file_utils import find_files, get_project_root


# Language detection patterns
LANGUAGE_PATTERNS = {
    'rust': {
        'files': ['Cargo.toml'],
        'extensions': ['.rs'],
        'confidence': 1.0,
    },
    'go': {
        'files': ['go.mod', 'go.sum'],
        'extensions': ['.go'],
        'confidence': 1.0,
    },
    'typescript': {
        'files': ['tsconfig.json'],
        'extensions': ['.ts', '.tsx'],
        'dependencies': ['@types/node', 'typescript'],
        'confidence': 0.95,
    },
    'javascript': {
        'files': ['package.json'],
        'extensions': ['.js', '.jsx', '.mjs'],
        'confidence': 0.9,
    },
    'python': {
        'files': ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile'],
        'extensions': ['.py'],
        'confidence': 1.0,
    },
    'cpp': {
        'files': ['CMakeLists.txt'],
        'extensions': ['.cpp', '.cc', '.cxx', '.hpp', '.h++'],
        'confidence': 0.95,
    },
    'c': {
        'files': ['Makefile', 'makefile'],
        'extensions': ['.c', '.h'],
        'confidence': 0.9,
    },
    'dart': {
        'files': ['pubspec.yaml'],
        'extensions': ['.dart'],
        'confidence': 1.0,
    },
    'java': {
        'files': ['pom.xml', 'build.gradle', 'build.gradle.kts'],
        'extensions': ['.java'],
        'confidence': 1.0,
    },
    'kotlin': {
        'files': ['build.gradle.kts'],
        'extensions': ['.kt', '.kts'],
        'confidence': 0.95,
    },
    'csharp': {
        'files': ['*.csproj', '*.sln'],
        'extensions': ['.cs'],
        'confidence': 1.0,
    },
    'fsharp': {
        'files': ['*.fsproj'],
        'extensions': ['.fs', '.fsi', '.fsx'],
        'confidence': 1.0,
    },
    'swift': {
        'files': ['Package.swift'],
        'extensions': ['.swift'],
        'confidence': 1.0,
    },
    'ruby': {
        'files': ['Gemfile', 'Rakefile'],
        'extensions': ['.rb'],
        'confidence': 1.0,
    },
    'php': {
        'files': ['composer.json'],
        'extensions': ['.php'],
        'confidence': 1.0,
    },
    'elixir': {
        'files': ['mix.exs'],
        'extensions': ['.ex', '.exs'],
        'confidence': 1.0,
    },
    'erlang': {
        'files': ['rebar.config'],
        'extensions': ['.erl', '.hrl'],
        'confidence': 1.0,
    },
    'haskell': {
        'files': ['*.cabal', 'stack.yaml'],
        'extensions': ['.hs', '.lhs'],
        'confidence': 1.0,
    },
    'scala': {
        'files': ['build.sbt'],
        'extensions': ['.scala'],
        'confidence': 1.0,
    },
    'clojure': {
        'files': ['project.clj', 'deps.edn'],
        'extensions': ['.clj', '.cljs', '.cljc'],
        'confidence': 1.0,
    },
    'julia': {
        'files': ['Project.toml'],
        'extensions': ['.jl'],
        'confidence': 1.0,
    },
    'r': {
        'files': ['DESCRIPTION', '*.Rproj'],
        'extensions': ['.R', '.r'],
        'confidence': 0.95,
    },
    'lua': {
        'files': ['*.rockspec'],
        'extensions': ['.lua'],
        'confidence': 0.9,
    },
    'perl': {
        'files': ['Makefile.PL', 'Build.PL'],
        'extensions': ['.pl', '.pm'],
        'confidence': 0.9,
    },
    'zig': {
        'files': ['build.zig'],
        'extensions': ['.zig'],
        'confidence': 1.0,
    },
    'nim': {
        'files': ['*.nimble'],
        'extensions': ['.nim'],
        'confidence': 1.0,
    },
    'assembly': {
        'files': ['*.asmproj'],
        'extensions': ['.asm', '.s', '.S'],
        'confidence': 0.8,
    },
    'mojo': {
        'files': ['mojo.toml'],
        'extensions': ['.mojo', '.🔥'],
        'confidence': 1.0,
    },
    'deno': {
        'files': ['deno.json', 'deno.jsonc'],
        'extensions': ['.ts', '.js'],
        'confidence': 0.95,
    }
}


class LanguageDetector:
    """Detect programming languages in a directory."""
    
    def __init__(self, ignore_dirs: Optional[List[str]] = None):
        """Initialize the language detector."""
        self.ignore_dirs = ignore_dirs or [
            '.git', 'node_modules', '__pycache__', 'venv', '.venv',
            'target', 'build', 'dist', 'coverage', '.idea', '.vscode'
        ]
        self.console = Console()
    
    def detect_single_directory(self, directory: Path) -> Dict[str, float]:
        """Detect languages in a single directory."""
        languages = {}
        
        for lang, patterns in LANGUAGE_PATTERNS.items():
            confidence = 0.0
            
            # Check for specific files
            for file_pattern in patterns.get('files', []):
                if '*' in file_pattern:
                    if find_files(file_pattern, directory, self.ignore_dirs):
                        confidence = max(confidence, patterns['confidence'])
                else:
                    if (directory / file_pattern).exists():
                        confidence = max(confidence, patterns['confidence'])
            
            # Check for file extensions
            for ext in patterns.get('extensions', []):
                if find_files(f'*{ext}', directory, self.ignore_dirs):
                    confidence = max(confidence, patterns['confidence'] * 0.8)
            
            # Special case for TypeScript vs JavaScript
            if lang == 'javascript' and 'typescript' in languages:
                continue  # Skip JavaScript if TypeScript is detected
            
            if confidence > 0:
                languages[lang] = confidence
        
        return languages
    
    def detect_recursive(self, root_dir: Path) -> Dict[Path, Dict[str, float]]:
        """Recursively detect languages in all subdirectories."""
        results = {}
        
        # First check the root directory
        root_languages = self.detect_single_directory(root_dir)
        if root_languages:
            results[root_dir] = root_languages
        
        # Check subdirectories
        for subdir in root_dir.iterdir():
            if not subdir.is_dir():
                continue
            
            if subdir.name in self.ignore_dirs:
                continue
            
            # Look for project markers
            project_markers = [
                'Cargo.toml', 'go.mod', 'package.json', 'pom.xml',
                'CMakeLists.txt', 'setup.py', 'pubspec.yaml'
            ]
            
            if any((subdir / marker).exists() for marker in project_markers):
                languages = self.detect_single_directory(subdir)
                if languages:
                    results[subdir] = languages
        
        return results
    
    def get_language_versions(self, directory: Path, language: str) -> Optional[str]:
        """Try to detect the version of a language/framework."""
        version = None
        
        try:
            if language == 'python':
                req_file = directory / 'requirements.txt'
                if req_file.exists():
                    # Simple check for Python version comment
                    content = req_file.read_text()
                    if '# Python' in content:
                        for line in content.split('\n'):
                            if '# Python' in line:
                                version = line.split('# Python')[1].strip()
                                break
            
            elif language == 'node' or language == 'typescript':
                pkg_file = directory / 'package.json'
                if pkg_file.exists():
                    data = json.loads(pkg_file.read_text())
                    engines = data.get('engines', {})
                    if 'node' in engines:
                        version = f"Node {engines['node']}"
            
            # Add more version detection logic as needed
            
        except Exception:
            pass
        
        return version


@click.command()
@click.argument('directories', nargs=-1, type=click.Path(exists=True))
@click.option('--json', 'output_json', is_flag=True, help='Output results as JSON')
@click.option('--recursive', '-r', is_flag=True, help='Recursively scan subdirectories')
@click.option('--confidence', '-c', default=0.5, help='Minimum confidence threshold (0-1)')
@click.option('--versions', '-v', is_flag=True, help='Try to detect language versions')
def main(directories: Tuple[str, ...], output_json: bool, recursive: bool, 
         confidence: float, versions: bool) -> None:
    """Detect programming languages in the specified directories."""
    detector = LanguageDetector()
    
    # Default to current directory if none specified
    if not directories:
        directories = ('.',)
    
    all_results = {}
    
    for dir_path in directories:
        dir_path = Path(dir_path).resolve()
        
        if recursive:
            results = detector.detect_recursive(dir_path)
        else:
            languages = detector.detect_single_directory(dir_path)
            results = {dir_path: languages} if languages else {}
        
        # Filter by confidence threshold
        for path, langs in results.items():
            filtered = {l: c for l, c in langs.items() if c >= confidence}
            if filtered:
                all_results[str(path)] = filtered
    
    # Add version information if requested
    if versions:
        for path_str, languages in all_results.items():
            path = Path(path_str)
            for lang in languages:
                version = detector.get_language_versions(path, lang)
                if version:
                    all_results[path_str][f"{lang}_version"] = version
    
    # Output results
    if output_json:
        print(json.dumps(all_results, indent=2))
    else:
        if not all_results:
            print(f"{Colors.YELLOW}No languages detected with confidence >= {confidence}{Colors.RESET}")
            return
        
        # Create a table for pretty output
        table = Table(title="Detected Languages")
        table.add_column("Directory", style="cyan")
        table.add_column("Language", style="green")
        table.add_column("Confidence", style="yellow")
        
        for path, languages in all_results.items():
            rel_path = Path(path).relative_to(Path.cwd())
            for lang, conf in sorted(languages.items(), key=lambda x: x[1], reverse=True):
                if not lang.endswith('_version'):
                    table.add_row(str(rel_path), lang, f"{conf:.0%}")
        
        detector.console.print(table)


if __name__ == '__main__':
    main()