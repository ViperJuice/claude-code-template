#!/bin/bash
# Run all example projects

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Running example projects...${NC}"

# Helper function to run an example project
run_example() {
    local name=$1
    echo -e "\n${YELLOW}Running $name example...${NC}"
    cd "examples/$name"
    
    # Run example-specific commands
    case $name in
        "rust-go-microservices")
            make build
            echo "Starting services..."
            make run &
            sleep 2
            echo "Running integration test..."
            make integration-test
            ;;
            
        "python-ml-typescript-api")
            make install
            echo "Starting services..."
            make run &
            sleep 2
            echo "Testing predictions..."
            make test-predictions
            ;;
            
        "cpp-java-python-engine")
            make all
            echo "Running benchmarks..."
            make benchmark
            ;;
            
        *)
            echo -e "${RED}Unknown example: $name${NC}"
            return 1
            ;;
    esac
    
    # Return to root directory
    cd ../..
}

# Run all examples or specific one
if [ $# -eq 0 ]; then
    # Run all examples
    for example in examples/*/; do
        if [ -d "$example" ]; then
            name=$(basename "$example")
            run_example "$name"
        fi
    done
else
    # Run specific example
    run_example "$1"
fi

echo -e "\n${GREEN}✓ Example projects completed!${NC}"