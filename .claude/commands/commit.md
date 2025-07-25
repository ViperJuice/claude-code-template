# Commit Command

Create well-structured git commits following project conventions.

## Steps

1. Check git status
   - Show untracked files
   - Show staged and unstaged changes
   - Review recent commits for style consistency

2. Analyze changes
   - Categorize changes (feature, fix, docs, refactor, test, chore)
   - Identify the scope of changes
   - Check for sensitive data

3. Stage appropriate files
   - Add relevant files to staging
   - Exclude temporary or generated files

4. Create commit
   - Follow conventional commit format: `type(scope): description`
   - Write clear, concise commit message
   - Include relevant issue numbers
   - Add co-author attribution if applicable

5. Verify commit
   - Show the created commit
   - Run pre-commit hooks if configured

## Commit Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, semicolons, etc)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

## Usage

```
/commit
```