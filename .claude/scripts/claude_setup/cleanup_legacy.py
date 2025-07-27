#!/usr/bin/env python3
"""Remove legacy orchestration files from Claude Code projects."""

import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import click
from rich.console import Console
from rich.prompt import Confirm
from rich.table import Table

from .utils.colors import Colors, success, error, warning, info
from .utils.file_utils import get_project_root, ensure_directory


# Legacy patterns to remove
LEGACY_PATTERNS = [
    '.claude/**/*.py',  # Old Python orchestration files
    '.claude/orchestration',
    '.claude/agents/state/*.py',
    '.claude/phase-manager*',
    '.claude/agent-mesh*',
    '.claude/**/*orchestrat*',
    '.claude/playbooks/*.yaml',
    '.claude/contracts',
    '.claude/agents/*.yaml',
    '.claude/agents/*.yml',
    '.claude/agents/*.json',
]

# Patterns to always keep
KEEP_PATTERNS = [
    '**/claude_setup/**',  # Our new Python scripts
    '.claude/config.json',
    '.claude/.gitignore',
    '.claude/state/*.json',
    '**/__pycache__/**',
]


class LegacyCleaner:
    """Clean up legacy Claude Code files."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize the legacy cleaner."""
        self.project_root = project_root or get_project_root()
        self.console = Console()
        self.found_files: List[Path] = []
    
    def should_keep(self, filepath: Path) -> bool:
        """Check if a file should be kept."""
        str_path = str(filepath)
        
        # Check keep patterns
        for pattern in KEEP_PATTERNS:
            if '*' in pattern:
                # Simple wildcard matching
                pattern_parts = pattern.split('**')
                if all(part.strip('/') in str_path for part in pattern_parts if part):
                    return True
            elif pattern in str_path:
                return True
        
        # Special case: keep our new Python implementation
        if 'claude_setup' in str_path:
            return True
        
        return False
    
    def find_legacy_files(self) -> List[Path]:
        """Find all legacy files matching the patterns."""
        legacy_files = []
        
        for pattern in LEGACY_PATTERNS:
            try:
                for path in self.project_root.glob(pattern):
                    if path.is_file() and not self.should_keep(path):
                        legacy_files.append(path)
            except Exception:
                # Some glob patterns might fail, that's okay
                pass
        
        # Remove duplicates and sort
        legacy_files = sorted(set(legacy_files))
        self.found_files = legacy_files
        return legacy_files
    
    def backup_files(self, files: List[Path]) -> Optional[Path]:
        """Create a backup of files before deletion."""
        if not files:
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = self.project_root / '.claude' / 'backups' / f'legacy_backup_{timestamp}'
        ensure_directory(backup_dir)
        
        for filepath in files:
            try:
                # Maintain directory structure in backup
                rel_path = filepath.relative_to(self.project_root)
                backup_path = backup_dir / rel_path
                ensure_directory(backup_path.parent)
                shutil.copy2(filepath, backup_path)
            except Exception as e:
                self.console.print(warning(f"Failed to backup {filepath}: {e}"))
        
        return backup_dir
    
    def delete_files(self, files: List[Path]) -> int:
        """Delete the specified files."""
        deleted = 0
        
        for filepath in files:
            try:
                filepath.unlink()
                deleted += 1
            except Exception as e:
                self.console.print(error(f"Failed to delete {filepath}: {e}"))
        
        return deleted
    
    def cleanup_empty_dirs(self) -> int:
        """Remove empty directories left after file deletion."""
        removed = 0
        
        # Start from deepest directories
        for dirpath in sorted(self.project_root.rglob('*'), reverse=True):
            if dirpath.is_dir() and not any(dirpath.iterdir()):
                try:
                    dirpath.rmdir()
                    removed += 1
                except Exception:
                    pass  # Directory might not be empty or have permissions issues
        
        return removed
    
    def display_files(self, files: List[Path]) -> None:
        """Display found files in a table."""
        if not files:
            self.console.print(success("No legacy files found!"))
            self.console.print("Your project is using the native sub-agent approach.")
            return
        
        table = Table(title=f"Found {len(files)} Legacy Files")
        table.add_column("File", style="yellow")
        table.add_column("Size", style="cyan")
        
        total_size = 0
        for filepath in files[:20]:  # Show first 20
            try:
                size = filepath.stat().st_size
                total_size += size
                rel_path = filepath.relative_to(self.project_root)
                table.add_row(str(rel_path), f"{size:,} bytes")
            except Exception:
                pass
        
        if len(files) > 20:
            table.add_row(f"... and {len(files) - 20} more", "")
        
        self.console.print(table)
        self.console.print(f"\nTotal size: {total_size:,} bytes")
    
    def generate_undo_script(self, backup_dir: Path) -> Path:
        """Generate a script to restore backed up files."""
        undo_script = backup_dir / 'restore.py'
        
        script_content = f'''#!/usr/bin/env python3
"""Restore files from legacy cleanup backup."""

import shutil
from pathlib import Path

backup_dir = Path(__file__).parent
project_root = Path("{self.project_root}")

print("Restoring files from backup...")
restored = 0

for backup_file in backup_dir.rglob("*"):
    if backup_file.is_file() and backup_file.name != "restore.py":
        rel_path = backup_file.relative_to(backup_dir)
        restore_path = project_root / rel_path
        
        try:
            restore_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup_file, restore_path)
            restored += 1
            print(f"  Restored: {{rel_path}}")
        except Exception as e:
            print(f"  Failed to restore {{rel_path}}: {{e}}")

print(f"\\nRestored {{restored}} files")
'''
        
        undo_script.write_text(script_content)
        undo_script.chmod(0o755)
        return undo_script


