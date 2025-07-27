# Multi-Language Phase Execution Example

This example shows how Claude Code agents handle a phase with services written in different languages.

## Example: Phase 2 - Core Services

**Components:**
- Payment Service (Rust) - High-performance, memory-safe
- Order Service (Go) - Concurrent order processing  
- Analytics Engine (Python) - Data science libraries
- Legacy Integration (Java) - Enterprise system compatibility
- Firmware Module (C/Assembly) - Hardware control

## Execution Flow

### 1. Human Initiates

```
Human: /phase-breakdown 2
```

### 2. Phase Architect Analyzes

Phase architect reads ROADMAP and detects multi-language requirements:

```bash
# ROADMAP.md excerpt
## Phase 2: Core Services
- Payment processing (Rust) - High-performance transaction handling
- Order management (Go) - Concurrent order processing with channels
- Analytics engine (Python) - ML-powered fraud detection
- Legacy ERP connector (Java) - SOAP/XML integration
- Hardware security module (C/Assembly) - Cryptographic operations
```

### 3. Interface Designer Creates Language-Specific Interfaces

The interface-designer creates appropriate interface definitions for each language:

#### Rust Interface
```rust
// src/interfaces/payment_processor.rs
pub trait PaymentProcessor: Send + Sync {
    async fn process_payment(&self, request: PaymentRequest) -> Result<PaymentResult, PaymentError>;
    async fn validate_card(&self, card: &CreditCard) -> Result<bool, ValidationError>;
}
```

#### Go Interface
```go
// pkg/interfaces/order_manager.go
type OrderManager interface {
    CreateOrder(ctx context.Context, items []OrderItem) (*Order, error)
    ProcessConcurrentOrders(ctx context.Context, orders <-chan OrderRequest) <-chan OrderResult
}
```

#### Python Abstract Base Class
```python
# src/interfaces/analytics_engine.py
from abc import ABC, abstractmethod
import pandas as pd

class AnalyticsEngine(ABC):
    @abstractmethod
    async def detect_fraud(self, transaction: Transaction) -> FraudScore:
        """ML-based fraud detection"""
        pass
```

#### Java Interface
```java
// src/main/java/interfaces/ERPConnector.java
public interface ERPConnector {
    CompletableFuture<SAPResponse> syncWithSAP(Order order);
    XMLDocument transformToLegacyFormat(Order order);
}
```

#### C Header
```c
// include/crypto_module.h
typedef struct {
    uint8_t key[32];
    uint8_t iv[16];
} crypto_context_t;

int crypto_sign_transaction(const uint8_t* data, size_t len, uint8_t* signature);
int crypto_verify_signature(const uint8_t* data, size_t len, const uint8_t* signature);
```

### 4. Interface Verifier Checks All Languages

```bash
# Rust
cargo check --all-features ✓

# Go  
go build ./... ✓

# Python
mypy src/interfaces --strict ✓

# Java
mvn compile ✓

# C
gcc -fsyntax-only include/*.h ✓
```

### 5. Worktree Manager Creates Language-Specific Worktrees

```bash
# Each worktree has appropriate build files
git worktree add ./worktrees/payment-service -b feature/phase-2-payment
cp Cargo.toml worktrees/payment-service/

git worktree add ./worktrees/order-service -b feature/phase-2-orders  
cp go.mod worktrees/order-service/

git worktree add ./worktrees/analytics -b feature/phase-2-analytics
cp requirements.txt worktrees/analytics/

git worktree add ./worktrees/erp-connector -b feature/phase-2-erp
cp pom.xml worktrees/erp-connector/

git worktree add ./worktrees/crypto-module -b feature/phase-2-crypto
cp Makefile worktrees/crypto-module/
```

### 6. Language-Specific Test Builders Create Tests

#### Rust Tests (payment-service)
```rust
#[cfg(test)]
mod tests {
    use super::*;
    use tokio;
    
    #[tokio::test]
    async fn test_process_payment_success() {
        let processor = PaymentProcessorImpl::new();
        let request = PaymentRequest {
            amount: 99.99,
            currency: "USD".to_string(),
        };
        
        let result = processor.process_payment(request).await;
        assert!(result.is_ok());
    }
}
```

#### Go Tests (order-service)
```go
func TestProcessConcurrentOrders(t *testing.T) {
    manager := &OrderManagerImpl{}
    ctx := context.Background()
    
    orders := make(chan OrderRequest, 10)
    results := manager.ProcessConcurrentOrders(ctx, orders)
    
    // Send 10 orders concurrently
    go func() {
        for i := 0; i < 10; i++ {
            orders <- OrderRequest{ID: i}
        }
        close(orders)
    }()
    
    // Verify all processed
    count := 0
    for range results {
        count++
    }
    assert.Equal(t, 10, count)
}
```

#### Python Tests (analytics)
```python
@pytest.mark.asyncio
async def test_fraud_detection_ml_model():
    engine = AnalyticsEngineImpl()
    
    # Test with known fraudulent pattern
    transaction = Transaction(
        amount=9999.99,
        location="unusual_country",
        time_since_last=0.1  # Rapid transactions
    )
    
    score = await engine.detect_fraud(transaction)
    assert score.risk_level > 0.8  # High fraud probability
```

### 7. Language-Specific Coders Implement

Each coder uses language idioms:

#### Rust - Memory Safety & Performance
```rust
impl PaymentProcessor for PaymentProcessorImpl {
    async fn process_payment(&self, request: PaymentRequest) -> Result<PaymentResult, PaymentError> {
        // Use ? operator for error propagation
        let validated = self.validate_amount(request.amount)?;
        
        // Zero-copy string handling
        let currency = request.currency.as_str();
        
        // Concurrent processing with Tokio
        let (tx_result, fraud_check) = tokio::join!(
            self.gateway.process(validated),
            self.fraud_detector.check(&request)
        );
        
        // Pattern matching for elegant error handling
        match (tx_result, fraud_check) {
            (Ok(tx), Ok(false)) => Ok(PaymentResult::success(tx.id)),
            (Ok(_), Ok(true)) => Err(PaymentError::FraudDetected),
            (Err(e), _) => Err(PaymentError::Gateway(e)),
        }
    }
}
```

#### Go - Concurrency with Channels
```go
func (m *OrderManagerImpl) ProcessConcurrentOrders(ctx context.Context, orders <-chan OrderRequest) <-chan OrderResult {
    results := make(chan OrderResult)
    
    // Worker pool pattern
    var wg sync.WaitGroup
    for i := 0; i < runtime.NumCPU(); i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for order := range orders {
                select {
                case <-ctx.Done():
                    return
                default:
                    result := m.processOrder(order)
                    results <- result
                }
            }
        }()
    }
    
    // Cleanup goroutine
    go func() {
        wg.Wait()
        close(results)
    }()
    
    return results
}
```

#### Python - Data Science Libraries
```python
class AnalyticsEngineImpl(AnalyticsEngine):
    def __init__(self):
        self.model = joblib.load('fraud_detection_model.pkl')
        self.scaler = StandardScaler()
    
    async def detect_fraud(self, transaction: Transaction) -> FraudScore:
        # Feature engineering with pandas
        features = pd.DataFrame([{
            'amount': transaction.amount,
            'hour': transaction.timestamp.hour,
            'day_of_week': transaction.timestamp.weekday(),
            'merchant_risk': self._get_merchant_risk(transaction.merchant_id)
        }])
        
        # Async database query
        history = await self._get_user_history(transaction.user_id)
        features['velocity'] = self._calculate_velocity(history)
        
        # ML prediction
        scaled_features = self.scaler.transform(features)
        probability = self.model.predict_proba(scaled_features)[0, 1]
        
        return FraudScore(
            risk_level=probability,
            factors=self._explain_prediction(features, probability)
        )
```

#### Assembly - Low-Level Crypto
```asm
; crypto_sign_transaction - Hardware-accelerated signing
; Input: RDI = data ptr, RSI = length, RDX = signature out
crypto_sign_transaction:
    push rbp
    mov rbp, rsp
    
    ; Check CPU features for AES-NI
    mov eax, 1
    cpuid
    test ecx, 0x2000000  ; AES-NI bit
    jz .software_fallback
    
    ; Hardware-accelerated path
    ; Load key schedule
    movdqu xmm0, [crypto_key]
    
    ; Process data in 16-byte blocks
.aes_loop:
    cmp rsi, 16
    jl .final_block
    
    movdqu xmm1, [rdi]
    aesenc xmm1, xmm0
    movdqu [rdx], xmm1
    
    add rdi, 16
    add rdx, 16
    sub rsi, 16
    jmp .aes_loop
```

### 8. Integration Testing Across Languages

The integration-guardian runs cross-language tests:

```yaml
# docker-compose.test.yml
version: '3.8'
services:
  payment-service:
    build: ./worktrees/payment-service
    environment:
      - RUST_LOG=debug
  
  order-service:
    build: ./worktrees/order-service
    environment:
      - GO_ENV=test
  
  analytics:
    build: ./worktrees/analytics
    volumes:
      - ./ml-models:/app/models
  
  test-runner:
    build: ./integration-tests
    depends_on:
      - payment-service
      - order-service
      - analytics
    command: pytest integration_tests/ -v
```

### 9. Final Integration

All services communicate via gRPC/REST:

```
┌─────────────┐     gRPC      ┌──────────────┐
│   Rust      │◄─────────────►│     Go       │
│  Payment    │               │   Orders     │
└─────────────┘               └──────────────┘
       │                              │
       │         ┌────────┐          │
       └────────►│ Python │◄─────────┘
          REST   │Analytics│   REST
                 └────────┘
                      │
                      ▼
                ┌──────────┐
                │   Java   │
                │   ERP    │
                └──────────┘
```

## Benefits of Multi-Language Support

1. **Right Tool for the Job**
   - Rust for performance-critical payment processing
   - Go for concurrent order handling
   - Python for ML/data science
   - Java for enterprise integration
   - Assembly for hardware crypto

2. **Team Expertise**
   - Each team uses their strongest language
   - No forced language standardization
   - Leverage existing code/libraries

3. **Performance Optimization**
   - Critical paths in Rust/C/Assembly
   - Business logic in Go/Java
   - Analytics in Python
   - UI in TypeScript/Dart

4. **Gradual Migration**
   - Keep legacy Java while building new services
   - Incrementally replace components
   - No big-bang rewrites

The Claude Code agents handle all language differences seamlessly, allowing you to focus on building the best solution with the right tools!