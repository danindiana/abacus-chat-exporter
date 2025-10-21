#!/bin/bash
# Convenience script to export both AI Chat and Deployment conversations
# Usage: ./export_all.sh

set -e

# Activate virtual environment if it exists
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ -d "$SCRIPT_DIR/venv" ] && [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source "$SCRIPT_DIR/venv/bin/activate"
fi

# Check if .env file exists
if [ -f .env ]; then
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
fi

# Check for API key, prompt if not set
if [ -z "$ABACUS_API_KEY" ]; then
    echo "🔑 Abacus.AI API key not found in environment or .env file"
    echo ""
    read -p "Enter your Abacus.AI API key: " ABACUS_API_KEY
    
    if [ -z "$ABACUS_API_KEY" ]; then
        echo "❌ Error: API key cannot be empty"
        exit 1
    fi
    
    export ABACUS_API_KEY
    echo "✓ API key set for this session"
    echo ""
fi

echo "🚀 Starting Abacus.AI chat export..."
echo ""

# Test API connection first
echo "🔍 Testing API connection..."
if ! python -c "from abacusai import ApiClient; import os; client = ApiClient(os.environ['ABACUS_API_KEY']); print('✓ API client initialized successfully')" 2>/dev/null; then
    echo "❌ Error: Failed to initialize API client. Please check your API key."
    exit 1
fi
echo ""

# Export all deployment conversations (where your chats actually are!)
echo "📥 Exporting all deployment conversations..."
if python bulk_export_all_deployment_conversations.py; then
    echo "✓ Deployment conversations export completed"
else
    EXIT_CODE=$?
    echo "❌ Export failed with exit code: $EXIT_CODE"
    if [ $EXIT_CODE -eq 139 ]; then
        echo "⚠️  Segmentation fault detected. This may be a library compatibility issue."
        echo "Try: ./fix_segfault.sh"
    fi
    exit $EXIT_CODE
fi

echo ""
echo "✅ All exports complete!"
