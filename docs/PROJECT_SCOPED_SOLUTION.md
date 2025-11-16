# Project-Scoped Chats - Important Discovery!

## 🎯 Key Finding

Your Abacus.AI account uses **project-scoped resources**. This means:

- ✅ Chats are organized by **Projects**
- ✅ Agents require a `project_id` parameter
- ✅ Deployments require a `project_id` parameter

## Your Projects

You have **4 projects**:

1. **Smaug Chrome Extension** (147ffe202) - Type: `CHAT_LLM`
2. **Smaug chrome extension** (14cd1c45b2) - Type: `AI_AGENT`
3. **Calisota RAG** (f3ebd9032) - Type: `AI_AGENT`
4. **chatllm-teams** (14264832aa) - Type: `CHAT_LLM`

## ✅ Solution: Use the New Export Script

I've created a new script that handles project-scoped chats:

```bash
python bulk_export_all_projects.py
```

This script will:
1. List all your projects
2. For each `CHAT_LLM` project → export chat sessions
3. For each `AI_AGENT` project → export agent conversations
4. Save everything organized by project

## 🚀 Quick Start

```bash
cd ~/programs/abacus-chat-exporter
source venv/bin/activate
export ABACUS_API_KEY="your-key"

# This now uses the new project-based exporter
./export_all.sh
```

Or run directly:

```bash
python bulk_export_all_projects.py
```

## 📁 Output Structure

Exports will be saved in:

```
exports/
├── Smaug_Chrome_Extension_147ffe202/
│   ├── 2025-10-21__chat_name__session123.html
│   └── 2025-10-21__chat_name__session123.json
├── Smaug_chrome_extension_14cd1c45b2/
│   └── (agent conversations)
├── Calisota_RAG_f3ebd9032/
│   └── (agent conversations)
└── chatllm-teams_14264832aa/
    └── (chat sessions)
```

## 🔍 What Changed

**Old scripts** tried to call:
- `list_chat_sessions()` without parameters → ✗ Returned empty
- `list_deployments()` without parameters → ✗ Required project_id
- `list_agents()` without parameters → ✗ Required project_id

**New script** properly:
- ✅ Lists all projects first
- ✅ Calls `list_deployments(project_id=...)` for each project
- ✅ Calls `list_agents(project_id=...)` for each project
- ✅ Exports conversations from each deployment
- ✅ Handles both CHAT_LLM and AI_AGENT project types

## 💡 Why This Happened

Abacus.AI's API architecture requires project context for most resources. The original scripts assumed global access to chats, but your account structure (correctly) scopes everything to projects for better organization.

This is actually a **good design** - it keeps your chats organized and isolated by project!
