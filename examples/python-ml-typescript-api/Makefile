.PHONY: all install test run clean

all: install

install:
	@echo "Installing ML Service dependencies..."
	cd ml-service && pip install -r requirements.txt
	@echo "Installing API Gateway dependencies..."
	cd api-gateway && npm install

test:
	@echo "Testing ML Service..."
	cd ml-service && python -m pytest tests/ || echo "No tests yet"
	@echo "Testing API Gateway..."
	cd api-gateway && npm test || echo "No tests yet"

run-ml:
	cd ml-service && python main.py

run-api:
	cd api-gateway && npm run dev

run: install
	@echo "Starting services..."
	@trap 'kill %1; kill %2' INT; \
	cd ml-service && python main.py & \
	cd api-gateway && npm run dev & \
	wait

test-predictions:
	@echo "Testing sentiment analysis..."
	@sleep 2
	@curl -s -X POST http://localhost:3000/api/analyze \
		-H "Content-Type: application/json" \
		-d '{"text": "This product is amazing!"}' | python -m json.tool
	@echo "\nTesting batch analysis..."
	@curl -s -X POST http://localhost:3000/api/batch-analyze \
		-H "Content-Type: application/json" \
		-d '{"texts": ["Great service!", "Terrible experience", "It was okay"]}' | python -m json.tool

clean:
	cd ml-service && rm -rf __pycache__ .pytest_cache
	cd api-gateway && rm -rf node_modules dist
	rm -rf worktrees/