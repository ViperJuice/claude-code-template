# Master Makefile for Multi-Language Project
# Coordinates builds across all languages

.PHONY: all build test lint coverage clean help

# Detect which components exist
COMPONENTS := $(shell find . -type f -name "Cargo.toml" -o -name "go.mod" -o -name "CMakeLists.txt" -o -name "pom.xml" -o -name "package.json" -o -name "requirements.txt" -o -name "pubspec.yaml" | xargs -I {} dirname {} | sort -u)

# Language-specific build commands
define build-rust
	@echo "🦀 Building Rust components..."
	@for dir in $$(find . -name "Cargo.toml" -exec dirname {} \;); do \
		echo "  Building $$dir"; \
		(cd $$dir && cargo build --release) || exit 1; \
	done
endef

define build-go
	@echo "🐹 Building Go components..."
	@for dir in $$(find . -name "go.mod" -exec dirname {} \;); do \
		echo "  Building $$dir"; \
		(cd $$dir && go build ./...) || exit 1; \
	done
endef

define build-cpp
	@echo "⚙️  Building C/C++ components..."
	@for dir in $$(find . -name "CMakeLists.txt" -exec dirname {} \;); do \
		echo "  Building $$dir"; \
		(cd $$dir && mkdir -p build && cd build && cmake .. && make -j$$(nproc)) || exit 1; \
	done
	@for dir in $$(find . -name "Makefile" ! -path "*/build/*" ! -path "./*" -exec dirname {} \;); do \
		echo "  Building $$dir"; \
		(cd $$dir && make) || exit 1; \
	done
endef

define build-java
	@echo "☕ Building Java components..."
	@for dir in $$(find . -name "pom.xml" -exec dirname {} \;); do \
		echo "  Building $$dir"; \
		(cd $$dir && mvn clean package) || exit 1; \
	done
	@for dir in $$(find . -name "build.gradle" -exec dirname {} \;); do \
		echo "  Building $$dir"; \
		(cd $$dir && gradle build) || exit 1; \
	done
endef

define build-python
	@echo "🐍 Setting up Python components..."
	@for dir in $$(find . -name "requirements.txt" -exec dirname {} \;); do \
		echo "  Setting up $$dir"; \
		(cd $$dir && python -m venv venv && . venv/bin/activate && pip install -r requirements.txt) || exit 1; \
	done
endef

define build-typescript
	@echo "📘 Building TypeScript components..."
	@for dir in $$(find . -name "package.json" -exec dirname {} \;); do \
		if grep -q "typescript" $$dir/package.json; then \
			echo "  Building $$dir"; \
			(cd $$dir && npm install && npm run build) || exit 1; \
		fi \
	done
endef

define build-dart
	@echo "🎯 Building Dart/Flutter components..."
	@for dir in $$(find . -name "pubspec.yaml" -exec dirname {} \;); do \
		echo "  Building $$dir"; \
		if [ -f "$$dir/lib/main.dart" ]; then \
			(cd $$dir && flutter pub get && flutter build apk --release) || exit 1; \
		else \
			(cd $$dir && dart pub get && dart compile exe bin/main.dart) || exit 1; \
		fi \
	done
endef

define build-assembly
	@echo "⚡ Building Assembly components..."
	@for file in $$(find . -name "*.asm" -o -name "*.s"); do \
		echo "  Assembling $$file"; \
		if [[ $$file == *.asm ]]; then \
			nasm -f elf64 $$file -o $${file%.asm}.o || exit 1; \
		else \
			as $$file -o $${file%.s}.o || exit 1; \
		fi \
	done
endef

# Main targets
all: build test

help:
	@echo "Multi-Language Build System"
	@echo "=========================="
	@echo ""
	@echo "Targets:"
	@echo "  make build     - Build all components"
	@echo "  make test      - Run all tests"
	@echo "  make lint      - Run linters for all languages"
	@echo "  make coverage  - Generate coverage reports"
	@echo "  make clean     - Clean all build artifacts"
	@echo "  make docker    - Build Docker images"
	@echo ""
	@echo "Language-specific targets:"
	@echo "  make build-rust    - Build only Rust components"
	@echo "  make build-go      - Build only Go components"
	@echo "  make build-cpp     - Build only C/C++ components"
	@echo "  make build-java    - Build only Java components"
	@echo "  make build-python  - Build only Python components"
	@echo "  make build-dart    - Build only Dart/Flutter components"
	@echo ""
	@echo "Detected components:"
	@for comp in $(COMPONENTS); do echo "  $$comp"; done

build:
	@echo "🚀 Building all components..."
	$(call build-cpp)
	$(call build-assembly)
	$(call build-rust)
	$(call build-go)
	$(call build-java)
	$(call build-python)
	$(call build-typescript)
	$(call build-dart)
	@echo "✅ Build complete!"

