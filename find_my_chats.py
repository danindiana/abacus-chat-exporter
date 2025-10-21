#!/usr/bin/env python3
"""
Manual chat finder - checks all possible locations for chats in Abacus.AI

This is more thorough than the automated discovery and will show you
exactly what the API is returning.

Usage:
    export ABACUS_API_KEY="your-api-key"  
    python find_my_chats.py
"""

import os
import sys
import json
from abacusai import ApiClient

def safe_call(func, *args, **kwargs):
    """Safely call an API method and return result or None"""
    try:
        result = func(*args, **kwargs)
        return result
    except Exception as e:
        return None, str(e)

def main():
    API_KEY = os.environ.get("ABACUS_API_KEY")
    if not API_KEY:
        print("❌ Error: ABACUS_API_KEY environment variable is required")
        print("\nUsage:")
        print("  export ABACUS_API_KEY='your-key'")
        print("  python find_my_chats.py")
        sys.exit(1)
    
    print("🔍 Manual Chat Finder")
    print("=" * 70)
    print(f"API Key: {API_KEY[:10]}...{API_KEY[-4:]}")
    print("=" * 70)
    print()
    
    client = ApiClient(API_KEY)
    found_anything = False
    
    # 1. AI Chat Sessions
    print("📍 Location 1: AI Chat Sessions (list_chat_sessions)")
    print("-" * 70)
    sessions = safe_call(client.list_chat_sessions)
    if isinstance(sessions, tuple):  # Error occurred
        print(f"   ✗ API Error: {sessions[1]}")
    elif sessions:
        found_anything = True
        print(f"   ✓ FOUND {len(sessions)} chat session(s)!")
        print()
        for i, s in enumerate(sessions, 1):
            print(f"   Session {i}:")
            print(f"     • ID: {s.chat_session_id}")
            print(f"     • Name: {s.name or 'Untitled'}")
            print(f"     • Created: {getattr(s, 'created_at', 'Unknown')}")
            if hasattr(s, 'chat_history') and s.chat_history:
                print(f"     • Messages: {len(s.chat_history)}")
            print()
    else:
        print("   ✗ No chat sessions found (empty list returned)")
    print()
    
    # 2. Projects (check first, as other resources need project_id)
    print("📍 Location 2: Projects (list_projects)")
    print("-" * 70)
    projects = safe_call(client.list_projects)
    project_list = []
    if isinstance(projects, tuple):
        print(f"   ✗ API Error: {projects[1]}")
    elif projects:
        project_list = projects
        print(f"   ✓ Found {len(projects)} project(s)")
        print()
        for p in projects:
            print(f"   Project: {p.name}")
            print(f"     • ID: {p.project_id}")
            print(f"     • Use Case: {getattr(p, 'use_case', 'N/A')}")
            print()
    else:
        print("   ✗ No projects found")
    print()
    
    # 3. Deployments (need project_id)
    print("📍 Location 3: Deployments in Projects")
    print("-" * 70)
    if project_list:
        for p in project_list:
            print(f"   Checking project: {p.name}")
            deployments = safe_call(client.list_deployments, project_id=p.project_id)
            if isinstance(deployments, tuple):
                print(f"     ✗ Error: {deployments[1]}")
                        print(f"     ✓ Found {len(deployments)} deployment(s)")
                for d in deployments:
                    print(f"       Deployment: {d.name}")
                    print(f"         • ID: {d.deployment_id}")
                    print(f"         • Status: {getattr(d, 'status', 'Unknown')}")
                    
                    # Check for conversations
                    convos = safe_call(client.list_deployment_conversations, deployment_id=d.deployment_id)
                    if isinstance(convos, tuple):
                        print(f"         • Conversations: Error - {convos[1]}")
                    elif convos:
                        found_anything = True
                        print(f"         • Conversations: ✓ FOUND {len(convos)}!")
                        for c in convos[:2]:  # Show first 2
                            print(f"           - {getattr(c, 'name', 'Untitled')} ({c.deployment_conversation_id})")
                        if len(convos) > 2:
                            print(f"           ... and {len(convos) - 2} more")
                    else:
                        print(f"         • Conversations: None")
                print()
            else:
                print(f"     ✗ No deployments")
    else:
        print("   ⚠ No projects found - deployments require project_id")
    print()
    
    # 4. Agents (need project_id)
    print("📍 Location 4: AI Agents in Projects")
    print("-" * 70)
    if project_list:
        for p in project_list:
            print(f"   Checking project: {p.name}")
            agents = safe_call(client.list_agents, project_id=p.project_id)
            if isinstance(agents, tuple):
                print(f"     ✗ Error: {agents[1]}")
                        print(f"     ✓ Found {len(agents)} agent(s)")
                for a in agents:
                    print(f"       Agent: {a.name}")
                    print(f"         • ID: {a.agent_id}")
                    print(f"         • Type: {getattr(a, 'agent_type', 'Unknown')}")
                    found_anything = True
                print()
            else:
                print(f"     ✗ No agents")
    else:
        print("   ⚠ No projects found - agents require project_id")
    print()
    
    # Summary
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print()
    
    if found_anything:
        print("✅ SUCCESS! Found chats/agents/deployments in your account!")
        print()
        print("Next steps:")
        print("  1. Export ALL chats from ALL projects (RECOMMENDED):")
        print("     → Run: python bulk_export_all_projects.py")
        print()
        print("  2. If you want to export from a specific project:")
        print("     → Note the project_id from above")
        print("     → Edit the export scripts to filter by project")
        print()
        print("  3. For deployment conversations:")
        print("     → Use the deployment_id shown above")
        print("     → Run: python bulk_export_deployment_convos.py")
        print()
    else:
        print("⚠️  NO CHATS FOUND in your Abacus.AI account")
        print()
        print("Possible reasons:")
        print()
        print("  1. You haven't created any chats yet")
        print("     → Go to https://abacus.ai and start a conversation")
        print()
        print("  2. API key doesn't have the right permissions")
        print("     → Check your API key in Settings → API Keys")
        print("     → Ensure it has 'read' permissions")
        print()
        print("  3. Chats are in a different organization")
        print("     → API keys are organization-specific")
        print("     → Make sure you're using the right org's key")
        print()
        print("  4. Chats use a different API endpoint")
        print("     → Check the browser URL when viewing chats")
        print("     → Run: python explore_api.py")
        print()
        print("  5. Web UI vs API mismatch")
        print("     → If you see chats in the web interface")
        print("     → But not via API, contact support@abacus.ai")
        print()
        print("Next steps:")
        print("  • Visit https://abacus.ai in your browser")
        print("  • Create a test chat if none exist")
        print("  • Run this script again")
        print("  • Read FINDING_CHATS.md for more help")
    
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
