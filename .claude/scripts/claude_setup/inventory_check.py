#!/usr/bin/env python3
"""Check which Claude Code files are present and validate setup."""

import json
from pathlib import Path
from typing import Dict, List, Tuple

import click
from rich.console import Console
from rich.table import Table
from rich.tree import Tree

from .config import get_config, AGENT_DEFINITIONS
from .utils.colors import Colors, success, error, warning
from .utils.file_utils import get_project_root


class InventoryChecker:
    """Check and validate Claude Code installation."""
    
    def __init__(self):
        """Initialize the inventory checker."""
        self.project_root = get_project_root()
        self.claude_dir = self.project_root / '.claude'
        self.console = Console()
        self.results: Dict[str, List[Tuple[str, bool, str]]] = {}
    
    def check_file(self, filepath: Path, category: str, description: str = "") -> bool:
        """Check if a file exists and record the result."""
        exists = filepath.exists()
        relative_path = filepath.relative_to(self.project_root)
        
        if category not in self.results:
            self.results[category] = []
        
        self.results[category].append((str(relative_path), exists, description))
        return exists
    
    def check_directory(self, dirpath: Path, category: str, description: str = "") -> bool:
        """Check if a directory exists and record the result."""
        exists = dirpath.exists() and dirpath.is_dir()
        relative_path = dirpath.relative_to(self.project_root)
        
        if category not in self.results:
            self.results[category] = []
        
        self.results[category].append((str(relative_path) + "/", exists, description))
        return exists
    
    def check_core_structure(self) -> None:
        """Check core directory structure."""
        self.check_directory(self.claude_dir, "Core", "Claude Code root directory")
        self.check_directory(self.claude_dir / 'agents', "Core", "Agent definitions")
        self.check_directory(self.claude_dir / 'commands', "Core", "Slash commands")
        self.check_directory(self.claude_dir / 'scripts', "Core", "Helper scripts")
        self.check_directory(self.claude_dir / 'state', "Core", "Runtime state")
        self.check_directory(self.project_root / 'worktrees', "Core", "Git worktrees")
        self.check_directory(self.project_root / 'specs', "Core", "Project specifications")
    
    def check_agents(self) -> None:
        """Check for agent files."""
        for agent_name, agent_def in AGENT_DEFINITIONS.items():
            agent_path = self.claude_dir / 'agents' / f'{agent_name}.md'
            self.check_file(agent_path, "Agents", agent_def['description'])
    
    def check_commands(self) -> None:
        """Check for command files."""
        self.check_file(
            self.claude_dir / 'commands' / 'phase-breakdown.md',
            "Commands",
            "Main phase execution command"
        )
    
    def check_scripts(self) -> None:
        """Check for script files."""
        # Check Python scripts
        script_dir = self.claude_dir / 'scripts' / 'claude_setup'
        self.check_file(script_dir / 'setup_native_subagents.py', "Scripts", "Setup script (Python)")
        self.check_file(script_dir / 'detect_language.py', "Scripts", "Language detection (Python)")
        self.check_file(script_dir / 'inventory_check.py', "Scripts", "Inventory checker (Python)")
        self.check_file(script_dir / 'cleanup_legacy.py', "Scripts", "Legacy cleanup (Python)")
        
        # Check bash wrappers
        self.check_file(self.claude_dir / 'scripts' / 'setup-native-subagents.sh', "Scripts", "Setup wrapper")
        self.check_file(self.claude_dir / 'scripts' / 'detect-language.sh', "Scripts", "Language detection wrapper")
    
    def check_configuration(self) -> None:
        """Check configuration files."""
        self.check_file(self.claude_dir / 'config.json', "Configuration", "Main configuration")
        self.check_file(self.claude_dir / '.gitignore', "Configuration", "Git ignore rules")
        self.check_file(self.claude_dir / 'state' / '.gitkeep', "Configuration", "State directory keeper")
    
    def check_cicd(self) -> None:
        """Check CI/CD files."""
        self.check_directory(self.project_root / '.github', "CI/CD", "GitHub directory")
        self.check_directory(self.project_root / '.github' / 'workflows', "CI/CD", "Workflows directory")
        self.check_file(
            self.project_root / '.github' / 'workflows' / 'multi-language-ci.yml',
            "CI/CD",
            "Multi-language CI workflow"
        )
        self.check_file(self.project_root / 'docker-compose.yml', "CI/CD", "Docker Compose config")
        self.check_file(self.project_root / 'Makefile', "CI/CD", "Master Makefile")
    
    def check_documentation(self) -> None:
        """Check documentation files."""
        self.check_file(self.project_root / 'README.md', "Documentation", "Project README")
        self.check_file(self.project_root / 'CHANGELOG.md', "Documentation", "Change log")
        self.check_file(self.project_root / 'specs' / 'ROADMAP.md', "Documentation", "Project roadmap")
        
        # Check doc directories
        doc_dirs = ['api', 'architecture', 'services', 'migration', 'guides']
        for doc_dir in doc_dirs:
            self.check_directory(
                self.project_root / 'docs' / doc_dir,
                "Documentation",
                f"{doc_dir.capitalize()} documentation"
            )
    
    def check_legacy_files(self) -> List[Path]:
        """Check for legacy Python orchestration files."""
        legacy_patterns = [
            '.claude/**/*.py',
            '.claude/orchestration',
            '.claude/phase-manager*',
            '.claude/agent-mesh*',
            '.claude/**/*orchestrat*',
            '.claude/playbooks/*.yaml',
            '.claude/contracts',
        ]
        
        legacy_files = []
        for pattern in legacy_patterns:
            # Skip our new Python scripts
            if 'claude_setup' in pattern:
                continue
            
            for path in self.project_root.glob(pattern):
                if path.is_file() and 'claude_setup' not in str(path):
                    legacy_files.append(path)
        
        return legacy_files
    
    def generate_text_report(self) -> str:
        """Generate a text report of the inventory check."""
        lines = []
        lines.append("🔍 Claude Code Template Inventory Check")
        lines.append("=" * 50)
        lines.append("")
        
        total_files = 0
        missing_files = 0
        
        for category, items in self.results.items():
            lines.append(f"\n{category}:")
            for filepath, exists, description in items:
                total_files += 1
                if exists:
                    status = f"{Colors.GREEN}✓{Colors.RESET}"
                else:
                    status = f"{Colors.RED}✗{Colors.RESET}"
                    missing_files += 1
                
                if description:
                    lines.append(f"{status} {filepath} - {description}")
                else:
                    lines.append(f"{status} {filepath}")
        
        # Check for legacy files
        legacy_files = self.check_legacy_files()
        if legacy_files:
            lines.append(f"\n{Colors.YELLOW}⚠ Legacy Files Found:{Colors.RESET}")
            for legacy_file in legacy_files[:10]:  # Show first 10
                lines.append(f"  - {legacy_file.relative_to(self.project_root)}")
            if len(legacy_files) > 10:
                lines.append(f"  ... and {len(legacy_files) - 10} more")
        
        # Summary
        lines.append("\n" + "=" * 50)
        lines.append(f"Total items checked: {total_files}")
        lines.append(f"Missing items: {missing_files}")
        
        health_score = ((total_files - missing_files) / total_files * 100) if total_files > 0 else 0
        lines.append(f"Health score: {health_score:.0f}%")
        
        if missing_files > 0:
            lines.append(f"\n{Colors.YELLOW}Run setup script to create missing files:{Colors.RESET}")
            lines.append("  ./.claude/scripts/setup-native-subagents.sh")
        
        return "\n".join(lines)
    
    def generate_json_report(self) -> Dict:
        """Generate a JSON report of the inventory check."""
        report = {
            "project_root": str(self.project_root),
            "categories": {},
            "summary": {
                "total_items": 0,
                "missing_items": 0,
                "health_score": 0
            },
            "legacy_files": []
        }
        
        total = 0
        missing = 0
        
        for category, items in self.results.items():
            report["categories"][category] = []
            for filepath, exists, description in items:
                total += 1
                if not exists:
                    missing += 1
                
                report["categories"][category].append({
                    "path": filepath,
                    "exists": exists,
                    "description": description
                })
        
        # Add legacy files
        legacy_files = self.check_legacy_files()
        report["legacy_files"] = [str(f.relative_to(self.project_root)) for f in legacy_files]
        
        # Update summary
        report["summary"]["total_items"] = total
        report["summary"]["missing_items"] = missing
        report["summary"]["health_score"] = ((total - missing) / total * 100) if total > 0 else 0
        
        return report
    
    def run_full_check(self) -> None:
        """Run all inventory checks."""
        self.check_core_structure()
        self.check_agents()
        self.check_commands()
        self.check_scripts()
        self.check_configuration()
        self.check_cicd()
        self.check_documentation()


