# Claude Code Template

A comprehensive GitHub template for Claude Code projects with standardized directory structure, configurations, and best practices.

## 🚀 Quick Start

### Using this Template

1. Click the "Use this template" button on GitHub
2. Create a new repository from this template
3. Clone your new repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```
4. Customize the `CLAUDE.md` file with your project specifics
5. Update `.claude/settings.json` with your project's commands

## 📁 Project Structure

```
.
├── .claude/                    # Claude Code configuration directory
│   ├── commands/              # Custom slash commands
│   │   ├── start.md          # Initialize project
│   │   ├── commit.md         # Create structured commits
│   │   ├── review.md         # Perform code review
│   │   └── test.md           # Run tests
│   ├── agents/               # Custom sub-agents
│   ├── hooks/                # Pre/post execution hooks
│   │   ├── pre_tool_use.sh   # Run before tool execution
│   │   └── post_tool_use.sh  # Run after tool execution
│   ├── settings.json         # Project settings and permissions
│   └── settings.local.json   # Local overrides (gitignored)
├── .github/                   # GitHub specific files
│   ├── ISSUE_TEMPLATE/       # Issue templates
│   └── workflows/            # GitHub Actions
├── CLAUDE.md                 # Project context for Claude
├── README.md                 # This file
├── .gitignore               # Git ignore rules
└── LICENSE                  # Project license
```

## 🔧 Configuration

### `.claude/settings.json`

The main configuration file for Claude Code. Customize it with:

- **Permissions**: Control which tools Claude can use
- **Hooks**: Define pre/post execution scripts
- **Project Settings**: Configure build, test, and lint commands

Example:
```json
{
  "project": {
    "type": "webapp",
    "language": "typescript",
    "framework": "react",
    "test_command": "npm test",
    "lint_command": "npm run lint",
    "build_command": "npm run build"
  }
}
```

### `CLAUDE.md`

This file provides context to Claude about your project. Update it with:
- Project overview and architecture
- Development setup instructions
- Coding standards and conventions
- Key commands and workflows
- Troubleshooting guides

## 📝 Custom Slash Commands

Create custom commands in `.claude/commands/`:

### `/start`
Initializes the project with dependencies and initial setup.

### `/commit`
Creates well-structured git commits following your project's conventions.

### `/review`
Performs a code review on recent changes.

### `/test`
Runs the project's test suite.

### Creating New Commands

1. Create a new `.md` file in `.claude/commands/`
2. Write the command instructions in markdown
3. Use the command with `/command-name` in Claude Code

## 🪝 Hooks

Hooks allow you to run scripts before or after Claude uses tools:

- **Pre-tool hooks**: Validate actions, check permissions
- **Post-tool hooks**: Log actions, notify team members

Example pre-tool hook:
```bash
#!/bin/bash
# .claude/hooks/pre_tool_use.sh
if [[ "$CLAUDE_TOOL" == "Bash" && "$CLAUDE_COMMAND" =~ "rm -rf" ]]; then
    echo "Dangerous command blocked"
    exit 1
fi
```

## 🤝 Team Collaboration

### Shared Settings
- Commit `.claude/settings.json` for team-wide settings
- Use `.claude/settings.local.json` for personal overrides

### Best Practices
1. Keep `CLAUDE.md` up to date with project changes
2. Document custom commands thoroughly
3. Use hooks for team-specific workflows
4. Review and update permissions regularly

## 🔒 Security

- Never commit sensitive data to `.claude/settings.json`
- Use environment variables for secrets
- Review hook scripts for security implications
- Limit permissions to necessary tools only

## 📚 Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code GitHub](https://github.com/anthropics/claude-code)
- [Report Issues](https://github.com/anthropics/claude-code/issues)

## 📄 License

This template is provided under the MIT License. See [LICENSE](LICENSE) file for details.

---

## Getting Help

- Use `/help` in Claude Code for built-in help
- Check the [troubleshooting guide](https://docs.anthropic.com/en/docs/claude-code/troubleshooting)
- Report issues at the [Claude Code repository](https://github.com/anthropics/claude-code/issues)