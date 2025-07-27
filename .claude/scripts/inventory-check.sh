#!/bin/bash
# Wrapper script for Python implementation of inventory-check

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    echo "Please install Python 3.8 or later."
    exit 1
fi

# Check if required packages are installed
if ! python3 -c "import click, rich" 2>/dev/null; then
    echo "Installing required Python packages..."
    pip3 install -r "$SCRIPT_DIR/requirements.txt" || {
        echo "Error: Failed to install required packages."
        echo "Please run: pip3 install -r $SCRIPT_DIR/requirements.txt"
        exit 1
    }
fi

# Run the Python implementation
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
python3 -m claude_setup.inventory_check "$@"