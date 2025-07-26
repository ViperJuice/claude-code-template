# phase-breakdown.md - Advanced Phase Breakdown Command for Claude Code

Place this file at: `.claude/commands/phase-breakdown.md`

---
allowed-tools: Bash(git:*), Bash(gh:*), Bash(npm:*), Bash(mkdir:*), Bash(cd:*), Bash(pwd:*), Bash(ls:*), Bash(cat:*), Bash(echo:*), Bash(test:*), Bash(grep:*), Bash(find:*), Bash(for:*), Bash(if:*), Bash(rmdir:*), Task, TodoWrite, Write, MultiEdit, Read, Glob, Grep
description: Break down a development phase into parallel tasks with clear interface boundaries and automated execution
argument-hint: [phase-name or phase-number]
---

## Initial Context

!`echo "=== Git Repository Status ==="`
!`git status --porcelain`
!`echo ""`
!`echo "=== Current Branch ==="`
!`git branch --show-current`
!`echo ""`
!`echo "=== Existing Worktrees ==="`
!`git worktree list`
!`test -d worktrees && echo "⚠ worktrees directory exists" || echo "✓ No worktrees directory"`

## Project Analysis

!`echo "=== Project Structure ==="`
!`find . -type f -name "package.json" -o -name "tsconfig.json" -o -name "setup.py" -o -name "main.js" -o -name "index.js"`
!`echo ""`
!`echo "=== Test Framework ==="`
!`test -f package.json && grep -E "(test|jest|mocha|vitest)" package.json || echo "No package.json found"`

## Roadmap Content

!`echo "=== ROADMAP.md Content ==="`
!`cat ./specs/ROADMAP.md || cat ./ROADMAP.md || echo "ERROR: ROADMAP.md not found"`

## Phase Detection

!`echo ""`
!`echo "=== Available Phases ==="`
!`grep -E "^## Phase [0-9]+" ./specs/ROADMAP.md || grep -E "^## Phase [0-9]+" ./ROADMAP.md || echo "No phases found"`
!`echo ""`
!`echo "=== Incomplete Phases ==="`
!`grep -E "^## Phase [0-9]+" ./specs/ROADMAP.md || grep -E "^## Phase [0-9]+" ./ROADMAP.md || echo "No ROADMAP found"`
!`echo "(Showing all phases - completed phases marked with ✅)"`

---

## Instructions

You are Claude Code's most advanced slash command for orchestrating parallel development. Your mission is to break down the phase "$ARGUMENTS" into perfectly parallelizable tasks with zero merge conflicts.

### Phase 1: Ultra-Deep Analysis

1. **Parse the ROADMAP.md** to extract all tasks for phase "$ARGUMENTS"
2. **Categorize each task** as either:
   - **NEW**: Requires creating stubs/skeletons
   - **MODIFY**: Works within existing code
3. **Identify boundaries** for parallel work
4. **Plan the interface/boundary strategy**

### Phase 2: Boundary Creation

For NEW features, create skeleton code with clear ownership:
```javascript
// Example: src/monitoring/collector.js
class MetricsCollector {
  constructor() {
    // TODO: Implement by monitoring-team
    throw new Error('Not implemented');
  }
  
  collectMetrics() {
    // TODO: Implement by monitoring-team
    throw new Error('Not implemented');
  }
}

// Example: src/api/marketplace.js  
function searchServices(query) {
  // TODO: Implement by marketplace-team
  throw new Error('Not implemented');
}
```

For EXISTING features, document the boundaries without creating stubs.

### Phase 3: Git Operations

**CRITICAL**: After creating boundaries, commit and push to main:
```bash
# Check for changes
git status

# If boundaries were created:
git add -A
git commit -m "feat: add Phase $ARGUMENTS boundaries for parallel implementation"
git push origin main

# Verify push succeeded
git log -1 --oneline
```

### Phase 4: Worktree Setup

Create worktrees INSIDE the current repository:
```bash
# Create worktrees directory
mkdir -p worktrees

# Create worktrees for each parallel task
git worktree add ./worktrees/task1-name -b feature/phase-X-component1
git worktree add ./worktrees/task2-name -b feature/phase-X-component2

# Verify creation
ls -la worktrees/
git worktree list
```

### Phase 5: Task Tool Agent Orchestration

Use the Task tool to spawn parallel agents. Each agent works in their assigned worktree:

```javascript
// Launch multiple agents in parallel
Task({
  description: "Component 1 implementation",
  prompt: `You are implementing Component 1 for Phase X.

CRITICAL FIRST STEPS - MUST EXECUTE:
========================================
cd ./worktrees/task1-name
pwd  # MUST show: .../worktrees/task1-name
git status  # MUST show: On branch feature/phase-X-component1

If you're not in the worktree, STOP and navigate there first!

YOUR BOUNDARIES:
================
NEW implementations:
- src/path/to/file.js -> methodName() marked "TODO: Implement by team1"
- src/another/file.js -> className marked "TODO: Implement by team1"

