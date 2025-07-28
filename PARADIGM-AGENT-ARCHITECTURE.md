# Paradigm-Based Agent Architecture

## Overview

This document outlines a paradigm-based approach to organizing Claude Code agents, moving away from simple language-family groupings to agents that specialize in specific programming paradigms and design patterns.

## Motivation

The current language-family approach (e.g., "scripting languages" for Python, Ruby, Perl, PHP) fails to capture the fundamental differences in how these languages are used:

- **Python** can be used for OOP (Django models), functional programming (data pipelines), or scientific computing
- **JavaScript** supports OOP, functional, reactive, and event-driven paradigms
- **Scala** is designed as an OOP/FP hybrid

Agents need to understand **programming paradigms and design philosophies**, not just syntax.

## Proposed Architecture

### Agent Naming Convention

All agents remain in `.claude/agents/` with structured naming:

- `{paradigm}-specialist.md` - Pure paradigm specialists
- `{paradigm}-{language}-coder.md` - Language-specific paradigm experts
- `{paradigm}-{language}-test-builder.md` - Paradigm-aware test builders
- `{domain}-expert.md` - Domain specialists
- `{tool}-specialist.md` - Tool/language specialists

### Core Agent Categories

#### 1. Paradigm Specialists
Pure paradigm experts that understand patterns across languages:

- `oop-specialist.md` - Object-Oriented Programming patterns & SOLID principles
- `functional-specialist.md` - Functional programming concepts (monads, functors)
- `reactive-specialist.md` - Event-driven and reactive programming
- `concurrent-specialist.md` - Concurrency and parallelism patterns
- `systems-specialist.md` - Low-level systems programming patterns

#### 2. OOP Language Experts
Masters of GoF patterns and language-specific OOP:

- `oop-java-coder.md` - Java with Spring, Enterprise patterns
- `oop-csharp-coder.md` - C# with .NET patterns, LINQ
- `oop-python-coder.md` - Python OOP with duck typing, metaclasses
- `oop-cpp-coder.md` - C++ with templates, RAII
- `oop-ruby-coder.md` - Ruby with metaprogramming
- `oop-php-coder.md` - PHP with modern OOP patterns

#### 3. Functional Language Experts
FP patterns and paradigm-specific idioms:

- `functional-haskell-coder.md` - Monads, type classes, lazy evaluation
- `functional-scala-coder.md` - Hybrid FP/OOP, Cats, Scalaz
- `functional-clojure-coder.md` - STM, persistent data structures
- `functional-fsharp-coder.md` - Computation expressions, type providers
- `functional-ocaml-coder.md` - Modules, functors
- `functional-elixir-coder.md` - Actor model, OTP

#### 4. Reactive/Event-Driven Experts
Event sourcing, streams, and reactive patterns:

- `reactive-javascript-coder.md` - RxJS, EventEmitter, Promises
- `reactive-java-coder.md` - Project Reactor, RxJava
- `reactive-csharp-coder.md` - Rx.NET, IObservable

#### 5. Concurrent Programming Experts
Async patterns and parallel programming:

- `concurrent-go-coder.md` - Goroutines, channels, CSP
- `concurrent-rust-coder.md` - async/await, tokio, fearless concurrency
- `concurrent-java-coder.md` - CompletableFuture, ExecutorService
- `concurrent-python-coder.md` - asyncio, threading, multiprocessing

#### 6. Systems Programming Experts
Low-level patterns and performance optimization:

- `systems-rust-coder.md` - Ownership, zero-cost abstractions
- `systems-c-coder.md` - Memory management, module pattern
- `systems-cpp-coder.md` - RAII, move semantics, templates
- `systems-zig-coder.md` - Comptime, explicit memory control

#### 7. Architecture Experts
High-level design patterns and architectural patterns:

- `architecture-ddd-expert.md` - Domain-Driven Design patterns
- `architecture-event-expert.md` - Event Sourcing, CQRS
- `architecture-microservices.md` - Service mesh, API patterns

