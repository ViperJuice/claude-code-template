# phase-breakdown.md
Place this file at: `.claude/commands/phase-breakdown.md`

---
allowed-tools: Bash, Task, Read, Write, TodoWrite
description: Execute a development phase using native Claude Code sub-agents for parallel implementation. Supports C/C++, Rust, Go, Python, Java, TypeScript, Dart, Assembly and 15+ other languages.
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

# Detect project languages
echo ""
echo "Detecting project languages..."
find . -type f \( -name "*.go" -o -name "*.rs" -o -name "*.py" -o -name "*.ts" -o -name "*.java" -o -name "*.rb" -o -name "*.cpp" -o -name "*.swift" -o -name "*.dart" -o -name "*.ex" -o -name "*.hs" -o -name "*.ml" -o -name "*.r" -o -name "*.jl" -o -name "*.m" -o -name "*.sql" \) -not -path "./worktrees/*" -not -path "./.git/*" | sed 's/.*\.//' | sort | uniq -c | sort -nr | head -10

# Check for language configs
echo ""
echo "Language configuration files:"
ls -la | grep -E "(go.mod|Cargo.toml|package.json|pom.xml|requirements.txt|Gemfile|CMakeLists.txt|Package.swift|pubspec.yaml|mix.exs|stack.yaml|dune-project)"
```

### Create Initial State

```javascript
// Detect primary languages from above output
const detectedLanguages = ['typescript', 'go', 'rust']; // Update based on detection

Write({
  path: '.claude/state/current-phase.json',
  content: JSON.stringify({
    phase: '$ARGUMENTS',
    status: 'initializing',
    startTime: new Date().toISOString(),
    projectLanguages: detectedLanguages
  }, null, 2)
});

TodoWrite({
  todos: [{
    id: 'phase-$ARGUMENTS-start',
    content: 'Execute Phase $ARGUMENTS',
    status: 'in_progress',
    priority: 'high'
  }]
});
```

### Launch Phase Architect

Use the Task tool to delegate the entire phase orchestration to the phase-architect sub-agent:

```javascript
Task({
  description: "Orchestrate Phase $ARGUMENTS development",
  prompt: `Use the phase-architect sub agent to orchestrate Phase $ARGUMENTS. 

The phase architect should:
1. Read the ROADMAP.md to understand phase requirements
2. Detect project languages and assign languages to components
3. Create a detailed execution plan with language specifications
4. Design interfaces using the interface-designer sub agent
5. Set up worktrees using the worktree-manager sub agent
6. Launch parallel worktree-lead sub agents for implementation
7. Ensure worktree-leads use language-specific test-builder and coder agents
8. Coordinate integration using the integration-guardian sub agent

The phase is: $ARGUMENTS
Detected project languages: ${detectedLanguages.join(', ')}

Each component should be assigned an appropriate language based on its purpose and the project's language distribution.`,
  subagent_type: 'phase-architect'
});
```

### Monitor Progress

The phase-architect will handle all orchestration. Check progress in:
- `.claude/state/current-phase.json` - Overall phase status
- `.claude/state/worktree-status.json` - Individual component progress
- Git worktree list - Active development branches

### Success Criteria

Phase is complete when:
- All components implemented and tested
- All PRs merged to main
- Integration tests passing
- Documentation updated