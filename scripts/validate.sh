#!/bin/bash
# Validate Claude Code template setup and functionality

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Validating Claude Code template setup...${NC}"

# Check required directories
echo "Checking directories..."
required_dirs=(
    ".claude/agents"
    ".claude/commands"
    ".claude/hooks"
    ".claude/scripts"
    ".claude/state"
    "docs/api"
    "docs/architecture"
    "docs/guides"
    "docs/migration"
    "docs/services"
    "examples"
    "specs"
    "tests/integration"
    "worktrees"
)

for dir in "${required_dirs[@]}"; do
    if [ ! -d "$dir" ]; then
        echo -e "${RED}✗ Missing directory: $dir${NC}"
        exit 1
    fi
done

# Check required files
echo "Checking files..."
required_files=(
    ".claude/config.json"
    ".claude/commands/phase-breakdown.md"
    "README.md"
    "CHANGELOG.md"
    "Makefile"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}✗ Missing file: $file${NC}"
        exit 1
    fi
done

# Check Python setup
echo "Checking Python setup..."
if ! python3 -c "import click, rich, yaml" 2>/dev/null; then
    echo -e "${RED}✗ Missing Python dependencies${NC}"
    echo "Run: pip install -r .claude/scripts/requirements.txt"
    exit 1
fi

# Run integration tests
echo -e "\n${YELLOW}Running integration tests...${NC}"
python3 tests/integration/test_language_detection.py

# Run inventory check
echo -e "\n${YELLOW}Running inventory check...${NC}"
./.claude/scripts/inventory-check.sh

# Check example projects
echo -e "\n${YELLOW}Checking example projects...${NC}"
for example in examples/*/; do
    if [ -d "$example" ]; then
        name=$(basename "$example")
        echo "Checking $name..."
        
        if [ ! -f "$example/README.md" ] || [ ! -f "$example/specs/ROADMAP.md" ]; then
            echo -e "${RED}✗ Missing files in $name${NC}"
            exit 1
        fi
    fi
done

echo -e "\n${GREEN}✓ All validation checks passed!${NC}"