#### 8. Specialized Tool Experts
Domain-specific languages and tools:

- `sql-specialist.md` - SQL optimization, query patterns
- `shell-specialist.md` - Bash/shell scripting patterns
- `config-specialist.md` - YAML, JSON, TOML patterns
- `regex-specialist.md` - Regular expression patterns

## Pattern Alignment

### GoF Patterns to Paradigm Mapping

**OOP Agents handle:**
- Creational: Abstract Factory, Builder, Factory Method, Prototype, Singleton
- Structural: Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy
- Behavioral: Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor

**Functional Agents handle:**
- HOC (Higher Order Components)
- Pipeline/Composition patterns
- Monadic patterns
- FP alternatives to OOP patterns (e.g., Strategy → Higher Order Functions)

**Reactive Agents handle:**
- Event Sourcing, CQRS
- Pub/Sub, Observer variants
- Reactor, Proactor patterns

**Concurrent Agents handle:**
- Future/Promise, Async/Await
- Worker Pool, Thread Pool
- Actor Model

## Implementation Strategy

### 1. Agent Selection Logic

```javascript
// In worktree-lead.md
async function selectAgents(component) {
  // Detect language
  const language = detectLanguage(component);
  
  // Detect paradigm using paradigm-detector
  const paradigm = await detectParadigm(component);
  
  // Select appropriate agents
  return paradigmAgentMap[language]?.[paradigm] || fallbackAgent(language);
}
```

### 2. Multi-Language Support

For embedded languages (e.g., SQL in Python):

1. Primary agent detects embedded language
2. Extracts context and constraints
3. Delegates to specialist via Task tool
4. Integrates response back into main code

Example:
```javascript
// In oop-python-coder.md
if (hasEmbeddedSQL(code)) {
  const optimizedSQL = await Task({
    description: "Optimize embedded SQL",
    prompt: `Optimize this query: ${sqlContext}`,
    subagent_type: "sql-specialist"
  });
  return integrateSQLResult(code, optimizedSQL);
}
```

### 3. Pattern Knowledge Structure

```
.claude/knowledge/patterns/
├── paradigm-patterns/
│   ├── oop/
│   │   ├── gof-patterns.json
│   │   └── ddd-patterns.json
│   ├── functional/
│   │   ├── fp-patterns.json
│   │   └── fp-alternatives.json
│   ├── reactive/
│   │   └── event-patterns.json
│   └── concurrent/
│       └── async-patterns.json
└── language-specific/
    ├── java-idioms.json
    └── python-idioms.json
```

## Benefits

1. **Paradigm Expertise**: Agents deeply understand their paradigm's patterns
2. **Cross-Language Learning**: OOP patterns from Java can inform Python OOP
3. **Better Pattern Selection**: FP agents won't suggest OOP patterns inappropriately
4. **Natural Multi-Paradigm Support**: Different agents for different parts of codebase
5. **Embedded Language Handling**: Specialists for SQL, regex, config files

## Migration Path

1. Create paradigm specialists and language-paradigm experts
2. Update worktree-lead with paradigm detection
3. Reorganize pattern files by paradigm
4. Test with multi-paradigm codebases
5. Remove old language-family agents

## Future Considerations

- **Framework-Specific Agents**: `spring-expert.md`, `django-expert.md`
- **Performance Specialists**: `rust-perf-expert.md`, `cpp-optimization-expert.md`
- **Testing Paradigms**: `tdd-expert.md`, `bdd-expert.md`, `property-testing-expert.md`

## Open Questions

1. Should we have "hybrid" agents for strongly multi-paradigm languages?
2. How deep should framework specialization go?
3. Should paradigm specialists be able to generate code or only advise?

---

*This architecture ensures that Claude Code agents can effectively apply design patterns idiomatically for each paradigm-language combination, maximizing the use of established patterns while respecting language-specific conventions.*