#!/bin/bash
# Quick diagnostic wrapper to help find your chats
# Usage: ./diagnose.sh

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate venv
if [ -d "venv" ] && [ -z "$VIRTUAL_ENV" ]; then
    source venv/bin/activate
fi

# Check if .env file exists
if [ -f .env ]; then
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
fi

# Check for API key
if [ -z "$ABACUS_API_KEY" ]; then
    echo "🔑 Abacus.AI API key not found in environment or .env file"
    echo ""
    read -p "Enter your Abacus.AI API key: " ABACUS_API_KEY
    
    if [ -z "$ABACUS_API_KEY" ]; then
        echo "❌ Error: API key cannot be empty"
        exit 1
    fi
    
    export ABACUS_API_KEY
    echo ""
fi

echo "🔍 Running Abacus.AI Chat Discovery..."
echo "=" * 60
echo ""

# Run discovery
python discover_chats.py

echo ""
echo "=" * 60
echo "💡 Additional Diagnostics"
echo "=" * 60
echo ""
echo "Would you like to explore available API methods? (y/n)"
read -p "> " response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo ""
    python explore_api.py
fi

echo ""
echo "=" * 60
echo "📚 Next Steps"
echo "=" * 60
echo ""
echo "1. Check the output above for any found chats/deployments"
echo "2. Read FINDING_CHATS.md for detailed troubleshooting"
echo "3. Visit https://abacus.ai to verify chats exist in the web UI"
echo "4. If you found chats, run: ./export_all.sh"
echo ""
