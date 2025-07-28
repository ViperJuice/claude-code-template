# Supported Languages

The Claude Code Multi-Language Template supports **33 programming languages** organized into 8 language families for optimal context management and code generation.

## Language Families and Their Languages

### 1. Systems Programming Languages (5 languages)
Handled by: `test-builder-systems` and `coder-systems`

| Language | Extensions | Test Framework | Build Tool |
|----------|------------|----------------|------------|
| **C** | `.c`, `.h` | Check, Unity, CUnit | make, gcc |
| **C++** | `.cpp`, `.cc`, `.hpp`, `.h` | Google Test, Catch2 | cmake, make |
| **Rust** | `.rs` | Built-in `#[test]` | cargo |
| **Go** | `.go` | Built-in `testing` | go build |
| **Zig** | `.zig` | Built-in `test` | zig build |

### 2. JVM Languages (4 languages)
Handled by: `test-builder-jvm` and `coder-jvm`

| Language | Extensions | Test Framework | Build Tool |
|----------|------------|----------------|------------|
| **Java** | `.java` | JUnit 5, TestNG | Maven, Gradle |
| **Kotlin** | `.kt` | Kotest, JUnit 5 | Gradle, Maven |
| **Scala** | `.scala` | ScalaTest, Specs2 | SBT, Maven |
| **Clojure** | `.clj`, `.cljs`, `.cljc` | clojure.test, Midje | Leiningen |

### 3. Web Development Languages (5 languages)
Handled by: `test-builder-web` and `coder-web`

| Language | Extensions | Test Framework | Build Tool |
|----------|------------|----------------|------------|
| **JavaScript** | `.js`, `.jsx` | Jest, Vitest, Mocha | npm, yarn |
| **TypeScript** | `.ts`, `.tsx` | Jest, Vitest | npm, yarn |
| **JSX** | `.jsx` | Jest + React Testing Library | npm, yarn |
| **TSX** | `.tsx` | Jest + React Testing Library | npm, yarn |
| **Vue** | `.vue` | Vue Test Utils + Vitest | npm, yarn |

### 4. Scripting Languages (5 languages)
Handled by: `test-builder-scripting` and `coder-scripting`

| Language | Extensions | Test Framework | Build Tool |
|----------|------------|----------------|------------|
| **Python** | `.py` | pytest, unittest | pip, poetry |
| **Ruby** | `.rb` | RSpec, Minitest | bundler |
| **Perl** | `.pl`, `.pm` | Test::More, Test::Unit | cpan |
| **Bash** | `.sh`, `.bash` | Bats, shUnit2 | N/A |
| **Shell** | `.sh` | Bats, shUnit2 | N/A |

### 5. Mobile Development Languages (4 languages)
Handled by: `test-builder-mobile` and `coder-mobile`

| Language | Extensions | Test Framework | Build Tool |
|----------|------------|----------------|------------|
| **Swift** | `.swift` | XCTest, Quick/Nimble | xcodebuild, swift |
| **Objective-C** | `.m`, `.mm`, `.h` | XCTest, OCMock | xcodebuild |
| **Dart** | `.dart` | flutter_test | dart, flutter |
| **React Native** | `.js`, `.jsx` | Jest + RN Testing Library | npm, yarn |

### 6. Functional Programming Languages (6 languages)
Handled by: `test-builder-functional` and `coder-functional`

| Language | Extensions | Test Framework | Build Tool |
|----------|------------|----------------|------------|
| **Haskell** | `.hs` | Hspec, QuickCheck | stack, cabal |
| **OCaml** | `.ml`, `.mli` | OUnit2, Alcotest | dune, ocamlbuild |
| **F#** | `.fs`, `.fsi`, `.fsx` | xUnit, FsUnit | dotnet |
| **Elixir** | `.ex`, `.exs` | ExUnit | mix |
| **Erlang** | `.erl`, `.hrl` | EUnit, Common Test | rebar3 |
| **Clojure** | `.clj`, `.cljs`, `.cljc` | clojure.test | lein |

### 7. Data/Scientific Languages (4 languages)
Handled by: `test-builder-data` and `coder-data`

| Language | Extensions | Test Framework | Build Tool |
|----------|------------|----------------|------------|
| **SQL** | `.sql` | tSQLt, pgTAP | Database-specific |
| **R** | `.r`, `.R` | testthat, RUnit | Rscript |
| **Julia** | `.jl` | Test (built-in) | julia |
| **MATLAB** | `.m` | MATLAB Unit Test | matlab |

### 8. Assembly Languages (4 languages)
Handled by: `test-builder-assembly` and `coder-assembly`

| Language | Extensions | Test Framework | Build Tool |
|----------|------------|----------------|------------|
| **x86/x86_64** | `.asm`, `.s` | Custom C harness | nasm, gas |
| **ARM** | `.s` | Custom C harness | as, gcc |
| **RISC-V** | `.S` | Custom C harness | riscv-as |
| **WebAssembly** | `.wat`, `.wasm` | Node.js test runner | wat2wasm |

## Language Detection

The system automatically detects languages in your project based on:
1. File extensions
2. Configuration files (package.json, Cargo.toml, etc.)
3. Build files (Makefile, pom.xml, etc.)

## Multi-Language Projects

The template excels at handling multi-language projects. For example:
- A microservices architecture with Rust (performance), Go (services), and TypeScript (frontend)
- A game engine in C++ with Python bindings and Lua scripting
- An enterprise system with Java backend, React frontend, and SQL databases

## Adding New Languages

To add support for a new language:
1. Add the language configuration to `.claude/config.json`
2. Assign it to the most appropriate language family agent
3. Update this documentation

## Language-Specific Features

Each language family agent includes:
- Idiomatic code patterns
- Language-specific best practices
- Appropriate error handling
- Performance optimizations
- Testing conventions
- Build tool integration

This approach ensures that code generation is optimized for each language's strengths while maintaining consistency across the project.