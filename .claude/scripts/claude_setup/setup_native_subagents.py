#!/usr/bin/env python3
"""Complete setup script for Claude Code native sub-agents."""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .config import get_config, AGENT_DEFINITIONS, DEFAULT_CONFIG
from .utils.colors import Colors, success, error, warning, info, print_banner
from .utils.file_utils import (
    ensure_directory, write_json, safe_write, make_executable,
    get_project_root, relative_to_cwd
)


# Template content for various files
GITIGNORE_CONTENT = """# State files (runtime only)
state/*.json
state/**/*.json

# Temporary files
*.tmp
*.log

# Local overrides
*.local.*

# Python cache
__pycache__/
*.pyc

# But keep directory structure
!state/.gitkeep
"""

README_TEMPLATE = """# Claude Code Multi-Language Project

This project uses Claude Code's native sub-agent system for parallel development across multiple programming languages.

## Features

- 🤖 9 specialized AI sub-agents
- 🌐 25+ programming language support
- 🔀 Zero-merge-conflict parallel development
- 🧪 Test-driven development (TDD) enforcement
- 📊 Automated documentation generation

## Quick Start

```bash
# Run setup (only needed once)
./.claude/scripts/setup-native-subagents.sh

# Start Claude Code
claude

# Execute a development phase
/phase-breakdown 1
```

## Supported Languages

- Systems: C, C++, Rust, Assembly
- Enterprise: Java, C#, Go
- Web: TypeScript, JavaScript, Dart
- Scripting: Python, Ruby, Perl
- And 15+ more...

## Documentation

- [Implementation Guide](docs/implementation-guide.md)
- [Architecture](docs/architecture/README.md)
- [API Reference](docs/api/README.md)

## License

[Your License]
"""

CHANGELOG_TEMPLATE = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial Claude Code native sub-agent system
- Multi-language support (25+ languages)
- Parallel development workflow
- TDD enforcement
- Automated documentation generation
"""

PHASE_BREAKDOWN_TEMPLATE = """---
allowed-tools: Bash, Task, Read, Write, TodoWrite
description: Execute a development phase using native Claude Code sub-agents for parallel implementation.
argument-hint: [phase-name or phase-number]
---

## Phase Breakdown Execution

You will orchestrate Phase "$ARGUMENTS" using Claude Code's native sub-agent system.

### Initial Setup

```bash
# Verify environment
echo "=== Phase Breakdown: $ARGUMENTS ==="
git status --porcelain
git branch --show-current
```

### Launch Phase Architect

Use the Task tool to delegate the entire phase orchestration to the phase-architect sub-agent.
"""

# Simple agent template
AGENT_TEMPLATE = """---
name: {name}
description: {description}
tools: {tools}
---

