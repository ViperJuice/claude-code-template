# Migration Guide: From Shell Scripts to Python

## Overview

This guide helps you migrate from the legacy shell script implementation to the new Python-based Claude Code template system.

## What's Changed

### Old Architecture (Shell Scripts)
- Bash scripts with placeholder content
- Limited error handling
- Platform-specific code
- Difficult to maintain and extend

### New Architecture (Python)
- Python modules with proper error handling
- Cross-platform compatibility
- Rich CLI output with progress indicators
- Modular, extensible design

## Migration Steps

### Step 1: Backup Existing Setup

```bash
# Create backup of current .claude directory
cp -r .claude .claude.backup

# Save current state
git add -A
git commit -m "Backup before Python migration"
```

### Step 2: Update Scripts

The migration script handles this automatically:

```bash
# Run the migration
./.claude/scripts/setup-native-subagents.sh --migrate
```

This will:
1. Back up old shell scripts as `.old` files
2. Replace with Python wrapper scripts
3. Install required Python dependencies
4. Validate the new setup

### Step 3: Update Custom Commands

If you have custom commands or scripts, update them to use the new Python modules:

**Old Way (Shell)**:
```bash
#!/bin/bash
source .claude/scripts/detect-language.sh
detect_languages
```

**New Way (Python)**:
```python
#!/usr/bin/env python3
from claude_setup.detect_language import LanguageDetector

detector = LanguageDetector()
results = detector.detect_all()
detector.display_results(results)
```

### Step 4: Update CI/CD Pipelines

Update your CI/CD configurations to use Python:

**GitHub Actions Example**:
```yaml
- name: Setup Claude Code
  run: |
    pip install -r .claude/scripts/requirements.txt
    python -m claude_setup.setup_native_subagents --check
```

### Step 5: Clean Up Legacy Files

After confirming everything works:

```bash
# Remove old backup files
./.claude/scripts/cleanup-legacy.sh --force

# Remove .old script backups
rm .claude/scripts/*.sh.old
```

## API Changes

### Language Detection

**Old Shell API**:
```bash
languages=$(detect_project_languages)
```

**New Python API**:
```python
from claude_setup.detect_language import LanguageDetector

detector = LanguageDetector()
languages = detector.detect_all()
```

### Setup Configuration

**Old Shell Configuration**:
```bash
PROJECT_ROOT="$1"
PHASES="$2"
```

**New Python Configuration**:
```python
from claude_setup.config import Config

config = Config(project_root=".", phases_dir="specs")
```

### Inventory Check

**Old Shell Function**:
```bash
check_setup
```

**New Python Function**:
```python
from claude_setup.inventory_check import InventoryChecker

checker = InventoryChecker()
checker.run_checks()
```

## Environment Variables

### Legacy Variables (Deprecated)
- `CLAUDE_SCRIPTS_DIR`
- `CLAUDE_LEGACY_MODE`

### New Variables
- `CLAUDE_SETUP_CONFIG` - Path to configuration file
- `CLAUDE_SETUP_LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `CLAUDE_SETUP_NO_COLOR` - Disable colored output

## Feature Improvements

### 1. Better Error Messages

**Old**:
```
Error: File not found
```

**New**:
```
❌ Error: Configuration file not found
   Path: /home/user/project/.claude/config.json
   Suggestion: Run setup-native-subagents.sh to create it
```

### 2. Progress Indicators

The new Python implementation includes:
- Progress bars for long operations
- Spinner animations for background tasks
- Colored output for better readability

### 3. Validation

Enhanced validation includes:
- JSON schema validation
- Path existence checks
- Permission verification
- Dependency checking

## Extending the New System

### Creating Custom Modules

1. Add your module to `.claude/scripts/claude_setup/`:

```python
# .claude/scripts/claude_setup/my_feature.py
from typing import List
from .utils.console import console
from .config import Config

class MyFeature:
    def __init__(self, config: Config):
        self.config = config
    
    def run(self) -> None:
        console.print("[bold green]Running my feature...[/bold green]")
```

2. Add CLI command:

```python
# Add to existing CLI or create new script
@click.command()
@click.pass_context
def my_command(ctx):
    """Run my custom feature."""
    feature = MyFeature(ctx.obj)
    feature.run()
```

### Using the Module System

```python
from claude_setup.utils.console import console, create_progress
from claude_setup.utils.filesystem import find_files, ensure_directory

# Use utilities
with create_progress() as progress:
    task = progress.add_task("Processing files...", total=100)
    # ... do work
    progress.update(task, advance=1)
```

## Troubleshooting

### Issue: Import Errors

```bash
# Error: ModuleNotFoundError: No module named 'claude_setup'

# Solution:
export PYTHONPATH="${PYTHONPATH}:/path/to/.claude/scripts"
# Or install in development mode:
cd .claude/scripts && pip install -e .
```

### Issue: Missing Dependencies

```bash
# Error: No module named 'click'

# Solution:
pip install -r .claude/scripts/requirements.txt
```

### Issue: Permission Errors

```bash
# Error: Permission denied

# Solution:
chmod +x .claude/scripts/*.sh
```

### Issue: Old Scripts Still Running

```bash
# Check which script is being called
which setup-native-subagents.sh

# Update PATH if needed
export PATH="/path/to/new/scripts:$PATH"
```

## Rollback Plan

If you need to rollback to shell scripts:

```bash
# Restore from backup
mv .claude.backup .claude

# Or restore specific scripts
cp .claude/scripts/*.sh.old .claude/scripts/
# Remove .old extension
for f in .claude/scripts/*.sh.old; do
    mv "$f" "${f%.old}"
done
```

## Benefits of Migration

1. **Cross-Platform**: Works on Windows, macOS, and Linux
2. **Better Testing**: Unit tests for all components
3. **Maintainability**: Cleaner code structure
4. **Performance**: Faster execution with better caching
5. **Extensibility**: Easy to add new features
6. **Debugging**: Better error messages and logging

## Getting Help

- Check logs: `.claude/logs/`
- Run validation: `python -m claude_setup.inventory_check`
- Enable debug mode: `export CLAUDE_SETUP_LOG_LEVEL=DEBUG`

## Future Deprecations

The following will be removed in future versions:
- Shell script placeholders
- Legacy environment variables
- Old configuration format

Plan your migration accordingly!