EXISTING modifications:  
- src/existing/file.js -> optimize existingMethod() (stay within method boundaries)

CONSTRAINTS:
============
- Work ONLY within your assigned boundaries
- Do NOT create new public methods unless they're stubs assigned to you
- Do NOT modify code outside your boundaries
- Include comprehensive error handling
- Write tests for all implementations

WORKFLOW:
=========
1. Implement features within boundaries
2. Write comprehensive tests
3. Run tests: npm test
4. Commit your work:
   git add -A
   git commit -m "feat: implement Component 1 for Phase X"
5. Push to remote:
   git push -u origin feature/phase-X-component1  
6. Create PR:
   gh pr create --title "feat: [Phase X] Component 1" --body "Implements boundaries defined in main branch"

PROGRESS TRACKING:
==================
Use TodoWrite to update your task status:
- Mark "Implement Component 1" as in_progress when starting
- Mark as completed when done
- Add any new discovered tasks

Begin by navigating to the worktree and verifying your location.`
});

// Launch other agents in parallel...
```

### Phase 6: Progress Monitoring

Monitor all agents and worktrees:
```bash
# Check worktree status
for worktree in ./worktrees/*/; do
  if [ -d "$worktree" ]; then
    echo "=== $worktree ==="
    cd "$worktree"
    git status --short
    git log --oneline origin/main..HEAD
    cd ..
  fi
done

# Check PR status  
gh pr list --state open
```

### Phase 7: Integration

After agents complete their work:
```bash
# Update main
git checkout main
git pull origin main

# Merge PRs in dependency order
gh pr merge PR_NUMBER --merge --delete-branch

# Run integration tests after each merge
npm test
npm run test:integration

# Continue with next PR...
```

### Phase 8: Cleanup

```bash
# Remove worktrees
git worktree remove ./worktrees/task1-name
git worktree remove ./worktrees/task2-name
git worktree prune

# Clean up directory
rmdir worktrees || echo "Worktrees directory not empty or doesn't exist"

# Update documentation
# Update ROADMAP.md to mark phase complete
```

---

## Output Format

Structure your response as follows:

### 📊 Phase Analysis

**Phase Identified**: Phase X: Name
**Total Tasks**: N tasks found
**Parallelization Strategy**: 
- X new features (need stubs)
- Y existing features (modify in place)
- Z independent components

### 🎯 Task Breakdown

1. **Task Group Alpha** (New Feature)
   - **Boundaries**: Create stubs in `src/feature/new.js`
   - **Methods**: `doSomething()`, `doAnother()`
   - **Agent**: monitoring-team
   - **Dependencies**: None

2. **Task Group Beta** (Existing Feature)
   - **Boundaries**: Modify `processData()` in `src/core/processor.js`
   - **Constraints**: Stay within method, maintain signature
   - **Agent**: optimization-team
   - **Dependencies**: Complete after Alpha

### 🏗️ Boundary Definitions

I will now create the necessary boundaries in the main branch...

[Create actual stub files using Write/MultiEdit tools]

### 📝 TodoWrite Setup

```javascript
TodoWrite({
  todos: [
    {
      id: "phase-X-setup",
      content: "Setup Phase X infrastructure and boundaries",
      status: "completed",
      priority: "high"
    },
    {
      id: "phase-X-task-alpha",
      content: "Implement Task Alpha features",
      status: "pending",
      priority: "high"
    },
    // ... more tasks
  ]
});
```

### 🚀 Git Operations

```bash
# Committing boundaries
git add -A
git commit -m "feat: add Phase X boundaries for parallel implementation"
git push origin main
```

### 🌳 Worktree Creation

```bash
# Creating worktrees
mkdir -p worktrees
git worktree add ./worktrees/task-alpha -b feature/phase-X-alpha
git worktree add ./worktrees/task-beta -b feature/phase-X-beta
```

### 🤖 Agent Launch Commands

[Show the exact Task tool invocations]

### 📈 Progress Monitoring

```bash
# Monitor command
for worktree in ./worktrees/*/; do
  echo "=== $worktree ==="
  cd "$worktree" && git log --oneline -1 && cd ..
done
```

### 🔄 Integration Plan

1. Merge order based on dependencies
2. Test commands after each merge
3. Rollback procedures if needed

---

## Important Notes

1. **Boundaries are Sacred**: Agents must stay within assigned boundaries
2. **Commit Early and Often**: Boundaries must be in main before worktrees are created
3. **Test Everything**: Run tests after implementation and after merges
4. **Clean Up**: Remove worktrees after integration
5. **Track Progress**: Use TodoWrite throughout the process

## Error Recovery

If an agent fails:
```bash
# Inspect the problematic worktree
cd ./worktrees/task-name
git status
git diff
# Fix issues or provide new instructions
```

If merge conflicts occur:
```bash
# Boundaries should prevent this, but if it happens:
git status
git diff
# Resolve conflicts maintaining boundary integrity
```

Remember: The goal is PERFECT parallel execution with ZERO merge conflicts through INTELLIGENT boundary design.