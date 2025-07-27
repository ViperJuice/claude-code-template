# Rust + Go Microservices Example

This example demonstrates building high-performance microservices using Rust for payment processing and Go for order management.

## Architecture

```
┌─────────────┐     ┌──────────────┐
│   Client    │────▶│ Order Service│
└─────────────┘     │     (Go)     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │Payment Service│
                    │    (Rust)    │
                    └──────────────┘
```

## Services

### Payment Service (Rust)
- High-performance payment processing
- Fraud detection
- Transaction logging
- WebAssembly ready

### Order Service (Go)
- Concurrent order processing
- Inventory management
- Payment integration
- Event streaming

## Running the Example

1. **Using Claude Code**:
   ```bash
   cd examples/rust-go-microservices
   claude
   /phase-breakdown 1
   ```

2. **Manual Development**:
   ```bash
   # Terminal 1: Payment Service
   cd payment-service
   cargo run

   # Terminal 2: Order Service
   cd order-service
   go run .
   ```

## Testing

```bash
# Run all tests
make test

# Run integration tests
make integration-test
```

## Project Structure

```
rust-go-microservices/
├── README.md
├── Makefile
├── specs/
│   └── ROADMAP.md
├── payment-service/    # Rust service
│   ├── Cargo.toml
│   ├── src/
│   └── tests/
├── order-service/      # Go service
│   ├── go.mod
│   ├── main.go
│   └── tests/
└── tests/             # Integration tests
    └── integration.sh
```