test:
	@echo "🧪 Running all tests..."
	@echo ""
	@echo "🦀 Rust tests..."
	@for dir in $$(find . -name "Cargo.toml" -exec dirname {} \;); do \
		(cd $$dir && cargo test) || exit 1; \
	done
	@echo ""
	@echo "🐹 Go tests..."
	@for dir in $$(find . -name "go.mod" -exec dirname {} \;); do \
		(cd $$dir && go test -v ./...) || exit 1; \
	done
	@echo ""
	@echo "⚙️  C/C++ tests..."
	@for dir in $$(find . -name "CMakeLists.txt" -exec dirname {} \;); do \
		if [ -d "$$dir/build" ]; then \
			(cd $$dir/build && ctest --verbose) || exit 1; \
		fi \
	done
	@echo ""
	@echo "☕ Java tests..."
	@for dir in $$(find . -name "pom.xml" -exec dirname {} \;); do \
		(cd $$dir && mvn test) || exit 1; \
	done
	@echo ""
	@echo "🐍 Python tests..."
	@for dir in $$(find . -name "requirements.txt" -exec dirname {} \;); do \
		if [ -d "$$dir/tests" ] || [ -d "$$dir/test" ]; then \
			(cd $$dir && . venv/bin/activate && pytest) || exit 1; \
		fi \
	done
	@echo ""
	@echo "📘 TypeScript tests..."
	@for dir in $$(find . -name "package.json" -exec dirname {} \;); do \
		if grep -q "test" $$dir/package.json; then \
			(cd $$dir && npm test) || exit 1; \
		fi \
	done
	@echo ""
	@echo "🎯 Dart tests..."
	@for dir in $$(find . -name "pubspec.yaml" -exec dirname {} \;); do \
		if [ -d "$$dir/test" ]; then \
			(cd $$dir && dart test) || exit 1; \
		fi \
	done
	@echo "✅ All tests passed!"

lint:
	@echo "🔍 Running linters..."
	# Rust
	@cargo clippy --all-features -- -D warnings 2>/dev/null || true
	# Go
	@golangci-lint run ./... 2>/dev/null || true
	# C/C++
	@find . -name "*.c" -o -name "*.cpp" -o -name "*.h" -o -name "*.hpp" | xargs clang-tidy 2>/dev/null || true
	# Python
	@find . -name "*.py" | xargs pylint --errors-only 2>/dev/null || true
	# TypeScript
	@for dir in $$(find . -name "package.json" -exec dirname {} \;); do \
		(cd $$dir && npm run lint 2>/dev/null) || true; \
	done
	# Dart
	@for dir in $$(find . -name "pubspec.yaml" -exec dirname {} \;); do \
		(cd $$dir && dart analyze) || true; \
	done

coverage:
	@echo "📊 Generating coverage reports..."
	@mkdir -p coverage
	# Rust coverage
	@for dir in $$(find . -name "Cargo.toml" -exec dirname {} \;); do \
		(cd $$dir && cargo tarpaulin --out Html --output-dir ../coverage/rust) || true; \
	done
	# Go coverage
	@for dir in $$(find . -name "go.mod" -exec dirname {} \;); do \
		(cd $$dir && go test -coverprofile=../coverage/go-coverage.out ./... && \
		 go tool cover -html=../coverage/go-coverage.out -o ../coverage/go-coverage.html) || true; \
	done
	# Python coverage
	@for dir in $$(find . -name "requirements.txt" -exec dirname {} \;); do \
		(cd $$dir && . venv/bin/activate && pytest --cov=. --cov-report=html:../coverage/python) || true; \
	done
	@echo "Coverage reports generated in coverage/"

clean:
	@echo "🧹 Cleaning build artifacts..."
	# Rust
	@find . -name "target" -type d -exec rm -rf {} + 2>/dev/null || true
	# Go
	@go clean -cache -modcache -i -r 2>/dev/null || true
	# C/C++
	@find . -name "build" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.o" -type f -delete 2>/dev/null || true
	@find . -name "*.so" -type f -delete 2>/dev/null || true
	@find . -name "*.a" -type f -delete 2>/dev/null || true
	# Java
	@find . -name "target" -type d -exec rm -rf {} + 2>/dev/null || true
	# Python
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -type f -delete 2>/dev/null || true
	@find . -name "venv" -type d -exec rm -rf {} + 2>/dev/null || true
	# Node
	@find . -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "dist" -type d -exec rm -rf {} + 2>/dev/null || true
	# Coverage
	@rm -rf coverage/
	@echo "✅ Clean complete!"

# Docker targets
docker:
	@echo "🐳 Building Docker images..."
	@for dockerfile in $$(find . -name "Dockerfile"); do \
		dir=$$(dirname $$dockerfile); \
		name=$$(basename $$dir); \
		echo "  Building $$name..."; \
		(cd $$dir && docker build -t $$name:latest .) || exit 1; \
	done

# Language-specific targets
build-rust:
	$(call build-rust)

build-go:
	$(call build-go)

build-cpp:
	$(call build-cpp)

build-java:
	$(call build-java)

build-python:
	$(call build-python)

build-typescript:
	$(call build-typescript)

build-dart:
	$(call build-dart)

build-assembly:
	$(call build-assembly)

# Integration test target
integration-test:
	@echo "🔗 Running integration tests..."
	docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
	docker-compose -f docker-compose.test.yml down

# Performance benchmarks
benchmark:
	@echo "⚡ Running benchmarks..."
	# Rust benchmarks
	@for dir in $$(find . -name "Cargo.toml" -exec dirname {} \;); do \
		(cd $$dir && cargo bench) || true; \
	done
	# Go benchmarks
	@for dir in $$(find . -name "go.mod" -exec dirname {} \;); do \
		(cd $$dir && go test -bench=. ./...) || true; \
	done

# Security scan
security-scan:
	@echo "🔒 Running security scans..."
	# Rust
	@cargo audit 2>/dev/null || true
	# Go
	@gosec ./... 2>/dev/null || true
	# Python
	@bandit -r . 2>/dev/null || true
	# Node
	@npm audit 2>/dev/null || true

# Format all code
format:
	@echo "✨ Formatting code..."
	# Rust
	@cargo fmt --all 2>/dev/null || true
	# Go
	@gofmt -w . 2>/dev/null || true
	# C/C++
	@find . -name "*.c" -o -name "*.cpp" -o -name "*.h" -o -name "*.hpp" | xargs clang-format -i 2>/dev/null || true
	# Python
	@black . 2>/dev/null || true
	# Dart
	@dart format . 2>/dev/null || true