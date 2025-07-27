"""Configuration management for Claude Code setup tools."""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from jsonschema import validate, ValidationError

from .utils.file_utils import read_json, get_project_root


# Default Claude Code configuration
DEFAULT_CONFIG = {
    "project": {
        "name": "my-project",
        "description": "Multi-language project using Claude Code agents",
        "languages": ["auto-detect"],
        "defaultBranch": "main"
    },
    "phases": {
        "parallelExecution": True,
        "autoMerge": False,
        "requireCodeReview": True,
        "minTestCoverage": 80,
        "integrationTests": True
    },
    "agents": {
        "timeout": 300,
        "retryOnFailure": True,
        "maxRetries": 2
    },
    "worktrees": {
        "cleanupOnMerge": True,
        "branchPrefix": "feature/phase-",
        "isolateNodeModules": True,
        "isolateVirtualEnvs": True
    },
    "testing": {
        "runBeforeMerge": True,
        "integrationTests": True,
        "coverageThreshold": {
            "statements": 80,
            "branches": 70,
            "functions": 80,
            "lines": 80
        }
    },
    "github": {
        "autoCreatePR": True,
        "prTemplate": True,
        "requireApprovals": 0,
        "deletebranchOnMerge": True
    }
}

# Agent definitions
AGENT_DEFINITIONS = {
    "phase-architect": {
        "name": "phase-architect",
        "description": "Master orchestrator for phase execution. Analyzes roadmap, creates execution plans, coordinates parallel development.",
        "tools": ["Read", "Write", "Task", "Bash", "Glob", "TodoWrite"]
    },
    "interface-designer": {
        "name": "interface-designer", 
        "description": "Creates language-agnostic interfaces and contracts between components. Defines clear boundaries for parallel development.",
        "tools": ["Read", "Write", "MultiEdit", "Grep", "Glob"]
    },
    "interface-verifier": {
        "name": "interface-verifier",
        "description": "Validates interfaces compile correctly across all languages. Checks for circular dependencies and compatibility issues.",
        "tools": ["Read", "Bash", "Grep", "Glob"]
    },
    "worktree-manager": {
        "name": "worktree-manager",
        "description": "Creates and manages Git worktrees for parallel development. Ensures isolation between components.",
        "tools": ["Bash", "Read", "Write"]
    },
    "worktree-lead": {
        "name": "worktree-lead",
        "description": "Coordinates implementation within a single worktree. Manages the test-code cycle for one component.",
        "tools": ["Read", "Write", "Task", "Bash", "TodoWrite"]
    },
    "test-builder": {
        "name": "test-builder",
        "description": "Creates comprehensive test suites using language-specific frameworks. Implements TDD red phase.",
        "tools": ["Read", "Write", "MultiEdit", "Bash"]
    },
    "coder": {
        "name": "coder",
        "description": "Implements features to pass tests. Uses language-specific idioms and best practices.",
        "tools": ["Read", "Write", "MultiEdit", "Bash", "Grep"]
    },
    "integration-guardian": {
        "name": "integration-guardian",
        "description": "Manages PR creation and merging. Ensures all quality gates pass before integration.",
        "tools": ["Bash", "Read", "Write"]
    },
    "doc-scribe": {
        "name": "doc-scribe",
        "description": "Updates documentation after features are merged. Keeps docs in sync with implementation.",
        "tools": ["Read", "Write", "MultiEdit", "Grep"]
    }
}

