"""Terminal color utilities for Claude Code setup tools."""

import os
import sys
from typing import Optional


class Colors:
    """ANSI color codes for terminal output."""
    
    # Check if colors should be disabled
    NO_COLOR = os.environ.get('NO_COLOR') is not None
    IS_TERMINAL = sys.stdout.isatty()
    SUPPORTS_COLOR = IS_TERMINAL and not NO_COLOR
    
    # Color codes
    RESET = '\033[0m' if SUPPORTS_COLOR else ''
    BOLD = '\033[1m' if SUPPORTS_COLOR else ''
    DIM = '\033[2m' if SUPPORTS_COLOR else ''
    
    # Foreground colors
    BLACK = '\033[30m' if SUPPORTS_COLOR else ''
    RED = '\033[31m' if SUPPORTS_COLOR else ''
    GREEN = '\033[32m' if SUPPORTS_COLOR else ''
    YELLOW = '\033[33m' if SUPPORTS_COLOR else ''
    BLUE = '\033[34m' if SUPPORTS_COLOR else ''
    MAGENTA = '\033[35m' if SUPPORTS_COLOR else ''
    CYAN = '\033[36m' if SUPPORTS_COLOR else ''
    WHITE = '\033[37m' if SUPPORTS_COLOR else ''
    
    # Bright colors
    BRIGHT_RED = '\033[91m' if SUPPORTS_COLOR else ''
    BRIGHT_GREEN = '\033[92m' if SUPPORTS_COLOR else ''
    BRIGHT_YELLOW = '\033[93m' if SUPPORTS_COLOR else ''
    BRIGHT_BLUE = '\033[94m' if SUPPORTS_COLOR else ''
    
    # Symbols (with fallbacks for Windows)
    if os.name == 'nt':  # Windows
        CHECK = '[OK]'
        CROSS = '[X]'
        ARROW = '->'
        BULLET = '*'
    else:
        CHECK = '✓'
        CROSS = '✗'
        ARROW = '→'
        BULLET = '•'


def success(message: str) -> str:
    """Format a success message with green color."""
    return f"{Colors.GREEN}{Colors.CHECK} {message}{Colors.RESET}"


def error(message: str) -> str:
    """Format an error message with red color."""
    return f"{Colors.RED}{Colors.CROSS} {message}{Colors.RESET}"


def warning(message: str) -> str:
    """Format a warning message with yellow color."""
    return f"{Colors.YELLOW}⚠️  {message}{Colors.RESET}"


def info(message: str) -> str:
    """Format an info message with blue color."""
    return f"{Colors.BLUE}{Colors.BULLET} {message}{Colors.RESET}"


def header(message: str) -> str:
    """Format a header message with bold blue color."""
    return f"{Colors.BLUE}{Colors.BOLD}{message}{Colors.RESET}"


def dim(message: str) -> str:
    """Format a dimmed message."""
    return f"{Colors.DIM}{message}{Colors.RESET}"


def highlight(message: str, color: Optional[str] = None) -> str:
    """Highlight a message with the specified color."""
    if color is None:
        color = Colors.YELLOW
    return f"{color}{message}{Colors.RESET}"


def print_banner(title: str, subtitle: Optional[str] = None) -> None:
    """Print a formatted banner."""
    width = max(len(title), len(subtitle) if subtitle else 0) + 4
    
    print(f"\n{Colors.BLUE}{'=' * width}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{title.center(width)}{Colors.RESET}")
    if subtitle:
        print(f"{Colors.DIM}{subtitle.center(width)}{Colors.RESET}")
    print(f"{Colors.BLUE}{'=' * width}{Colors.RESET}\n")