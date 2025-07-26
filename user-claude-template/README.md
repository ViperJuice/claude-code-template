# User-Level Claude Code Configuration

This template provides a starting point for your personal Claude Code configuration that applies across all your projects.

## Installation

1. Copy the `.claude` directory to your home directory:
   ```bash
   cp -r user-claude-template/.claude ~/
   ```

2. Customize the configuration files:
   - Edit `~/.claude/CLAUDE.md` with your preferences
   - Update `~/.claude/settings.json` with your preferred settings
   - Add personal commands to `~/.claude/commands/`
   - Create custom hooks in `~/.claude/hooks/`

## Structure

```
~/.claude/
├── commands/          # Personal slash commands
│   ├── format.md     # Code formatting command
│   └── snippet.md    # Code snippet insertion
├── agents/           # Personal sub-agents
├── hooks/            # Personal hooks
├── settings.json     # Global settings
└── CLAUDE.md        # Personal preferences and notes
```

## Customization

### Personal Commands
Create commands that match your workflow:
- `/format` - Format code with your preferred style
- `/snippet` - Insert common code patterns
- `/deploy` - Personal deployment scripts
- `/backup` - Backup important files

### Settings
Configure your preferences in `settings.json`:
- Code style preferences
- Git workflow settings
- Testing preferences
- Security permissions

### Hooks
Add automation to your workflow:
- Pre-commit formatting
- Post-edit linting
- Test running triggers

## Best Practices

1. **Keep it DRY**: Put only truly global settings here
2. **Security**: Never store credentials or secrets
3. **Version Control**: Consider backing up your config to a private repo
4. **Documentation**: Keep CLAUDE.md updated with your preferences

## Merging with Project Settings

Claude Code merges settings in this order:
1. Built-in defaults
2. User-level settings (this configuration)
3. Project-level settings
4. Local project overrides

Project settings always take precedence over user settings.