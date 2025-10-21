# Finding Your Chats - Diagnostic Guide

If `export_all.sh` reports "No chat sessions found", follow these steps to locate your chats.

## Step 1: Run the Discovery Script

This will scan your Abacus.AI account for all possible chat locations:

```bash
cd ~/programs/abacus-chat-exporter
source venv/bin/activate

# Set your API key for this session
export ABACUS_API_KEY="your-api-key-here"

# Run discovery
python discover_chats.py
```

This will check:
- AI Chat Sessions (Data Science Copilot)
- Deployment Conversations
- Projects
- Agents

## Step 2: Explore Available API Methods

If the discovery script doesn't find chats, explore what methods are available:

```bash
python explore_api.py
```

This shows all chat-related API methods and tests them.

## Step 3: Check the Web Interface

1. Go to https://abacus.ai
2. Open any chat you want to export
3. Look at the browser URL

### Common URL Patterns:

**AI Chat (ChatLLM):**
```
https://abacus.ai/app/chat_llm/abc123
```
→ Use `bulk_export_ai_chat.py`

**Agent Playground:**
```
https://abacus.ai/app/agent/xyz789/playground
```
→ Chats are agent-specific

**Deployment Conversations:**
```
https://abacus.ai/app/deployment/deploy123
```
→ Use `bulk_export_deployment_convos.py` with `DEPLOYMENT_ID=deploy123`

## Step 4: Possible Scenarios

### Scenario A: Chats exist but API returns empty

The `list_chat_sessions()` API might be filtering by some criteria. Try:

```python
# Manual test
from abacusai import ApiClient
client = ApiClient("your-api-key")

# Try with different parameters if available
sessions = client.list_chat_sessions()
print(f"Found: {len(sessions)}")

# Check if there's a project_id or filter parameter
# (Inspect the method signature)
```

### Scenario B: Chats are in Agent conversations

If your chats are with AI Agents, they might be accessed differently:

```bash
# List all agents first
python -c "
from abacusai import ApiClient
import os
client = ApiClient(os.environ['ABACUS_API_KEY'])
agents = client.list_agents()
for a in agents:
    print(f'Agent: {a.name} (ID: {a.agent_id})')
"
```

Then check if agents have conversations:
- Agent sessions might be in deployment conversations
- Or accessed through agent-specific methods

### Scenario C: Chats are project-scoped

If chats are organized by project:

```bash
# List projects and their chats
python -c "
from abacusai import ApiClient
import os
client = ApiClient(os.environ['ABACUS_API_KEY'])
projects = client.list_projects()
for p in projects:
    print(f'Project: {p.name} (ID: {p.project_id})')
    # Try to get chats for this project
    # (method name depends on API structure)
"
```

### Scenario D: Using the wrong account/organization

If you're part of multiple Abacus.AI organizations:

1. Check which org your API key belongs to
2. Make sure you're looking at chats in that org's web interface
3. API keys are organization-specific

## Step 5: Create a Custom Export Script

If chats are found but in a non-standard location, create a custom script:

```bash
# Copy the template
cp bulk_export_ai_chat.py bulk_export_custom.py

# Edit to use the correct API method
# nano bulk_export_custom.py
```

## Still Can't Find Chats?

### Option 1: Check API Documentation

Visit: https://abacus.ai/help/api/

Search for methods containing:
- "chat"
- "conversation"
- "message"
- "session"

### Option 2: Export from Web UI Manually

As a fallback, you can export individual chats from the web interface:
1. Open a chat in Abacus.AI
2. Look for export/download options in the UI
3. Use browser dev tools to capture the export API call
4. Replicate it in a script

### Option 3: Contact Abacus.AI Support

If you see chats in the web UI but can't access them via API:

1. Email: support@abacus.ai
2. Mention: "Cannot access chat sessions via list_chat_sessions() API"
3. Include: Your use case and what you see in the web UI

## Debug Output

When running the discovery script, save the output:

```bash
python discover_chats.py > discovery_output.txt 2>&1
cat discovery_output.txt
```

This can help identify the issue or provide info to support.
