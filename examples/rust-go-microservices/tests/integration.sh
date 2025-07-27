#!/bin/bash

echo "Starting integration tests..."

# Start services in background
cd payment-service && cargo run &
PAYMENT_PID=$!

cd order-service && go run . &
ORDER_PID=$!

# Wait for services to start
sleep 3

# Test health endpoints
echo "Testing health endpoints..."
curl -s http://localhost:8001/health | grep -q "healthy" || { echo "Payment service health check failed"; exit 1; }
curl -s http://localhost:8002/health | grep -q "healthy" || { echo "Order service health check failed"; exit 1; }

# Test order creation
echo "Testing order creation..."
ORDER_RESPONSE=$(curl -s -X POST http://localhost:8002/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "cust_123",
    "items": [
      {
        "product_id": "prod_456",
        "quantity": 2,
        "price": "29.99"
      }
    ]
  }')

ORDER_ID=$(echo $ORDER_RESPONSE | grep -o '"order_id":"[^"]*' | cut -d'"' -f4)

if [ -z "$ORDER_ID" ]; then
  echo "Failed to create order"
  kill $PAYMENT_PID $ORDER_PID
  exit 1
fi

echo "Order created with ID: $ORDER_ID"

# Test order retrieval
echo "Testing order retrieval..."
curl -s http://localhost:8002/orders/$ORDER_ID | grep -q "$ORDER_ID" || { echo "Order retrieval failed"; exit 1; }

# Cleanup
kill $PAYMENT_PID $ORDER_PID

echo "Integration tests passed!"