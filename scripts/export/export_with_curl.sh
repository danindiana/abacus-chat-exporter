#!/bin/bash
# Alternative export script using cURL instead of Python SDK
# Usage: ABACUS_API_KEY="..." ./export_with_curl.sh

set -e

API_KEY="${ABACUS_API_KEY}"
BASE_URL="https://api.abacus.ai/api/v0"
OUT_DIR="abacus_curl_exports"

if [ -z "$API_KEY" ]; then
    echo "❌ Error: ABACUS_API_KEY environment variable is required"
    exit 1
fi

mkdir -p "$OUT_DIR"

echo "🚀 Fetching chat sessions via cURL..."

# List all chat sessions
curl -s -H "x-api-key: $API_KEY" \
  "$BASE_URL/listChatSessions" > "$OUT_DIR/sessions.json"

# Check if we got valid JSON
if ! jq empty "$OUT_DIR/sessions.json" 2>/dev/null; then
    echo "❌ Error: Failed to fetch sessions or invalid response"
    cat "$OUT_DIR/sessions.json"
    exit 1
fi

# Count sessions
SESSION_COUNT=$(jq '.chatSessions | length' "$OUT_DIR/sessions.json")
echo "✓ Found $SESSION_COUNT session(s)"

if [ "$SESSION_COUNT" -eq 0 ]; then
    echo "No sessions to export."
    exit 0
fi

# Extract session IDs and export each one
jq -r '.chatSessions[] | .chatSessionId' "$OUT_DIR/sessions.json" | while read -r sid; do
    echo "Exporting session: $sid"
    
    # Export to HTML
    curl -s -X POST \
      -H "x-api-key: $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"chatSessionId\": \"$sid\"}" \
      "$BASE_URL/exportChatSession" > "$OUT_DIR/${sid}.html"
    
    # Get full session details as JSON
    curl -s -X POST \
      -H "x-api-key: $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"chatSessionId\": \"$sid\"}" \
      "$BASE_URL/getChatSession" > "$OUT_DIR/${sid}.json"
    
    echo "  ✓ Saved $OUT_DIR/${sid}.html and .json"
done

echo ""
echo "✅ Done! Exports saved in: $(realpath $OUT_DIR)"
