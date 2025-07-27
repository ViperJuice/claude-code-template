# Claude Code Setup Tools (Python)

This directory contains Python implementations of the Claude Code setup scripts, providing better maintainability, error handling, and cross-platform compatibility.

## Installation

### Option 1: Direct usage (recommended)
The bash wrapper scripts handle Python dependencies automatically:
```bash
./.claude/scripts/setup-native-subagents-new.sh
```

### Option 2: Install as Python package
```bash
cd .claude/scripts
pip install -e .
```

This installs the following commands:
- `claude-setup` - Set up Claude Code native sub-agents
- `claude-detect-language` - Detect programming languages
- `claude-inventory` - Check installation status
- `claude-cleanup` - Remove legacy files

## Scripts Overview

### setup_native_subagents.py
Complete setup script for Claude Code native sub-agents.

**Features:**
- Creates directory structure
- Generates agent files with proper content
- Sets up configuration files
- Creates documentation templates
- Validates existing setup

**Usage:**
```bash
# Run full setup
./setup-native-subagents-new.sh

# Validate existing setup
./setup-native-subagents-new.sh --validate

# With specific languages
./setup-native-subagents-new.sh -l rust -l python -l typescript
```

### detect_language.py
Automatically detect programming languages in a project.

**Features:**
- Detects 25+ programming languages
- Confidence scoring
- Recursive directory scanning
- JSON output for integration
- Version detection (experimental)

**Usage:**
```bash
# Detect in current directory
./detect-language-new.sh

# Recursive scan with JSON output
./detect-language-new.sh -r --json

# Specific directories with confidence threshold
./detect-language-new.sh /path/to/project -c 0.8
```

### inventory_check.py
Check which Claude Code files are present and validate setup.

**Features:**
- Comprehensive file checking
- Health score calculation
- Multiple output formats (text, JSON, tree)
- Legacy file detection
- Fix suggestions

**Usage:**
```bash
# Basic check
./inventory-check-new.sh

# JSON output for CI/CD
./inventory-check-new.sh --format json

# Tree view
./inventory-check-new.sh --format tree
```

### cleanup_legacy.py
Remove legacy orchestration files from old Claude Code setups.

**Features:**
- Safe file detection with patterns
- Automatic backup before deletion
- Dry-run mode
- Undo script generation
- Empty directory cleanup

**Usage:**
```bash
# Dry run (see what would be deleted)
./cleanup-legacy-new.sh --dry-run

# Interactive cleanup with backup
./cleanup-legacy-new.sh

# Force cleanup without prompts
./cleanup-legacy-new.sh --force

# No backup
./cleanup-legacy-new.sh --no-backup
```

## Utility Modules

### utils/colors.py
Terminal color utilities with cross-platform support.
- ANSI color codes
- Windows compatibility
- NO_COLOR environment variable support

### utils/file_utils.py
File and directory manipulation utilities.
- Safe file writing with atomic operations
- Backup functionality
- Project root detection
- Template processing

### config.py
Configuration management for Claude Code.
- Language configurations
- Agent definitions
- Template loading
- Validation

## Python vs Bash Comparison

| Feature | Bash Scripts | Python Scripts |
|---------|-------------|----------------|
| Error Handling | Basic | Comprehensive exceptions |
| Cross-Platform | Limited | Full support |
| JSON Handling | External tools | Native support |
| Progress Display | Echo statements | Rich progress bars |
| Testing | Difficult | Easy unit tests |
| Debugging | Challenging | Standard Python tools |
| Dependencies | System packages | pip packages |

## Development

### Running tests
```bash
cd .claude/scripts
python -m pytest tests/
```

### Adding new scripts
1. Create module in `claude_setup/`
2. Add CLI entry point using `click`
3. Create bash wrapper in parent directory
4. Update setup.py if adding console script

### Code style
- Use type hints
- Follow PEP 8
- Add docstrings
- Handle exceptions gracefully

## Migration from Bash

The Python scripts are designed to be drop-in replacements for the bash versions:

| Old Bash Script | New Python Wrapper |
|----------------|-------------------|
| setup-native-subagents.sh | setup-native-subagents-new.sh |
| detect-language.sh | detect-language-new.sh |
| inventory-check.sh | inventory-check-new.sh |
| cleanup-legacy.sh | cleanup-legacy-new.sh |

To migrate, simply use the `-new.sh` versions. They accept the same arguments and produce similar output.