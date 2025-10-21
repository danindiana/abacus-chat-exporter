# Abacus.AI Chat Exporter & PDF Processor

Thinking of leaving abacus.ai but can't seem to find anyway to take your data with you? 

Then the Abacus.ai Chat Exporter is for you!

**Two powerful tools for Abacus.AI:**
1. 💬 **Chat Exporter**: Bulk download your chat conversations to HTML and JSON format
2. 📄 **PDF Processor**: Batch upload and process PDFs with automated prompts

## 🚀 Quick Start

### Export Chats

**Export all chats from all projects:**

```bash
cd ~/programs/abacus-chat-exporter
source venv/bin/activate
export ABACUS_API_KEY="your-key"

# Run the export
./export_all.sh
```

### ⚠️ Important: Do You Have Chats to Export?

**If the export completes but folders are empty:**
- You may not have created any chats yet
- Go to https://abacus.ai and verify chats exist in the web UI
- See **[NO_CHATS_FOUND.md](NO_CHATS_FOUND.md)** for diagnosis

**If you're seeing API errors:**
- See **[PROJECT_SCOPED_SOLUTION.md](PROJECT_SCOPED_SOLUTION.md)** 
- Or **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** for troubleshooting

### Process PDFs

**Batch upload and process PDFs with automated prompts:**

```bash
./process_pdfs.sh
```

See **[PDF_PROCESSING.md](PDF_PROCESSING.md)** for detailed documentation.

## Overview

### Chat Exporter
Abacus.AI provides APIs to list and export chat sessions. This tool includes scripts for:

- **Option A**: Exporting "Data Science Copilot" chats (AI Chat)
- **Option B**: Exporting "Deployment Conversations" (production assistant chats)
- **Diagnostic Tools**: Find where your chats are stored

### PDF Processor
Automates bulk PDF uploads to Abacus.AI with three-stage processing:
1. Summarize the paper
2. Extract insights using symbolic logic
3. Demonstrate insights with C++ code examples

## Setup

### 1. Install Dependencies

The project includes a pre-configured Python 3.13 virtual environment. Activate it:

```bash
cd ~/programs/abacus-chat-exporter
source venv/bin/activate
```

Or if starting fresh:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Get Your API Key

1. Log into Abacus.AI
2. Navigate to **Settings → Profile & Billing**
3. Enable API metering
4. Go to **API Keys Dashboard** and create a new key
5. Save your key securely

## Usage

### Option A: Export AI Chat Sessions

Export all your Data Science Copilot chat sessions:

```bash
export ABACUS_API_KEY="your-api-key-here"
python bulk_export_ai_chat.py
```

This will create a folder `abacus_ai_chat_exports/` containing:
- `.html` files for human-readable chat history
- `.json` files for full fidelity data (can be used to rehydrate later)

### Option B: Export Deployment Conversations

Export conversations from a specific deployed assistant:

```bash
export ABACUS_API_KEY="your-api-key-here"
export DEPLOYMENT_ID="your-deployment-id"
python bulk_export_deployment_convos.py
```

This will create a folder `abacus_deployment_{DEPLOYMENT_ID}_exports/` with HTML exports.

## Output Format

### File Naming

Files are named with the pattern: `{timestamp}__{name}__{id}.{ext}`

Example: `2025-10-21T10-30-00__my_chat_session__abc123.html`

### HTML Exports

Human-readable chat history with formatting and structure preserved.

### JSON Exports (AI Chat only)

Complete data dump including:
- Chat session metadata
- Full message history
- Timestamps
- All custom fields

## Advanced Usage

### Using cURL

If you prefer shell scripting:

```bash
# List all AI Chat sessions
curl -s -H "x-api-key: $ABACUS_API_KEY" \
  "https://api.abacus.ai/api/v0/listChatSessions" > sessions.json

# Export a specific session
curl -s -X POST -H "x-api-key: $ABACUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"chatSessionId": "your-session-id"}' \
  "https://api.abacus.ai/api/v0/exportChatSession" > export.html
```

## API Documentation

- [listChatSessions](https://abacus.ai/help/api/ref/ai_chat/listChatSessions)
- [exportChatSession](https://abacus.ai/help/api/ref/ai_chat/exportChatSession)
- [exportDeploymentConversation](https://abacus.ai/help/ref/deployment_conversations/exportDeploymentConversation)
- [Python SDK Guide](https://abacus.ai/help/sdk)

## Compliance

For full account-level data exports (GDPR/CCPA requests), contact Abacus.AI support. They honor data access requests with a ~15-day turnaround.

## Troubleshooting

### No Chats Found

If the export script reports "No chat sessions found":

1. **Run the discovery tool:**
   ```bash
   source venv/bin/activate
   export ABACUS_API_KEY="your-key"
   python discover_chats.py
   ```

2. **Check the web interface:**
   - Visit https://abacus.ai and verify you have chats
   - Note the URL pattern when viewing a chat
   - See `FINDING_CHATS.md` for detailed guidance

3. **Explore API methods:**
   ```bash
   python explore_api.py
   ```

### Authentication Issues

- Verify your API key is correct
- Ensure API metering is enabled in your account
- Check that the key has not expired

### Export Failures

The scripts include fallback mechanisms:
- If `exportChatSession` fails, the script will fetch raw data via `getChatSession` and render HTML locally
- Both HTML and JSON are saved to preserve data integrity

### Segmentation Faults

If you get segmentation faults (exit code 139):
```bash
./fix_segfault.sh
```
See `TROUBLESHOOTING.md` for details.

## Project Files

### Export Scripts
- `bulk_export_ai_chat.py` - Export AI Chat sessions
- `bulk_export_deployment_convos.py` - Export deployment conversations  
- `export_all.sh` - Convenience wrapper for both exports
- `export_with_curl.sh` - Alternative shell-based exporter

### Diagnostic Tools
- `find_my_chats.py` - 🎯 **Start here** - Comprehensive chat finder
- `discover_chats.py` - Scan all account resources
- `explore_api.py` - List all available API methods
- `diagnose.sh` - Interactive diagnostic tool

### Utilities
- `activate.sh` - Activate virtual environment
- `fix_segfault.sh` - Fix Python 3.13 compatibility issues
- `test_api.py` - Test API connection

### Documentation
- `README.md` - This file
- `QUICK_REFERENCE.md` - Fast lookup for finding & exporting
- `FINDING_CHATS.md` - Detailed troubleshooting for missing chats
- `TROUBLESHOOTING.md` - Fix common issues
- `QUICKSTART.md` - Basic setup and usage

## License

Free to use and modify for personal or commercial use.