# Language configurations
LANGUAGE_CONFIGS = {
    "c": {
        "extensions": [".c", ".h"],
        "testCommand": "make test",
        "buildCommand": "make",
        "lintCommand": "clang-tidy",
        "coverageCommand": "gcov"
    },
    "cpp": {
        "extensions": [".cpp", ".cc", ".hpp", ".h"],
        "testCommand": "ctest --output-on-failure",
        "buildCommand": "cmake --build .",
        "lintCommand": "clang-tidy",
        "coverageCommand": "lcov"
    },
    "rust": {
        "extensions": [".rs"],
        "testCommand": "cargo test",
        "buildCommand": "cargo build --release",
        "lintCommand": "cargo clippy -- -D warnings",
        "coverageCommand": "cargo tarpaulin"
    },
    "go": {
        "extensions": [".go"],
        "testCommand": "go test ./...",
        "buildCommand": "go build ./...",
        "lintCommand": "golangci-lint run",
        "coverageCommand": "go test -cover ./..."
    },
    "python": {
        "extensions": [".py"],
        "testCommand": "pytest",
        "buildCommand": "python -m py_compile",
        "lintCommand": "pylint --errors-only",
        "coverageCommand": "pytest --cov"
    },
    "typescript": {
        "extensions": [".ts", ".tsx"],
        "testCommand": "npm test",
        "buildCommand": "npm run build",
        "lintCommand": "npm run lint",
        "coverageCommand": "npm run coverage"
    },
    "javascript": {
        "extensions": [".js", ".jsx"],
        "testCommand": "npm test",
        "buildCommand": "npm run build",
        "lintCommand": "npm run lint",
        "coverageCommand": "npm run coverage"
    },
    "java": {
        "extensions": [".java"],
        "testCommand": "mvn test",
        "buildCommand": "mvn package",
        "lintCommand": "mvn checkstyle:check",
        "coverageCommand": "mvn jacoco:report"
    },
    "dart": {
        "extensions": [".dart"],
        "testCommand": "dart test",
        "buildCommand": "dart compile exe",
        "lintCommand": "dart analyze",
        "coverageCommand": "dart run coverage:test_with_coverage"
    }
}


class Config:
    """Manage Claude Code configuration."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration manager."""
        self.project_root = get_project_root()
        self.config_path = config_path or self.project_root / '.claude' / 'config.json'
        self._config: Dict[str, Any] = {}
        self.load()
    
    def load(self) -> None:
        """Load configuration from file or use defaults."""
        if self.config_path.exists():
            try:
                self._config = read_json(self.config_path)
            except Exception as e:
                print(f"Warning: Failed to load config from {self.config_path}: {e}")
                self._config = DEFAULT_CONFIG.copy()
        else:
            self._config = DEFAULT_CONFIG.copy()
    
    def save(self) -> None:
        """Save configuration to file."""
        from .utils.file_utils import write_json
        write_json(self.config_path, self._config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation."""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value using dot notation."""
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_language_config(self, language: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific language."""
        # First check project config
        lang_config = self.get(f'languages.{language}')
        if lang_config:
            return lang_config
        
        # Fall back to defaults
        return LANGUAGE_CONFIGS.get(language)
    
    def get_agent_definition(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get the definition for a specific agent."""
        return AGENT_DEFINITIONS.get(agent_name)
    
    def get_all_agents(self) -> Dict[str, Dict[str, Any]]:
        """Get all agent definitions."""
        return AGENT_DEFINITIONS.copy()
    
    def validate(self) -> List[str]:
        """Validate the configuration and return any errors."""
        errors = []
        
        # Check required fields
        if not self.get('project.name'):
            errors.append("Missing required field: project.name")
        
        # Validate language configurations
        for lang, config in self._config.get('languages', {}).items():
            if not isinstance(config, dict):
                errors.append(f"Invalid language config for {lang}")
                continue
            
            required_commands = ['testCommand', 'buildCommand']
            for cmd in required_commands:
                if cmd not in config:
                    errors.append(f"Missing {cmd} for language {lang}")
        
        # Validate numeric thresholds
        coverage = self.get('testing.coverageThreshold', {})
        for metric, value in coverage.items():
            if not isinstance(value, (int, float)) or value < 0 or value > 100:
                errors.append(f"Invalid coverage threshold for {metric}: {value}")
        
        return errors


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config


def load_template(template_name: str) -> Optional[str]:
    """Load a template file from the templates directory."""
    template_dir = Path(__file__).parent / 'templates'
    template_path = template_dir / f'{template_name}.template'
    
    if template_path.exists():
        return template_path.read_text(encoding='utf-8')
    
    return None