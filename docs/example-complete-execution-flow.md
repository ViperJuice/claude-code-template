# Example: Complete Phase Execution Flow

This example demonstrates how the native Claude Code sub-agents work together to execute Phase 2 (Core Features) with payment and order services.

## Initial State

```
Project structure:
├── ROADMAP.md (defines Phase 2: payment-service, order-service)
├── src/
├── tests/
└── .claude/
    ├── agents/ (all sub-agents installed)
    └── commands/phase-breakdown.md
```

## Execution Flow

### 1. Human Initiates Phase

```
Human: /phase-breakdown 2
```

### 2. Claude Code Main Thread

```javascript
// Claude reads phase-breakdown.md command and executes:
Task({
  description: "Orchestrate Phase 2 development",
  prompt: "Use the phase-architect sub agent to analyze and orchestrate Phase 2..."
});
```

### 3. Phase Architect Sub-Agent Activates

**Context**: Fresh context, reads ROADMAP.md

```bash
# Phase Architect analyzes Phase 2
cat ROADMAP.md
# Identifies: payment-service, order-service

# Creates execution plan
Write({
  path: ".claude/state/phase-2-plan.json",
  content: JSON.stringify({
    "phase": 2,
    "title": "Core Features",
    "components": [
      {
        "id": "payment-service",
        "interfaces": ["PaymentProcessor", "TransactionLogger"],
        "dependencies": []
      },
      {
        "id": "order-service",
        "interfaces": ["OrderManager", "OrderValidator"],
        "dependencies": ["payment-service"]
      }
    ]
  })
});

# Invokes interface designer
Task({
  description: "Design interfaces for Phase 2",
  prompt: "Use the interface-designer sub agent to create boundaries for phase 2..."
});
```

### 4. Interface Designer Sub-Agent Activates

**Context**: Fresh context, reads phase plan

```typescript
// Creates src/interfaces/payment-processor.ts
Write({
  path: "src/interfaces/payment-processor.ts",
  content: `
export interface PaymentProcessor {
  processPayment(amount: number, currency: string): Promise<PaymentResult>;
  refundPayment(transactionId: string): Promise<RefundResult>;
}

export interface PaymentResult {
  transactionId: string;
  status: 'success' | 'failed' | 'pending';
  timestamp: Date;
}

export interface RefundResult {
  refundId: string;
  originalTransactionId: string;
  amount: number;
  status: 'completed' | 'failed';
}`
});

// Creates stub implementations
Write({
  path: "src/stubs/payment-processor.stub.ts",
  content: `
export class PaymentProcessorStub implements PaymentProcessor {
  async processPayment(amount: number, currency: string): Promise<PaymentResult> {
    // TODO: Implement in payment-service worktree
    throw new Error('Not implemented - assigned to payment-service team');
  }
}`
});

// Documents boundaries
Write({
  path: ".claude/state/phase-2-boundaries.md",
  content: `
# Phase 2 Boundaries

## payment-service
- Owns: PaymentProcessor, TransactionLogger
- Worktree: worktrees/payment-service
- Called by: order-service

## order-service  
- Owns: OrderManager, OrderValidator
- Worktree: worktrees/order-service
- Depends on: payment-service`
});

# Signals completion back to architect
```

### 5. Phase Architect Creates Worktrees

```bash
# Back in architect's context
# Creates worktrees for parallel work
git worktree add ./worktrees/payment-service -b feature/phase-2-payment-service
git worktree add ./worktrees/order-service -b feature/phase-2-order-service

# Copies interfaces to each worktree
cp -r src/interfaces worktrees/payment-service/src/
cp -r src/interfaces worktrees/order-service/src/

# Launches payment-service first (no dependencies)
Task({
  description: "Implement payment-service",
  prompt: "Use the worktree-lead sub agent to implement payment-service in worktrees/payment-service for phase 2"
});
```

### 6. Worktree Lead (Payment) Activates

**Context**: Fresh context for payment-service

```bash
# Navigate to worktree
cd worktrees/payment-service
pwd  # Confirms: /project/worktrees/payment-service

# Invoke test builder
Task({
  description: "Create tests for payment-service",
  prompt: "Use the test-builder sub agent to create tests for PaymentProcessor interface"
});
```

### 7. Test Builder Creates Tests

```typescript
// Creates tests/payment-processor.test.ts
Write({
  path: "tests/payment-processor.test.ts",
  content: `
