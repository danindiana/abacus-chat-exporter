#!/bin/bash
# Activate the virtual environment
# Usage: source scripts/utils/activate.sh (from project root)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"

if [ -d "$PROJECT_ROOT/venv" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
    echo "✅ Virtual environment activated"
    echo "Python: $(which python)"
    echo "Version: $(python --version)"
else
    echo "❌ Virtual environment not found at $PROJECT_ROOT/venv"
    echo "Run from project root: python3 -m venv venv && pip install -r requirements.txt"
    exit 1
fi
