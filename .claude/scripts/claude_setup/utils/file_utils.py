"""File and directory utilities for Claude Code setup tools."""

import os
import json
import shutil
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Union, Any


def ensure_directory(path: Union[str, Path]) -> Path:
    """Create directory if it doesn't exist and return Path object."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_json(filepath: Union[str, Path]) -> Dict[str, Any]:
    """Read and parse a JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(filepath: Union[str, Path], data: Dict[str, Any], indent: int = 2) -> None:
    """Write data to a JSON file with pretty formatting."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def backup_file(filepath: Union[str, Path], backup_dir: Optional[Union[str, Path]] = None) -> Optional[Path]:
    """Create a backup of a file before modifying it."""
    filepath = Path(filepath)
    if not filepath.exists():
        return None
    
    if backup_dir is None:
        backup_dir = filepath.parent / '.backups'
    
    backup_dir = ensure_directory(backup_dir)
    timestamp = os.path.getmtime(filepath)
    backup_name = f"{filepath.name}.{int(timestamp)}.bak"
    backup_path = backup_dir / backup_name
    
    shutil.copy2(filepath, backup_path)
    return backup_path


def find_files(pattern: str, root_dir: Union[str, Path] = '.', 
               ignore_dirs: Optional[List[str]] = None) -> List[Path]:
    """Find files matching a pattern, ignoring specified directories."""
    root_dir = Path(root_dir)
    if ignore_dirs is None:
        ignore_dirs = ['.git', 'node_modules', '__pycache__', 'venv', '.venv']
    
    matches = []
    for path in root_dir.rglob(pattern):
        # Check if any parent directory should be ignored
        if any(ignored in path.parts for ignored in ignore_dirs):
            continue
        if path.is_file():
            matches.append(path)
    
    return sorted(matches)


def safe_write(filepath: Union[str, Path], content: str, backup: bool = True) -> None:
    """Safely write content to a file with optional backup."""
    filepath = Path(filepath)
    
    # Create backup if requested and file exists
    if backup and filepath.exists():
        backup_file(filepath)
    
    # Write to temporary file first
    temp_fd, temp_path = tempfile.mkstemp(dir=filepath.parent)
    try:
        with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Move temporary file to final location
        shutil.move(temp_path, str(filepath))
    except Exception:
        # Clean up temporary file on error
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise


def copy_with_template(src: Union[str, Path], dst: Union[str, Path], 
                      replacements: Optional[Dict[str, str]] = None) -> None:
    """Copy a file while performing template replacements."""
    with open(src, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if replacements:
        for key, value in replacements.items():
            content = content.replace(f"{{{key}}}", value)
    
    safe_write(dst, content, backup=False)


def get_project_root() -> Path:
    """Find the project root directory (containing .git or .claude)."""
    current = Path.cwd()
    
    # Look for .git or .claude directory
    for parent in [current] + list(current.parents):
        if (parent / '.git').exists() or (parent / '.claude').exists():
            return parent
    
    # Default to current directory
    return current


def make_executable(filepath: Union[str, Path]) -> None:
    """Make a file executable (Unix-like systems only)."""
    filepath = Path(filepath)
    if os.name != 'nt':  # Not Windows
        current_mode = filepath.stat().st_mode
        filepath.chmod(current_mode | 0o111)  # Add execute permission


def relative_to_cwd(path: Union[str, Path]) -> str:
    """Get a path relative to the current working directory."""
    try:
        return str(Path(path).relative_to(Path.cwd()))
    except ValueError:
        return str(path)