#!/bin/bash
# Activate the virtual environment
# Usage: source activate.sh

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -d "$SCRIPT_DIR/venv" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
    echo "✅ Virtual environment activated"
    echo "Python: $(which python)"
    echo "Version: $(python --version)"
else
    echo "❌ Virtual environment not found at $SCRIPT_DIR/venv"
    echo "Run: python3 -m venv venv && pip install -r requirements.txt"
    exit 1
fi