@click.command()
@click.option('--force', is_flag=True, help='Skip confirmation prompts')
@click.option('--dry-run', is_flag=True, help='Show what would be deleted without deleting')
@click.option('--backup/--no-backup', default=True, help='Create backup before deletion')
@click.option('--pattern', '-p', multiple=True, help='Additional patterns to clean')
def main(force: bool, dry_run: bool, backup: bool, pattern: List[str]) -> None:
    """Remove legacy orchestration files from Claude Code projects."""
    cleaner = LegacyCleaner()
    
    # Add any custom patterns
    if pattern:
        LEGACY_PATTERNS.extend(pattern)
    
    cleaner.console.print("🧹 Claude Code Legacy Files Cleanup")
    cleaner.console.print("=" * 50)
    
    if dry_run:
        cleaner.console.print(warning("Running in DRY RUN mode - no files will be deleted"))
    else:
        cleaner.console.print(warning("Running in FORCE mode - files will be deleted!") if force else "")
    
    # Find legacy files
    cleaner.console.print("\n🔍 Searching for legacy files...")
    legacy_files = cleaner.find_legacy_files()
    
    if not legacy_files:
        cleaner.console.print(success("No legacy files found!"))
        cleaner.console.print("Your project is clean and using the native sub-agent approach.")
        return
    
    # Display found files
    cleaner.display_files(legacy_files)
    
    if dry_run:
        cleaner.console.print(f"\n{Colors.YELLOW}To delete these files, run without --dry-run{Colors.RESET}")
        return
    
    # Confirm deletion
    if not force:
        if not Confirm.ask(f"\n[red]Delete {len(legacy_files)} files?[/red]"):
            cleaner.console.print("Cleanup cancelled.")
            return
    
    # Create backup if requested
    backup_dir = None
    if backup:
        cleaner.console.print("\n📦 Creating backup...")
        backup_dir = cleaner.backup_files(legacy_files)
        if backup_dir:
            cleaner.console.print(success(f"Backup created: {backup_dir}"))
    
    # Delete files
    cleaner.console.print("\n🗑️  Deleting legacy files...")
    deleted = cleaner.delete_files(legacy_files)
    cleaner.console.print(success(f"Deleted {deleted} files"))
    
    # Cleanup empty directories
    cleaner.console.print("\n🧹 Cleaning up empty directories...")
    removed_dirs = cleaner.cleanup_empty_dirs()
    if removed_dirs:
        cleaner.console.print(success(f"Removed {removed_dirs} empty directories"))
    
    # Create undo script if backup was made
    if backup_dir:
        undo_script = cleaner.generate_undo_script(backup_dir)
        cleaner.console.print(f"\n💡 To undo this cleanup, run:")
        cleaner.console.print(f"   python {undo_script}")
    
    cleaner.console.print(f"\n{Colors.GREEN}✓ Cleanup complete!{Colors.RESET}")
    cleaner.console.print("\n💡 Next steps:")
    cleaner.console.print("1. Run './inventory-check.sh' to see current state")
    cleaner.console.print("2. Run './.claude/scripts/setup-native-subagents.sh' to set up native agents")
    cleaner.console.print("3. Start using with: claude -> /phase-breakdown 1")


if __name__ == '__main__':
    main()