describe('PaymentProcessor', () => {
  let processor: PaymentProcessor;
  
  beforeEach(() => {
    processor = new PaymentProcessor();
  });
  
  describe('processPayment', () => {
    it('should process valid payment', async () => {
      const result = await processor.processPayment(100, 'USD');
      expect(result.status).toBe('success');
      expect(result.transactionId).toMatch(/^TXN-/);
    });
    
    it('should reject negative amounts', async () => {
      await expect(processor.processPayment(-10, 'USD'))
        .rejects.toThrow('Invalid amount');
    });
    
    it('should handle timeouts gracefully', async () => {
      // Test timeout handling
    });
  });
});`
});

# Run tests - they should fail
npm test  # All red - perfect for TDD!
```

### 8. Worktree Lead Invokes Coder

```javascript
Task({
  description: "Implement payment-service",
  prompt: "Use the coder sub agent to implement PaymentProcessor to make all tests pass"
});
```

### 9. Coder Implements Feature

```typescript
// Implements src/services/payment-processor.ts
Write({
  path: "src/services/payment-processor.ts",
  content: `
import { PaymentProcessor, PaymentResult } from '../interfaces/payment-processor';
import { v4 as uuidv4 } from 'uuid';

export class PaymentProcessorImpl implements PaymentProcessor {
  async processPayment(amount: number, currency: string): Promise<PaymentResult> {
    // Validate input
    if (amount <= 0) {
      throw new Error('Invalid amount');
    }
    
    // Simulate payment processing
    const transactionId = \`TXN-\${uuidv4()}\`;
    
    // In real implementation, would call payment gateway
    const result: PaymentResult = {
      transactionId,
      status: 'success',
      timestamp: new Date()
    };
    
    return result;
  }
  
  async refundPayment(transactionId: string): Promise<RefundResult> {
    // Implementation...
  }
}`
});

# Run tests again
npm test  # All green!
npm run coverage  # 85% coverage
```

### 10. Worktree Lead Completes

```bash
# Commit and push
git add -A
git commit -m "feat: implement payment-service for phase 2"
git push -u origin feature/phase-2-payment-service

# Create PR
gh pr create --title "feat: [Phase 2] Payment Service" \
  --body "Implements PaymentProcessor with 85% test coverage"

# Update status
Write({
  path: "../../.claude/state/payment-service-status.json",
  content: '{"status": "completed", "pr": 123}'
});
```

### 11. Phase Architect Monitors & Launches Order Service

```javascript
// Architect detects payment-service completion
// Now launches order-service (which depends on payment)

Task({
  description: "Implement order-service",
  prompt: "Use the worktree-lead sub agent to implement order-service in worktrees/order-service for phase 2. Note: payment-service interfaces are now available."
});
```

### 12. Order Service Implementation

Similar flow:
- Worktree Lead → Test Builder → Coder
- Can now import PaymentProcessor interface
- Creates OrderManager that uses PaymentProcessor

### 13. Integration Guardian Activates

Once both services complete:

```bash
# Check PRs
gh pr list --state open --label "phase-2"
# Shows: PR #123 (payment), PR #124 (order)

# Test each PR
gh pr checkout 123
npm test
npm run test:integration

# Merge payment first
gh pr merge 123 --merge --delete-branch

# Then merge order
gh pr checkout 124
npm test
gh pr merge 124 --merge --delete-branch

# Invoke documentation update
Task({
  description: "Update documentation",
  prompt: "Use the doc-scribe sub agent to update docs for new payment and order services"
});
```

### 14. Doc Scribe Updates Documentation

```markdown
// Updates README.md
## New in Phase 2

### Payment Service
- Process payments in multiple currencies
- Handle refunds
- Transaction logging

### Order Service  
- Create and validate orders
- Integrate with payment processing
- Order status tracking

See `/docs/api/` for detailed API documentation.
```

### 15. Phase Complete

Phase Architect updates final status:

```json
{
  "phase": 2,
  "status": "completed",
  "components": ["payment-service", "order-service"],
  "duration": "45 minutes",
  "prs_merged": [123, 124]
}
```

## Key Observations

1. **Clean Context Separation**: Each sub-agent starts fresh, preventing confusion
2. **Parallel Execution**: Payment and order services developed simultaneously
3. **Dependency Management**: Order service waits for payment completion
4. **TDD Enforcement**: Tests written before implementation
5. **Automatic Coordination**: Sub-agents invoke each other via Task tool
6. **Zero Merge Conflicts**: Worktrees ensure isolation
7. **Quality Gates**: Tests, coverage, linting at each step

## Monitoring During Execution

```bash
# In another terminal
./monitor-phase.sh

# Shows:
Phase Status:
{
  "phase": 2,
  "status": "in_progress",
  "payment-service": "completed",
  "order-service": "in_progress"
}

Active Worktrees:
  • payment-service (branch: feature/phase-2-payment-service)
  • order-service (branch: feature/phase-2-order-service)
```

This demonstrates the power of Claude Code's native sub-agent system - complex parallel workflows with simple, maintainable configuration!