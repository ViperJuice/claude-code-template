.PHONY: all build test run clean

all: build

build:
	@echo "Building Payment Service (Rust)..."
	cd payment-service && cargo build --release
	@echo "Building Order Service (Go)..."
	cd order-service && go build -o order-service

test:
	@echo "Testing Payment Service..."
	cd payment-service && cargo test
	@echo "Testing Order Service..."
	cd order-service && go test ./...

run-payment:
	cd payment-service && cargo run

run-order:
	cd order-service && go run .

run: build
	@echo "Starting services..."
	@trap 'kill %1; kill %2' INT; \
	cd payment-service && cargo run & \
	cd order-service && ./order-service & \
	wait

integration-test: build
	@echo "Running integration tests..."
	./tests/integration.sh

clean:
	cd payment-service && cargo clean
	cd order-service && rm -f order-service
	rm -rf worktrees/