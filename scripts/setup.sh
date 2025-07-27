#!/bin/bash
# Quick setup script for Claude Code template

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Setting up Claude Code template...${NC}"

# Create required directories
echo "Creating directories..."
mkdir -p .claude/state worktrees/{} tests/integration

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r .claude/scripts/requirements.txt

# Setup git worktree
echo "Configuring git worktree..."
git config --local core.worktree "$PWD/worktrees"

# Create example project directories
echo "Creating example project directories..."
for example in rust-go-microservices python-ml-typescript-api cpp-java-python-engine; do
    mkdir -p "examples/$example"/{specs,tests}
done

# Run template validation
echo -e "\n${YELLOW}Running template validation...${NC}"
./.claude/scripts/inventory-check.sh

echo -e "\n${GREEN}✓ Claude Code template setup complete!${NC}"
echo "Next steps:"
echo "1. Create a ROADMAP.md file in specs/"
echo "2. Use /phase-breakdown to start development"
echo "3. Check examples/ for multi-language project templates"