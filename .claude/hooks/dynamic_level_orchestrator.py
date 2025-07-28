#!/usr/bin/env python3
"""
Orchestrates dynamic level progression for the recursive code renovation branch.
Determines which depth level to process next.
"""
import json
import os
from datetime import datetime

class DynamicLevelOrchestrator:
    """Orchestrates dynamic level progression for a given branch."""

    def __init__(self, branch_num: int):
        self.branch = branch_num
        self.state_dir = '.claude/state'
        self.worktree_plan_file = f'{self.state_dir}/worktree-plan-b{self.branch}.json'

    def load_worktree_plan(self) -> dict | None:
        """Loads the worktree plan for the current branch."""
        if not os.path.exists(self.worktree_plan_file):
            return None
        with open(self.worktree_plan_file, 'r') as f:
            return json.load(f)

    def is_level_complete(self, level: int) -> bool:
        """Checks if a level's completion marker exists."""
        completion_file = f'{self.state_dir}/level-complete-b{self.branch}l{level}.json'
        return os.path.exists(completion_file)

    def determine_next_action(self) -> dict:
        """Determines the next action for the recursive branch."""
        plan = self.load_worktree_plan()
        if not plan:
            return {
                "agent": "recursive-code-analyzer",
                "message": f"No worktree plan found for Branch {self.branch}. Please run recursive analysis."
            }

        max_depth = max(int(k) for k in plan['levels'].keys())

        for level in range(max_depth + 1):
            if not self.is_level_complete(level):
                nodes_at_level = plan['levels'][str(level)]
                nodes_needing_work = [
                    n for n in nodes_at_level if not n['is_leaf'] or n['needs_renovation']
                ]
                if not nodes_needing_work:
                    # If no nodes need work, mark level as complete and re-evaluate
                    self.mark_level_complete(level)
                    return self.determine_next_action()

                return {
                    "agent": "generic-code-architect",
                    "message": f"Process Branch {self.branch}, Level {level}. Nodes to process: {len(nodes_needing_work)}."
                }
        
        return {
            "agent": "recursive-implementation-assembler",
            "message": f"All levels in Branch {self.branch} are complete. Begin assembly."
        }

    def mark_level_complete(self, level: int):
        """Creates a completion marker for a level."""
        completion_file = f'{self.state_dir}/level-complete-b{self.branch}l{level}.json'
        with open(completion_file, 'w') as f:
            json.dump({
                "branch": self.branch,
                "level": level,
                "completed": True,
                "timestamp": datetime.now().isoformat()
            }, f)

def main():
    """Main execution logic for a specific branch."""
    # This hook would be called with the current code branch number.
    current_code_branch = 3 
    orchestrator = DynamicLevelOrchestrator(current_code_branch)
    next_action = orchestrator.determine_next_action()
    
    print(f"--- Dynamic Orchestrator (Branch {current_code_branch}) Decision ---")
    print(f"Next Agent to Invoke: {next_action['agent']}")
    print(f"Reason/Message: {next_action['message']}")

    command_for_claude = f"Task: Use the {next_action['agent']} sub agent to {next_action['message']}"
    print("\n--- Command for Meta-Agent ---")
    print(command_for_claude)

if __name__ == '__main__':
    main()
