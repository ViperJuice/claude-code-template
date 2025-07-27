#!/bin/bash
# Integration test for the complete workflow

set -e

echo "Running workflow integration tests..."

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test directory
TEST_DIR=$(mktemp -d)
echo "Test directory: $TEST_DIR"

# Cleanup on exit
trap "rm -rf $TEST_DIR" EXIT

# Copy template to test directory
cp -r .claude $TEST_DIR/
cp -r specs $TEST_DIR/
mkdir -p $TEST_DIR/worktrees

# Test 1: Inventory check
echo -e "\n${GREEN}Test 1: Inventory Check${NC}"
cd $TEST_DIR
if $OLDPWD/.claude/scripts/inventory-check.sh > /dev/null 2>&1; then
    echo "✓ Inventory check passed"
else
    echo -e "${RED}✗ Inventory check failed${NC}"
    exit 1
fi

# Test 2: Language detection
echo -e "\n${GREEN}Test 2: Language Detection${NC}"
mkdir -p $TEST_DIR/test-service
echo 'package main' > $TEST_DIR/test-service/main.go
echo 'module test' > $TEST_DIR/test-service/go.mod

if $OLDPWD/.claude/scripts/detect-language.sh | grep -q "go"; then
    echo "✓ Language detection passed"
else
    echo -e "${RED}✗ Language detection failed${NC}"
    exit 1
fi

# Test 3: Python module imports
echo -e "\n${GREEN}Test 3: Python Module Imports${NC}"
cd $OLDPWD
if python3 -c "from claude_setup import config, detect_language, inventory_check" 2>/dev/null; then
    echo "✓ Python modules import correctly"
else
    echo -e "${RED}✗ Python module import failed${NC}"
    exit 1
fi

# Test 4: Agent validation
echo -e "\n${GREEN}Test 4: Agent Validation${NC}"
if python3 tests/integration/test_agent_loading.py > /dev/null 2>&1; then
    echo "✓ Agent validation passed"
else
    echo -e "${RED}✗ Agent validation failed${NC}"
    exit 1
fi

# Test 5: Example project structure
echo -e "\n${GREEN}Test 5: Example Projects${NC}"
for example in examples/*/; do
    if [ -d "$example" ]; then
        if [ -f "$example/README.md" ] && [ -f "$example/specs/ROADMAP.md" ]; then
            echo "✓ $(basename $example) structure valid"
        else
            echo -e "${RED}✗ $(basename $example) missing files${NC}"
            exit 1
        fi
    fi
done

# Test 6: Documentation structure
echo -e "\n${GREEN}Test 6: Documentation Structure${NC}"
required_docs=(
    "docs/api/README.md"
    "docs/architecture/README.md"
    "docs/guides/getting-started.md"
    "docs/migration/from-legacy.md"
    "docs/services/README.md"
)

for doc in "${required_docs[@]}"; do
    if [ -f "$doc" ]; then
        echo "✓ $doc exists"
    else
        echo -e "${RED}✗ $doc missing${NC}"
        exit 1
    fi
done

echo -e "\n${GREEN}✅ All workflow tests passed!${NC}"