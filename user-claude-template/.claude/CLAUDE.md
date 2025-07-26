# User-Level Claude Code Configuration

This is your personal Claude Code configuration that applies to all projects.

## Personal Preferences

### Code Style
- Preferred indentation: [spaces/tabs]
- Indent size: [2/4]
- Line length: [80/100/120]
- Quote style: [single/double]

### Development Workflow
- Preferred test framework: [jest/pytest/go test]
- Commit style: [conventional/descriptive]
- Branch naming: [feature/fix prefix style]

### Common Tools
- Package manager: [npm/yarn/pnpm/pip/cargo]
- Version control: git
- CI/CD: [GitHub Actions/GitLab CI/Jenkins]

## Global Commands

Place any personal slash commands in `.claude/commands/` that you want available across all projects.

## Personal Hooks

Add any personal pre/post execution hooks in `.claude/hooks/` for custom workflows.

## Frequently Used Snippets

### Git Aliases
```bash
# Common git operations
git co = checkout
git br = branch
git st = status
```

### Testing Patterns
```bash
# Quick test runners
test-watch = npm test -- --watch
test-coverage = npm test -- --coverage
```

## Project Templates

Links to your commonly used project templates:
- React: [link]
- Python API: [link]
- CLI Tool: [link]

## Notes
- Remember to keep sensitive information out of this file
- This configuration is meant to enhance your workflow across all projects
- Update this file as your preferences evolve