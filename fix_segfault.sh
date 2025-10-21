#!/bin/bash
# Recreate virtual environment with a more stable Python version
# This fixes segmentation fault issues with Python 3.13

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "🔧 Fixing segmentation fault by recreating venv with Python 3.11..."
echo ""

# Remove existing venv
if [ -d "venv" ]; then
    echo "Removing existing Python 3.13 venv..."
    rm -rf venv
fi

# Check for Python 3.11
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
    echo "✓ Found Python 3.11"
elif command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
    echo "✓ Found Python 3.12"
elif command -v python3.10 &> /dev/null; then
    PYTHON_CMD="python3.10"
    echo "✓ Found Python 3.10"
else
    echo "❌ Error: No compatible Python version found (3.10, 3.11, or 3.12)"
    echo "Python 3.13 has compatibility issues with some C-extension libraries."
    exit 1
fi

# Create new venv
echo "Creating new virtual environment with $PYTHON_CMD..."
$PYTHON_CMD -m venv venv

# Activate and install
echo "Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt

echo ""
echo "✅ Virtual environment recreated successfully!"
$PYTHON_CMD --version
echo ""
echo "You can now run: ./export_all.sh"
