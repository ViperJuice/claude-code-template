# Python ML + TypeScript API Example

This example demonstrates building a machine learning service with Python and exposing it through a TypeScript API gateway.

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Client    │────▶│ API Gateway  │────▶│ ML Service  │
└─────────────┘     │ (TypeScript) │     │  (Python)   │
                    └──────────────┘     └─────────────┘
```

## Services

### ML Service (Python)
- Sentiment analysis model
- Text classification
- Model training endpoints
- Batch prediction support

### API Gateway (TypeScript)
- RESTful API endpoints
- Request validation
- Response caching
- Rate limiting

## Running the Example

1. **Using Claude Code**:
   ```bash
   cd examples/python-ml-typescript-api
   claude
   /phase-breakdown 1
   ```

2. **Manual Development**:
   ```bash
   # Terminal 1: ML Service
   cd ml-service
   pip install -r requirements.txt
   python main.py

   # Terminal 2: API Gateway
   cd api-gateway
   npm install
   npm run dev
   ```

## Testing

```bash
# Run all tests
make test

# Test the ML predictions
make test-predictions
```

## API Examples

```bash
# Analyze sentiment
curl -X POST http://localhost:3000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is amazing!"}'

# Batch prediction
curl -X POST http://localhost:3000/api/batch-analyze \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Great service!", "Terrible experience"]}'
```