@click.command()
@click.option('--format', '-f', type=click.Choice(['text', 'json', 'tree']), 
              default='text', help='Output format')
@click.option('--fix', is_flag=True, help='Attempt to fix missing items')
@click.option('--check-legacy', is_flag=True, help='Check for legacy files')
def main(format: str, fix: bool, check_legacy: bool) -> None:
    """Check which Claude Code files are present and validate setup."""
    checker = InventoryChecker()
    checker.run_full_check()
    
    if format == 'json':
        report = checker.generate_json_report()
        print(json.dumps(report, indent=2))
    elif format == 'tree':
        # Create a tree view
        tree = Tree("📁 Claude Code Template")
        
        # Add categories as branches
        for category, items in checker.results.items():
            branch = tree.add(f"[bold]{category}[/bold]")
            for filepath, exists, description in items:
                icon = "✅" if exists else "❌"
                if description:
                    branch.add(f"{icon} {filepath} [dim]({description})[/dim]")
                else:
                    branch.add(f"{icon} {filepath}")
        
        checker.console.print(tree)
    else:
        print(checker.generate_text_report())
    
    if fix:
        checker.console.print("\n[yellow]Auto-fix feature coming soon![/yellow]")
        checker.console.print("For now, run: ./.claude/scripts/setup-native-subagents.sh")


if __name__ == '__main__':
    main()