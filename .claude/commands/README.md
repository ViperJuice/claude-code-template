# Claude Code Custom Commands

This directory contains custom slash commands for Claude Code. These commands provide shortcuts for common development tasks.

## Available Commands

### `/start`
Initialize the project with dependencies and setup.
- Installs dependencies
- Sets up environment variables
- Runs initial setup scripts

### `/commit`
Create well-structured git commits.
- Analyzes changes
- Follows commit conventions
- Includes appropriate files

### `/review`
Perform code review on recent changes.
- Checks code quality
- Reviews architecture
- Verifies tests and documentation

### `/test`
Run the project's test suite.
- Executes all tests
- Reports coverage
- Analyzes failures

## Creating Custom Commands

To create a new command:

1. Create a new `.md` file in this directory
2. Name it after your command (e.g., `deploy.md` for `/deploy`)
3. Document the command's purpose and steps
4. Use clear, actionable instructions

## Command Structure

Each command should include:
- **Purpose**: What the command does
- **Steps**: Detailed actions to perform
- **Usage**: How to invoke the command
- **Options**: Any parameters or variations

## Best Practices

- Keep commands focused on a single task
- Make commands idempotent when possible
- Include error handling instructions
- Document any prerequisites
- Use consistent formatting