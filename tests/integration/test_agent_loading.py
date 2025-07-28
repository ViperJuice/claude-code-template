#!/usr/bin/env python3
"""Integration tests for agent loading and validation"""

import os
import sys
import yaml
from pathlib import Path

def validate_agent_file(agent_path):
    """Validate a single agent file"""
    with open(agent_path, 'r') as f:
        content = f.read()
    
    # Check for YAML frontmatter
    if not content.startswith('---\n'):
        raise ValueError(f"{agent_path}: Missing YAML frontmatter")
    
    # Extract frontmatter
    parts = content.split('---\n', 2)
    if len(parts) < 3:
        raise ValueError(f"{agent_path}: Invalid frontmatter format")
    
    # Parse YAML
    try:
        metadata = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        raise ValueError(f"{agent_path}: Invalid YAML: {e}")
    
    # Validate required fields
    required_fields = ['name', 'description', 'tools']
    for field in required_fields:
        if field not in metadata:
            raise ValueError(f"{agent_path}: Missing required field '{field}'")
    
    # Validate tools is a list
    if not isinstance(metadata['tools'], list):
        raise ValueError(f"{agent_path}: 'tools' must be a list")
    
    return metadata

def test_all_agents():
    """Test all agent files in the agents directory"""
    agents_dir = Path(__file__).parent.parent.parent / '.claude' / 'agents'
    
    if not agents_dir.exists():
        raise FileNotFoundError(f"Agents directory not found: {agents_dir}")
    
    agent_files = list(agents_dir.glob('*.md'))
    if not agent_files:
        raise ValueError("No agent files found")
    
    print(f"Found {len(agent_files)} agent files")
    
    agents = {}
    for agent_file in agent_files:
        if agent_file.name in ['.gitkeep', 'README.md']:
            continue
            
        print(f"Validating {agent_file.name}...")
        try:
            metadata = validate_agent_file(agent_file)
            agents[metadata['name']] = metadata
            print(f"  ✓ {metadata['name']}: {metadata['description'][:60]}...")
        except Exception as e:
            print(f"  ✗ Failed: {e}")
            raise
    
    return agents

def test_agent_dependencies():
    """Test that agent tool dependencies are valid"""
    agents = test_all_agents()
    
    valid_tools = {
        'Read', 'Write', 'MultiEdit', 'Edit', 'Bash', 'Task', 
        'Glob', 'Grep', 'TodoWrite', 'WebSearch', 'WebFetch'
    }
    
    print("\nValidating agent tool dependencies...")
    for name, agent in agents.items():
        invalid_tools = set(agent['tools']) - valid_tools
        if invalid_tools:
            raise ValueError(f"{name} uses invalid tools: {invalid_tools}")
        print(f"  ✓ {name}: {len(agent['tools'])} tools")

def test_agent_roles():
    """Test that all expected agent roles are present"""
    agents = test_all_agents()
    
    # Core orchestration agents
    core_agents = {
        'phase-architect', 'interface-designer', 'interface-verifier',
        'worktree-manager', 'worktree-lead', 'integration-guardian', 
        'doc-scribe', 'pattern-advisor', 'anti-pattern-detector'
    }
    
    # Language-specific test builders
    test_builder_agents = {
        'test-builder-systems', 'test-builder-web', 'test-builder-scripting',
        'test-builder-jvm', 'test-builder-functional', 'test-builder-mobile',
        'test-builder-data', 'test-builder-assembly'
    }
    
    # Language-specific coders
    coder_agents = {
        'coder-systems', 'coder-web', 'coder-scripting',
        'coder-jvm', 'coder-functional', 'coder-mobile',
        'coder-data', 'coder-assembly'
    }
    
    all_expected = core_agents | test_builder_agents | coder_agents
    
    print("\nChecking for required agents...")
    missing_agents = all_expected - set(agents.keys())
    if missing_agents:
        raise ValueError(f"Missing required agents: {missing_agents}")
    
    print(f"  ✓ All {len(all_expected)} required agents present")

def test_phase_command():
    """Test that phase breakdown command exists"""
    command_path = Path(__file__).parent.parent.parent / '.claude' / 'commands' / 'phase-breakdown.md'
    
    print("\nValidating phase breakdown command...")
    if not command_path.exists():
        raise FileNotFoundError(f"Phase breakdown command not found: {command_path}")
    
    with open(command_path, 'r') as f:
        content = f.read()
    
    # Check for proper format
    if not content.startswith('---\n'):
        raise ValueError("Phase breakdown command missing frontmatter")
    
    # Parse frontmatter
    parts = content.split('---\n', 2)
    metadata = yaml.safe_load(parts[1])
    
    required_fields = ['allowed-tools', 'description', 'argument-hint']
    for field in required_fields:
        if field not in metadata:
            raise ValueError(f"Phase command missing field: {field}")
    
    print("  ✓ Phase breakdown command valid")

if __name__ == "__main__":
    print("Running agent loading integration tests...")
    
    try:
        test_all_agents()
        test_agent_dependencies()
        test_agent_roles()
        test_phase_command()
        print("\n✅ All agent tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)