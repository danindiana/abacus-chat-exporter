#!/bin/bash
# PDF Processing Wrapper Script
# Activates venv, checks API key, runs PDF processor
# Usage: ./scripts/pdf/process_pdfs.sh

set -e

# Get the project root directory (two levels up from this script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"
cd "$PROJECT_ROOT"

echo "=================================================="
echo "🚀 Abacus.AI PDF Batch Processor"
echo "=================================================="
echo

# Activate virtual environment
if [ -d "venv" ]; then
    echo "🐍 Activating Python virtual environment..."
    source venv/bin/activate
else
    echo "❌ Error: venv not found in project root"
    echo "   Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Check for .env file
if [ -f ".env" ]; then
    echo "📝 Loading environment from .env..."
    source .env
fi

# Check/prompt for API key
if [ -z "$ABACUS_API_KEY" ]; then
    echo "🔑 API Key not found in environment"
    read -p "Enter your Abacus.AI API Key: " api_key
    export ABACUS_API_KEY="$api_key"
    echo
fi

# Test API connection
echo "🔌 Testing API connection..."
python3 -c "
from abacusai import ApiClient
import sys
try:
    client = ApiClient('$ABACUS_API_KEY')
    projects = client.list_projects()
    print(f'✅ Connected! Found {len(projects)} projects')
except Exception as e:
    print(f'❌ API Connection failed: {e}')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Failed to connect to Abacus.AI API"
    exit 1
fi

echo
echo "=================================================="
echo

# Run the PDF processor
python3 scripts/pdf/process_pdfs.py

echo
echo "=================================================="
echo "✅ Processing session complete!"
echo "=================================================="
