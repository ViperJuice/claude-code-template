#!/usr/bin/env python3
"""
Orchestrates the high-level renovation workflow based on treesitter-chunker analysis.
Determines which major branch (Containers, Components, Code) to work on.
"""
import json
import os
from datetime import datetime

class ChunkBasedOrchestrator:
    """Orchestrates renovation based on chunk analysis."""

    def __init__(self):
        self.state_dir = '.claude/state'
        self.state_file = f'{self.state_dir}/orchestration-state.json'

    def load_cartography(self) -> dict | None:
        """Loads the chunk analysis from the cartographer."""
        cartography_file = f'{self.state_dir}/codebase-cartography.json'
        if not os.path.exists(cartography_file):
            return None
        with open(cartography_file, 'r') as f:
            return json.load(f)

    def get_current_state(self) -> dict:
        """Gets the current orchestration state."""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {"completed_branches": []}

    def save_state(self, state: dict):
        """Saves the orchestration state."""
        os.makedirs(self.state_dir, exist_ok=True)
        state['last_update'] = datetime.now().isoformat()
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def is_branch_complete(self, branch_num: int) -> bool:
        """Checks if a branch's summary report exists."""
        summary_file = f".claude/reports/branch-{branch_num}-summary.md"
        return os.path.exists(summary_file)

    def determine_next_action(self) -> dict:
        """Determines the next agent and task to execute."""
        state = self.get_current_state()
        cartography = self.load_cartography()

        if not cartography:
            return {
                "agent": "codebase-cartographer",
                "message": "No cartography found. Please analyze the codebase first."
            }

        # Define the sequence of branches
        branches = [
            {"num": 0, "name": "Container", "agent": "renovation-architect-b0l0"},
            {"num": 1, "name": "Component", "agent": "renovation-architect-b1l0"},
            {"num": 2, "name": "Class", "agent": "renovation-architect-b2l0"},
            {"num": 3, "name": "Code", "agent": "recursive-code-analyzer"},
        ]

        for branch in branches:
            if not self.is_branch_complete(branch["num"]):
                return {
                    "agent": branch["agent"],
                    "message": f"Begin Branch {branch['num']} ({branch['name']} renovation)."
                }
        
        return {
            "agent": "recursive-implementation-assembler",
            "message": "All branches are complete. Begin final assembly of the renovated codebase."
        }

def main():
    """Main execution logic."""
    orchestrator = ChunkBasedOrchestrator()
    next_action = orchestrator.determine_next_action()

    print("--- Orchestrator Decision ---")
    print(f"Next Agent to Invoke: {next_action['agent']}")
    print(f"Reason/Message: {next_action['message']}")
    
    # This command would be used by the meta-agent (e.g., Claude Code)
    command_for_claude = f"Task: Use the {next_action['agent']} sub agent to {next_action['message']}"
    print("\n--- Command for Meta-Agent ---")
    print(command_for_claude)

if __name__ == '__main__':
    main()
