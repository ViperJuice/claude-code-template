# Claude Code Multi-Language Project Template

[![Claude Code Compatible](https://img.shields.io/badge/Claude%20Code-Compatible-blue)](https://docs.anthropic.com/en/docs/claude-code/)
[![Languages](https://img.shields.io/badge/Languages-33-green)](docs/languages.md)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

This template provides a complete Claude Code setup with native sub-agents for orchestrating parallel development across 33 programming languages with zero merge conflicts.

## Features

- **25 Specialized AI Sub-Agents**: 9 core orchestration agents + 16 language-specific agents
- **33 Language Support**: From systems languages (C/C++/Rust) to modern web (TypeScript/Go)
- **Zero Merge Conflicts**: Git work tree isolation ensures parallel development
- **TDD Enforcement**: Tests are written before implementation
- **Automated Documentation**: Keeps docs in sync with code
- **CI/CD Ready**: GitHub Actions workflow included

## Project Structure

```bash
.claude/
├── agents/           # AI sub-agents for orchestration
├── commands/         # Slash commands (/phase-breakdown)
├── scripts/          # Helper scripts
├── state/            # Runtime state (git-ignored)
└── config.json       # Multi-language configuration

worktrees/           # Isolated development branches
docs/                # Project documentation
tests/               # Integration tests
specs/               # Project specifications (ROADMAP.md)
```

## Quick Start

1. **Clone this template**

   ```bash
   git clone https://github.com/ViperJuice/claude-code-template my-project
   cd my-project
   ```

2. **Install dependencies and initialize**

   ```bash
   # Install Python dependencies (including uv for hooks)
   pip install -r requirements.txt
   
   # Run setup script
   ./scripts/setup.sh
   ```

3. **Try example projects**

   ```bash
   # Run all examples
   ./scripts/run-examples.sh
   
   # Run specific example
   ./scripts/run-examples.sh python-ml-typescript-api
   ```

4. **Create your roadmap**

   ```bash
   # Copy an example as starting point
   cp examples/rust-go-microservices my-project
   cd my-project
   
   # Edit specs/ROADMAP.md with your phase definitions
   ```

5. **Start development**

   ```bash
   claude
   /phase-breakdown 1
   ```

## Sub-Agents

| Agent | Purpose |
|-------|---------|
| **phase-architect** | Master orchestrator, analyzes roadmap and coordinates execution |
| **interface-designer** | Creates language-agnostic interfaces and boundaries |
| **interface-verifier** | Validates interfaces compile and have no circular dependencies |
| **worktree-manager** | Sets up isolated Git work trees for parallel development |
| **worktree-lead** | Manages implementation of a single component |
| **test-builder** | Creates comprehensive test suites (TDD red phase) |
| **coder** | Implements features to pass tests (TDD green phase) |
| **integration-guardian** | Manages PR merges and ensures quality gates |
| **doc-scribe** | Updates documentation after features are merged |

## Supported Languages

### Systems Programming

C, C++, Rust, Zig, Assembly (x86, ARM)

### Enterprise

Java, C#, Go, Kotlin, Scala

### Web Development

TypeScript, JavaScript, Dart, PHP, Ruby

### Data Science & ML

Python, R, Julia, MATLAB

### Functional

Haskell, Elixir, Erlang, F#, OCaml, Clojure

### Mobile

Swift, Kotlin, Dart (Flutter)

### Emerging

Mojo, Carbon, V

## Example Workflow

### Phase 1: Define Your Project

Create a `ROADMAP.md` in the `specs/` directory:

```markdown
## Phase 1: Core Services
- **payment-service** (Rust) - High-performance payment processing
- **order-service** (Go) - Concurrent order management
- **analytics** (Python) - ML-powered insights
```

### Phase 2: Execute

```bash
claude
/phase-breakdown 1
```

### Phase 3: Watch the Magic

- Interfaces are automatically created
- Work trees are set up for each service
- Tests are written first (TDD)
- Implementation happens in parallel
- PRs are created and merged automatically
- Documentation is updated

## Configuration

Edit `.claude/config.json` to customize:

- Language preferences
- Test coverage thresholds
- Build commands
- Linting rules

## CI/CD

Includes GitHub Actions workflow that:

- Detects all languages automatically
- Runs language-specific tests
- Generates coverage reports
- Builds Docker images
- Runs integration tests

## Documentation

- [Implementation Guide](docs/implementation-guide.md)
- [Language Support Matrix](docs/languages.md)
- [Architecture Overview](docs/architecture/README.md)
- [API Reference](docs/api/README.md)
- [Helper Scripts](docs/helpers.md)

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) first.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

Built for use with [Claude Code](https://docs.anthropic.com/en/docs/claude-code/) by Anthropic.

---

**Ready to build something amazing?** Start with `/phase-breakdown 1` and let Claude orchestrate your development!