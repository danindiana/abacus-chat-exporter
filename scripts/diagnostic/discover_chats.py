#!/usr/bin/env python3
"""
Diagnostic tool to explore your Abacus.AI account and find where chats are stored

Usage:
    export ABACUS_API_KEY="your-api-key"
    python discover_chats.py
"""

import os
import sys
from abacusai import ApiClient

def main():
    API_KEY = os.environ.get("ABACUS_API_KEY")
    if not API_KEY:
        print("❌ Error: ABACUS_API_KEY environment variable is required")
        sys.exit(1)
    
    print("🔍 Discovering chat locations in your Abacus.AI account...\n")
    client = ApiClient(API_KEY)
    
    # 1. Check AI Chat Sessions
    print("=" * 60)
    print("1️⃣  Checking AI Chat Sessions (Data Science Copilot)")
    print("=" * 60)
    try:
        sessions = client.list_chat_sessions()
        if sessions:
            print(f"✓ Found {len(sessions)} chat session(s)")
            for i, s in enumerate(sessions[:3], 1):  # Show first 3
                print(f"  {i}. {s.name or 'Untitled'} (ID: {s.chat_session_id})")
                print(f"     Created: {s.created_at or 'Unknown'}")
            if len(sessions) > 3:
                print(f"  ... and {len(sessions) - 3} more")
        else:
            print("✗ No AI Chat sessions found")
    except Exception as e:
        print(f"✗ Error accessing chat sessions: {e}")
    
    print()
    
    # 2. Check Projects (chats might be in projects)
    print("=" * 60)
    print("2️⃣  Checking Projects")
    print("=" * 60)
    try:
        projects = client.list_projects()
        if projects:
            print(f"✓ Found {len(projects)} project(s)")
            for i, p in enumerate(projects[:5], 1):
                print(f"  {i}. {p.name} (ID: {p.project_id})")
                print(f"     Use Case: {getattr(p, 'use_case', 'N/A')}")
        else:
            print("✗ No projects found")
    except Exception as e:
        print(f"✗ Error accessing projects: {e}")
    
    print()
    
    # 3. Check Deployments
    print("=" * 60)
    print("3️⃣  Checking Deployments (for Deployment Conversations)")
    print("=" * 60)
    try:
        deployments = client.list_deployments()
        if deployments:
            print(f"✓ Found {len(deployments)} deployment(s)")
            for i, d in enumerate(deployments[:5], 1):
                print(f"  {i}. {d.name} (ID: {d.deployment_id})")
                # Try to get conversations for this deployment
                try:
                    convos = client.list_deployment_conversations(deployment_id=d.deployment_id)
                    if convos:
                        print(f"     → Has {len(convos)} conversation(s)")
                    else:
                        print(f"     → No conversations")
                except:
                    print(f"     → Could not check conversations")
        else:
            print("✗ No deployments found")
    except Exception as e:
        print(f"✗ Error accessing deployments: {e}")
    
    print()
    
    # 4. Check Agents
    print("=" * 60)
    print("4️⃣  Checking AI Agents")
    print("=" * 60)
    try:
        agents = client.list_agents()
        if agents:
            print(f"✓ Found {len(agents)} agent(s)")
            for i, a in enumerate(agents[:5], 1):
                print(f"  {i}. {a.name} (ID: {a.agent_id})")
        else:
            print("✗ No agents found")
    except Exception as e:
        print(f"✗ Error accessing agents: {e}")
    
    print()
    
    # 5. Try to list chat messages directly
    print("=" * 60)
    print("5️⃣  Checking for Direct Chat Access")
    print("=" * 60)
    
    # Try different API methods that might list chats
    methods_to_try = [
        ('list_chat_sessions', {}),
        ('list_deployment_conversations', {}),
    ]
    
    for method_name, kwargs in methods_to_try:
        if hasattr(client, method_name):
            try:
                result = getattr(client, method_name)(**kwargs) if kwargs else getattr(client, method_name)()
                if result:
                    print(f"✓ {method_name}() returned {len(result)} item(s)")
            except Exception as e:
                print(f"✗ {method_name}() error: {e}")
    
    print()
    print("=" * 60)
    print("📋 Summary")
    print("=" * 60)
    print("""
If no chats were found, this could mean:

1. **You haven't created any chats yet**
   - Go to https://abacus.ai and start a conversation
   - Use the AI Chat or create a deployed assistant

2. **Chats are in a different location**
   - Check if you have chats in the web UI
   - They might be under a specific project or deployment

3. **API key permissions**
   - Verify your API key has read access to chats
   - Check in Settings → API Keys

4. **Organization/Account context**
   - If you're part of multiple orgs, chats might be in another org
   - API key might be scoped to a specific organization

Next steps:
- Visit https://abacus.ai and verify you have chats in the UI
- Check the URL when viewing a chat - it will show the structure
- If you see chats in UI but not via API, contact Abacus.AI support
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
