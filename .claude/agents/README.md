# Claude Code Agents

This directory contains all the specialized AI sub-agents that power the Claude Code Multi-Language Template. The agents are organized into two categories: core orchestration agents and language-specific implementation agents.

## Agent Organization

### Core Orchestration Agents (9 agents)
These agents handle the high-level workflow and coordination:

1. **phase-architect.md**
   - Master orchestrator for phase execution
   - Analyzes roadmap and creates execution plans
   - Coordinates all other agents

2. **interface-designer.md**
   - Creates language-agnostic interfaces between components
   - Defines clear boundaries for parallel development
   - Generates appropriate patterns for each language

3. **interface-verifier.md**
   - Validates that interfaces compile correctly
   - Checks for circular dependencies
   - Ensures cross-language compatibility

4. **worktree-manager.md**
   - Creates and manages Git worktrees
   - Ensures isolation between parallel development streams
   - Sets up language-specific environments

5. **worktree-lead.md**
   - Manages implementation within a single worktree
   - Detects component language and selects appropriate agents
   - Coordinates TDD cycle with test-builder and coder

6. **integration-guardian.md**
   - Manages PR merges to main branch
   - Ensures all tests pass before integration
   - Handles merge conflicts and rollbacks

7. **doc-scribe.md**
   - Updates documentation after features are merged
   - Keeps README, API docs, and changelog in sync
   - Generates language-specific documentation

8. **test-builder.md.deprecated** (Generic - DO NOT USE)
   - Legacy multi-language test builder
   - Replaced by language-specific test builders

9. **coder.md.deprecated** (Generic - DO NOT USE)
   - Legacy multi-language coder
   - Replaced by language-specific coders

### Language-Specific Implementation Agents (16 agents)
These agents handle the actual code implementation for different language families:

#### Test Builder Agents (8)
Create failing tests following TDD principles:

- **test-builder-systems.md** - C, C++, Rust, Go, Zig
- **test-builder-jvm.md** - Java, Kotlin, Scala, Clojure
- **test-builder-web.md** - JavaScript, TypeScript, React, Vue
- **test-builder-scripting.md** - Python, Ruby, Perl, Bash
- **test-builder-mobile.md** - Swift, Objective-C, Dart/Flutter, React Native
- **test-builder-functional.md** - Haskell, OCaml, F#, Elixir, Erlang
- **test-builder-data.md** - SQL, R, Julia, MATLAB
- **test-builder-assembly.md** - x86, ARM, RISC-V, WebAssembly

#### Coder Agents (8)
Implement features to make tests pass:

- **coder-systems.md** - C, C++, Rust, Go, Zig
- **coder-jvm.md** - Java, Kotlin, Scala, Clojure
- **coder-web.md** - JavaScript, TypeScript, React, Vue
- **coder-scripting.md** - Python, Ruby, Perl, Bash
- **coder-mobile.md** - Swift, Objective-C, Dart/Flutter, React Native
- **coder-functional.md** - Haskell, OCaml, F#, Elixir, Erlang
- **coder-data.md** - SQL, R, Julia, MATLAB
- **coder-assembly.md** - x86, ARM, RISC-V, WebAssembly

## Agent Selection Flow

1. User runs `/phase-breakdown` command
2. **phase-architect** analyzes the roadmap and creates a plan
3. **interface-designer** creates component boundaries
4. **interface-verifier** validates the interfaces
5. **worktree-manager** sets up isolated Git worktrees
6. **worktree-lead** (for each component):
   - Detects the component's language
   - Selects appropriate language-specific agents
   - Invokes **test-builder-[family]** to create tests
   - Invokes **coder-[family]** to implement features
7. **integration-guardian** merges completed work
8. **doc-scribe** updates documentation

## Language Family Approach

Instead of having one massive agent trying to handle 33 languages, we group related languages into families. This approach:

- **Reduces context pollution** - Each agent handles 3-5 related languages
- **Improves code quality** - Agents can focus on language-specific idioms
- **Maintains efficiency** - Smaller, focused prompts generate better code
- **Enables specialization** - Each family has unique patterns and practices

## Adding New Agents

To add a new agent:

1. Create a new `.md` file in this directory
2. Add YAML frontmatter with name, description, and tools
3. Write clear instructions for the agent's role
4. Update this README to document the new agent
5. Update the orchestration flow if needed

## Best Practices

- Keep agents focused on a single responsibility
- Use clear, action-oriented descriptions
- Specify required tools in the frontmatter
- Include error handling instructions
- Document expected inputs and outputs