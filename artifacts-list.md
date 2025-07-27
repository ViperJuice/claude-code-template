# Complete Artifacts List - Claude Code Multi-Language Template

## 📁 Sub-Agents (`.claude/agents/`)

1. **phase-architect.md** - From "Phase Architect Sub-Agent" artifact
2. **interface-designer.md** - From "interface-designer.md" artifact (newly created)
3. **interface-verifier.md** - From "Multi-Language Interface Verifier Sub-Agent" artifact
4. **worktree-manager.md** - From "worktree-manager.md" artifact (newly created)
5. **worktree-lead.md** - From "Worktree Lead Sub-Agent" artifact
6. **test-builder.md** - From "Multi-Language Test Builder Sub-Agent" artifact
7. **coder.md** - From "Multi-Language Coder Sub-Agent" artifact
8. **integration-guardian.md** - From "integration-guardian.md" artifact (newly created)
9. **doc-scribe.md** - From "doc-scribe.md" artifact (newly created)

## 📝 Commands (`.claude/commands/`)

1. **phase-breakdown.md** - From "Refactored Phase-Breakdown Command" artifact

## 🔧 Scripts

1. **setup-native-subagents.sh** - From "setup-native-subagents.sh" artifact
2. **detect-language.sh** - From "Language Detection Script" artifact
3. **inventory-check.sh** - From "Project Inventory Check Script" artifact (optional)
4. **cleanup-legacy.sh** - From "Legacy Files Cleanup Script" artifact (optional)

## ⚙️ Configuration

1. **.claude/config.json** - From ".claude/config.json" artifact
2. **.claude/.gitignore** - From ".claude/.gitignore" artifact
3. **Makefile** - From "Master Makefile for Multi-Language Project" artifact

## 🚀 CI/CD & DevOps

1. **.github/workflows/multi-language-ci.yml** - From "GitHub Actions Multi-Language CI/CD" artifact
2. **docker-compose.yml** - From "Docker Compose Multi-Language Development" artifact

## 📚 Documentation

1. **README.md** - Basic version created in setup script (customize as needed)
2. **CHANGELOG.md** - Basic version created in setup script
3. **Implementation Guide** - From "Multi-Language Claude Code Implementation Guide" artifact

## 📋 Reference Documents (Keep in Claude Project)

These are reference documents to keep in your Claude project but don't need to be saved to the repo:
- "Final Project Structure with Native Sub-Agents"
- "Multi-Language Claude Code Agents - Summary"
- "Claude Code Multi-Language Support Matrix"
- "Example: Complete Phase Execution Flow"
- "Multi-Language Phase Execution Example"

## 🗂️ Directory Structure to Create

```
your-project/
├── .claude/
│   ├── agents/
│   │   └── (9 sub-agent .md files)
│   ├── commands/
│   │   └── phase-breakdown.md
│   ├── scripts/
│   │   ├── setup-native-subagents.sh
│   │   └── detect-language.sh
│   ├── state/
│   │   └── .gitkeep
│   ├── config.json
│   └── .gitignore
├── .github/
│   └── workflows/
│       └── multi-language-ci.yml
├── docs/
│   ├── api/
│   ├── architecture/
│   └── implementation-guide.md
├── worktrees/
│   └── .gitkeep
├── docker-compose.yml
├── Makefile
├── README.md
└── CHANGELOG.md
```

## ✅ Setup Instructions

1. Create the directory structure above
2. Copy each artifact content to its corresponding file
3. Make scripts executable:
   ```bash
   chmod +x .claude/scripts/*.sh
   chmod +x *.sh
   ```
4. Run the setup script:
   ```bash
   ./setup-native-subagents.sh
   ```
5. Create your ROADMAP.md with phase definitions
6. Start using:
   ```bash
   claude
   /phase-breakdown 1
   ```

## 💡 Notes

- The setup script creates placeholder files - you need to copy the actual content from the artifacts
- All sub-agents are now individual files (we split the bundled ones)
- The system supports 25+ programming languages out of the box
- Customize `.claude/config.json` for your specific language preferences