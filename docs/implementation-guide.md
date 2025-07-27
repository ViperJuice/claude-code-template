# Multi-Language Claude Code Implementation Guide

## 🚀 Quick Start

```bash
# 1. Clone your template
git clone https://github.com/ViperJuice/claude-code-template my-project
cd my-project

# 2. Run the setup script
chmod +x .claude/scripts/setup-native-subagents.sh
./.claude/scripts/setup-native-subagents.sh

# 3. Configure your languages
cp .claude/config.json.example .claude/config.json
# Edit to specify your project languages

# 4. Start Claude Code
claude

# 5. Execute a phase
/phase-breakdown 1
```

## 📋 Complete Feature List

### Native Sub-Agents (10 total)
1. **phase-architect** - Orchestrates entire workflow
2. **interface-designer** - Creates language-agnostic interfaces
3. **interface-verifier** - Validates interfaces for all languages
4. **worktree-manager** - Manages Git worktrees
5. **worktree-lead** - Coordinates component implementation
6. **test-builder** - Creates language-specific tests
7. **coder** - Implements features in any language
8. **integration-guardian** - Manages PR merges
9. **doc-scribe** - Updates documentation
10. **rollback-manager** - Handles error recovery

### Language Support (25+ languages)
- **Systems**: C, C++, Rust, Assembly
- **Enterprise**: Java, C#, Go
- **Web**: TypeScript, JavaScript, Dart
- **Scripting**: Python, Ruby, Perl, Lua
- **Functional**: Haskell, Elixir, Erlang, Clojure, F#
- **Data Science**: R, Julia
- **Mobile**: Swift, Kotlin
- **Modern**: Zig, Nim

### Helper Scripts
- `setup-native-subagents.sh` - Initial setup
- `detect-language.sh` - Auto-detect project languages
- `Master Makefile` - Coordinate multi-language builds

### CI/CD Integration
- GitHub Actions workflow for all languages
- Docker Compose for development environment
- Language-specific linting and testing

## 🏗️ Architecture Overview

```
┌─────────────────────┐
│  /phase-breakdown   │
└──────────┬──────────┘
           │
    ┌──────▼──────┐
    │Phase Architect│
    └──────┬──────┘
           │
    ┌──────▼──────────────┐
    │Interface Designer    │
    │(Multi-language)      │
    └──────┬──────────────┘
           │
    ┌──────▼──────────────┐
    │Interface Verifier    │
    │(25+ languages)       │
    └──────┬──────────────┘
           │
    ┌──────▼──────────────┐
    │Worktree Manager      │
    └──────┬──────────────┘
           │
    ┌──────▼──────────────┐
    │Parallel Worktrees    │
    │┌────┐┌────┐┌────┐   │
    ││Rust││ C  ││Dart│   │
    │└────┘└────┘└────┘   │
    └──────┬──────────────┘
           │
    ┌──────▼──────────────┐
    │Integration Guardian  │
    └──────┬──────────────┘
           │
    ┌──────▼──────────────┐
    │Production Ready      │
    └─────────────────────┘
```

## 💡 Usage Examples

### Example 1: Mixed Language Microservices
```bash
# ROADMAP.md contains:
# - Rust API service
# - Go worker service  
# - TypeScript web frontend
# - C++ performance module

/phase-breakdown 1
# Automatically creates 4 worktrees
# Launches specialized agents for each language
```

### Example 2: System Programming Project
```bash
# ROADMAP.md contains:
# - C kernel module
# - Rust user-space daemon
# - Assembly optimizations

/phase-breakdown 2
# Handles low-level languages appropriately
# Ensures ABI compatibility
```

### Example 3: Data Science Pipeline
```bash
# ROADMAP.md contains:
# - Python data ingestion
# - R statistical analysis
# - Julia ML models
# - Go API server

/phase-breakdown 3
# Coordinates data formats between languages
# Ensures consistent interfaces
```

## 🔧 Customization

### Adding a New Language

1. Update `.claude/agents/interface-designer.md`:
```yaml
# Add to LANGUAGE PATTERNS section
"Language": {
  interface: "interface ClassName { }",
  method: "functionName(param: Type): ReturnType",
  test_framework: "language-test",
  compile_command: "language-compiler"
}
```

2. Update `.claude/agents/test-builder.md` with test patterns
3. Update `.claude/agents/coder.md` with implementation patterns
4. Add to `Master Makefile` build rules

### Custom Workflows

Create your own slash commands:
```bash
# .claude/commands/security-scan.md
---
allowed-tools: Bash(security-scanner:*)
description: Run security scans across all languages
argument-hint: [critical|high|medium|low]
---

Scan all worktrees for security vulnerabilities...
```

## 🎯 Best Practices

1. **Always define interfaces first** - Let the interface-designer create boundaries
2. **Test stubs before implementation** - Catch interface issues early
3. **One feature per worktree** - Maintain clean separation
4. **Language-appropriate testing** - Use native test frameworks
5. **Regular integration** - Merge frequently to avoid conflicts

## 🐛 Troubleshooting

### Common Issues

**Issue**: Language not detected
```bash
# Solution: Check file markers
./detect-language.sh path/to/component
# Add appropriate config files (Cargo.toml, go.mod, etc.)
```

**Issue**: Merge conflicts
```bash
# Solution: Interfaces weren't properly defined
# Rollback and rerun interface-designer
/phase-breakdown --retry-interfaces
```

**Issue**: Tests failing in integration
```bash
# Solution: Check language interop
make integration-test
# Review interface compatibility
```

## 📚 Additional Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code/)
- [Git Worktree Guide](https://git-scm.com/docs/git-worktree)
- Language-specific guides in `.claude/docs/languages/`

## 🎉 Ready to Build!

Your multi-language Claude Code template is now ready. Start with:

```bash
claude
/phase-breakdown 1
```

Watch as your AI agents coordinate across languages to build your project with zero merge conflicts! 🚀