# Quick Reference - Finding & Exporting Chats

## 🚨 Problem: "No chat sessions found"

Run these commands in order:

### 1. Find Your Chats

```bash
cd ~/programs/abacus-chat-exporter
source venv/bin/activate
export ABACUS_API_KEY="your-api-key-here"

# Run the comprehensive finder
python find_my_chats.py
```

This will tell you exactly where your chats are (if they exist).

### 2. Export Based on What You Found

**If chats were found in "AI Chat Sessions":**
```bash
./export_all.sh
```

**If chats were found in "Deployment Conversations":**
```bash
export DEPLOYMENT_ID="your-deployment-id"
./export_all.sh
```

Or directly:
```bash
python bulk_export_deployment_convos.py
```

### 3. Still No Chats?

**Check the web interface:**
1. Go to https://abacus.ai
2. Do you see any chats in the UI?
3. If YES → Look at the URL when you open a chat
4. If NO → Create a test chat first

**URL patterns tell you where chats are:**
- `https://abacus.ai/app/chat_llm/xxx` → AI Chat Session
- `https://abacus.ai/app/deployment/xxx` → Deployment Conversation
- `https://abacus.ai/app/agent/xxx/playground` → Agent Chat

### 4. Explore API Methods

```bash
python explore_api.py
```

Shows all available API methods related to chats.

## 📝 Common Scenarios

### Scenario A: Using ChatLLM (Data Science Copilot)

Your chats should appear in `list_chat_sessions()`.

**Export command:**
```bash
python bulk_export_ai_chat.py
```

### Scenario B: Using Deployed Agents/Assistants

Your chats are "Deployment Conversations".

**First, find deployment ID:**
```bash
python -c "
from abacusai import ApiClient
import os
client = ApiClient(os.environ['ABACUS_API_KEY'])
deployments = client.list_deployments()
for d in deployments:
    print(f'{d.name}: {d.deployment_id}')
"
```

**Then export:**
```bash
export DEPLOYMENT_ID="abc123..."
python bulk_export_deployment_convos.py
```

### Scenario C: Brand New Account

If you just created your Abacus.AI account:
1. You need to create chats first
2. Go to https://abacus.ai
3. Start a conversation
4. Then run the export scripts

## 🔧 Diagnostic Tools

| Script | Purpose |
|--------|---------|
| `find_my_chats.py` | 🎯 **Start here** - Comprehensive search |
| `discover_chats.py` | Lists all resources in your account |
| `explore_api.py` | Shows all available API methods |
| `diagnose.sh` | Interactive diagnostic wrapper |

## 💡 Pro Tips

1. **Save your API key in .env file:**
   ```bash
   echo "ABACUS_API_KEY=your-key" > .env
   ```
   Then you don't need to export it each time.

2. **Check multiple locations:**
   Chats might be split between AI Chat and Deployments.

3. **API key permissions:**
   Make sure your API key has read access to chats.

4. **Organization context:**
   If you're in multiple orgs, ensure you're using the right API key.

## 📚 Full Documentation

- `README.md` - Complete project documentation
- `FINDING_CHATS.md` - Detailed troubleshooting for finding chats
- `TROUBLESHOOTING.md` - Fix common issues
- `QUICKSTART.md` - Basic setup and usage

## 🆘 Need Help?

1. Read `FINDING_CHATS.md` for detailed guidance
2. Check Abacus.AI documentation: https://abacus.ai/help/api/
3. Contact support: support@abacus.ai