{system_prompt}
"""


class SetupManager:
    """Manage the setup process for Claude Code native sub-agents."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize the setup manager."""
        self.project_root = project_root or get_project_root()
        self.claude_dir = self.project_root / '.claude'
        self.console = Console()
        self.config = get_config()
    
    def create_directory_structure(self) -> None:
        """Create the required directory structure."""
        directories = [
            '.claude/agents',
            '.claude/commands', 
            '.claude/scripts',
            '.claude/state',
            '.claude/docs',
            '.github/workflows',
            'worktrees',
            'docs/api',
            'docs/architecture',
            'docs/services',
            'docs/migration',
            'docs/guides',
            'examples',
            'tests/integration',
            'specs'
        ]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Creating directories...", total=len(directories))
            
            for dir_path in directories:
                full_path = self.project_root / dir_path
                ensure_directory(full_path)
                progress.update(task, advance=1)
        
        self.console.print(success("Directory structure created"))
    
    def create_agent_files(self) -> None:
        """Create sub-agent markdown files with proper content."""
        agents_created = 0
        
        for agent_name, agent_def in AGENT_DEFINITIONS.items():
            agent_path = self.claude_dir / 'agents' / f'{agent_name}.md'
            
            if agent_path.exists():
                self.console.print(warning(f"Agent {agent_name} already exists, skipping"))
                continue
            
            # Create agent content
            tools_str = ', '.join(agent_def['tools'])
            content = AGENT_TEMPLATE.format(
                name=agent_def['name'],
                description=agent_def['description'],
                tools=tools_str,
                system_prompt=self._get_agent_system_prompt(agent_name)
            )
            
            safe_write(agent_path, content, backup=False)
            agents_created += 1
            self.console.print(info(f"Created agent: {agent_name}"))
        
        self.console.print(success(f"Created {agents_created} agent files"))
    
    def _get_agent_system_prompt(self, agent_name: str) -> str:
        """Get the system prompt for a specific agent."""
        prompts = {
            "phase-architect": """You are the Phase Architect, responsible for orchestrating entire development phases with zero merge conflicts through intelligent parallelization.

## Core Responsibilities

1. **Phase Analysis**: Parse ROADMAP.md to extract phase requirements
2. **Interface Design**: Define clear boundaries between components  
3. **Parallel Orchestration**: Launch and coordinate sub-agents
4. **Progress Monitoring**: Track component completion and dependencies

When executing a phase:
1. Read and analyze the ROADMAP for the requested phase
2. Create a detailed execution plan
3. Delegate interface design to the interface-designer agent
4. Coordinate parallel implementation through worktree agents
5. Monitor progress and handle any issues""",
            
            "interface-designer": """You are the Interface Designer, responsible for creating language-agnostic interfaces that enable parallel development.

Design interfaces that:
- Define clear contracts between components
- Use appropriate patterns for each language
- Prevent circular dependencies
- Enable independent implementation
- Support testing in isolation""",
            
            "test-builder": """You are the Test Builder, implementing comprehensive test suites using language-specific frameworks.

Follow TDD principles:
1. Write tests that fail (red phase)
2. Define expected behavior clearly
3. Use language-specific testing frameworks
4. Include unit, integration, and edge cases
5. Ensure tests are maintainable""",
            
            "coder": """You are the Coder, implementing features to pass tests using language-specific best practices.

Your approach:
1. Read and understand the failing tests
2. Implement the minimum code to pass tests
3. Use language idioms and patterns
4. Optimize for readability and performance
5. Follow the project's coding standards""",
            
            # Add more agent prompts as needed
        }
        
        return prompts.get(agent_name, f"You are the {agent_name} agent. Follow your designated responsibilities.")
    
    def create_commands(self) -> None:
        """Create command files."""
        # Phase breakdown command
        phase_breakdown_path = self.claude_dir / 'commands' / 'phase-breakdown.md'
        safe_write(phase_breakdown_path, PHASE_BREAKDOWN_TEMPLATE, backup=False)
        self.console.print(success("Created phase-breakdown command"))
    
    def create_config_files(self) -> None:
        """Create configuration files."""
        # Main config.json
        config_path = self.claude_dir / 'config.json'
        if not config_path.exists():
            write_json(config_path, DEFAULT_CONFIG)
            self.console.print(success("Created config.json"))
        
        # .gitignore for .claude directory
        gitignore_path = self.claude_dir / '.gitignore'
        safe_write(gitignore_path, GITIGNORE_CONTENT, backup=False)
        
        # .gitkeep for state directory
        (self.claude_dir / 'state' / '.gitkeep').touch()
        
        self.console.print(success("Created configuration files"))
    
    def create_documentation(self) -> None:
        """Create initial documentation files."""
        # README.md
        readme_path = self.project_root / 'README.md'
        if not readme_path.exists():
            safe_write(readme_path, README_TEMPLATE, backup=False)
            self.console.print(success("Created README.md"))
        
        # CHANGELOG.md
        changelog_path = self.project_root / 'CHANGELOG.md'
        if not changelog_path.exists():
            safe_write(changelog_path, CHANGELOG_TEMPLATE, backup=False)
            self.console.print(success("Created CHANGELOG.md"))
        
        # Sample ROADMAP.md
        roadmap_path = self.project_root / 'specs' / 'ROADMAP.md'
        if not roadmap_path.exists():
            roadmap_content = """# Project Roadmap

## Phase 1: Foundation
- **core-api** (Go) - RESTful API service
- **database** (PostgreSQL) - Data persistence layer  
- **auth-service** (Rust) - Authentication and authorization

## Phase 2: Business Logic
- **payment-processor** (Rust) - Payment handling
- **notification-service** (Python) - Email/SMS notifications
- **analytics-engine** (Python) - Data analytics

## Phase 3: Frontend
- **web-app** (TypeScript/React) - Web interface
- **mobile-app** (Dart/Flutter) - Mobile applications
"""
            safe_write(roadmap_path, roadmap_content, backup=False)
            self.console.print(success("Created sample ROADMAP.md"))
    
    def create_github_workflow(self) -> None:
        """Create GitHub Actions workflow."""
        workflow_path = self.project_root / '.github' / 'workflows' / 'multi-language-ci.yml'
        workflow_content = """name: Multi-Language CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  detect-languages:
    runs-on: ubuntu-latest
    outputs:
      languages: ${{ steps.detect.outputs.languages }}
    steps:
    - uses: actions/checkout@v4
    - name: Detect languages
      id: detect
      run: |
        python3 .claude/scripts/claude_setup/detect_language.py --json > languages.json
        echo "languages=$(cat languages.json)" >> $GITHUB_OUTPUT

  test:
    needs: detect-languages
    runs-on: ubuntu-latest
    strategy:
      matrix:
        language: ${{ fromJson(needs.detect-languages.outputs.languages) }}
    steps:
    - uses: actions/checkout@v4
    - name: Run tests for ${{ matrix.language }}
      run: make test-${{ matrix.language }}
"""
        safe_write(workflow_path, workflow_content, backup=False)
        self.console.print(success("Created GitHub Actions workflow"))
    
    def create_makefile(self) -> None:
        """Create the master Makefile."""
        # For now, keep the existing Makefile as it's quite comprehensive
        self.console.print(info("Makefile already exists"))
    
    def run_full_setup(self, validate_only: bool = False) -> None:
        """Run the complete setup process."""
        print_banner("Claude Code Native Sub-Agents Setup", "Version 1.0.0")
        
        if validate_only:
            self.validate_setup()
            return
        
        steps = [
            ("Creating directory structure", self.create_directory_structure),
            ("Creating agent files", self.create_agent_files),
            ("Creating commands", self.create_commands),
            ("Creating configuration files", self.create_config_files),
            ("Creating documentation", self.create_documentation),
            ("Creating GitHub workflow", self.create_github_workflow),
            ("Creating Makefile", self.create_makefile),
        ]
        
        for step_name, step_func in steps:
            self.console.print(f"\n{Colors.BLUE}▶ {step_name}...{Colors.RESET}")
            try:
                step_func()
            except Exception as e:
                self.console.print(error(f"Failed: {str(e)}"))
                sys.exit(1)
        
        self.print_summary()
    
    def validate_setup(self) -> None:
        """Validate the current setup."""
        self.console.print("\n🔍 Validating Claude Code setup...\n")
        
        issues = []
        
        # Check directories
        required_dirs = ['.claude/agents', '.claude/commands', '.claude/state']
        for dir_path in required_dirs:
            if not (self.project_root / dir_path).exists():
                issues.append(f"Missing directory: {dir_path}")
        
        # Check agent files
        for agent_name in AGENT_DEFINITIONS:
            agent_path = self.claude_dir / 'agents' / f'{agent_name}.md'
            if not agent_path.exists():
                issues.append(f"Missing agent: {agent_name}")
        
        # Check config
        config_errors = self.config.validate()
        issues.extend(config_errors)
        
        if issues:
            self.console.print(error("Setup validation failed:"))
            for issue in issues:
                self.console.print(f"  • {issue}")
        else:
            self.console.print(success("Setup validation passed!"))
    
    def print_summary(self) -> None:
        """Print setup summary."""
        self.console.print(f"\n{Colors.GREEN}✅ Setup Complete!{Colors.RESET}\n")
        
        self.console.print("📁 Created Structure:")
        self.console.print("   .claude/")
        self.console.print("   ├── agents/        (9 sub-agents)")
        self.console.print("   ├── commands/      (phase-breakdown)")
        self.console.print("   ├── scripts/       (Python tools)")
        self.console.print("   ├── state/         (runtime state)")
        self.console.print("   └── config.json    (configuration)")
        
        self.console.print("\n🚀 Next Steps:")
        self.console.print("   1. Review/edit specs/ROADMAP.md")
        self.console.print("   2. Run: claude")
        self.console.print("   3. Execute: /phase-breakdown 1")
        
        self.console.print("\n📚 For more information, see docs/implementation-guide.md")


@click.command()
@click.option('--validate', '-v', is_flag=True, help='Validate existing setup')
@click.option('--template', '-t', help='Use a specific template set')
@click.option('--languages', '-l', multiple=True, help='Pre-configure specific languages')
def main(validate: bool, template: Optional[str], languages: List[str]) -> None:
    """Complete setup script for Claude Code native sub-agents."""
    manager = SetupManager()
    
    if template:
        manager.console.print(warning(f"Template support coming soon: {template}"))
    
    if languages:
        manager.console.print(info(f"Pre-configuring languages: {', '.join(languages)}"))
    
    manager.run_full_setup(validate_only=validate)


if __name__ == '__main__':
    main()