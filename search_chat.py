#!/usr/bin/env python3
"""
Search for a specific chat by ID or name

Usage:
    export ABACUS_API_KEY="your-key"
    python search_chat.py "7fb27921f"
    python search_chat.py "GPU Cost Crisis Solution"
"""

import os
import sys
from abacusai import ApiClient


def search_for_chat(client, search_term):
    """Try to find a chat using various methods"""
    
    print(f"🔍 Searching for: '{search_term}'")
    print("=" * 70)
    print()
    
    found = False
    
    # 1. Try to get it directly as a chat session
    print("1️⃣  Trying: get_chat_session(chat_session_id='{search_term}')")
    try:
        session = client.get_chat_session(chat_session_id=search_term)
        print(f"   ✓ FOUND! Chat session exists!")
        print(f"   Name: {getattr(session, 'name', 'N/A')}")
        print(f"   ID: {getattr(session, 'chat_session_id', 'N/A')}")
        print(f"   Project: {getattr(session, 'project_id', 'N/A')}")
        print(f"   Created: {getattr(session, 'created_at', 'N/A')}")
        if hasattr(session, 'chat_history'):
            print(f"   Messages: {len(session.chat_history) if session.chat_history else 0}")
        found = True
        print()
        return session
    except Exception as e:
        print(f"   ✗ Error: {e}")
        print()
    
    # 2. Try listing all sessions and searching
    print("2️⃣  Trying: list_chat_sessions() and searching...")
    try:
        sessions = client.list_chat_sessions()
        if sessions:
            print(f"   Found {len(sessions)} total session(s)")
            for s in sessions:
                sid = s.chat_session_id
                sname = getattr(s, 'name', '')
                if search_term.lower() in str(sid).lower() or search_term.lower() in str(sname).lower():
                    print(f"   ✓ MATCH: {sname} ({sid})")
                    found = True
        else:
            print(f"   ✗ No sessions returned by list_chat_sessions()")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    print()
    
    # 3. Check all projects for this chat
    print("3️⃣  Checking all projects...")
    try:
        projects = client.list_projects()
        for p in projects:
            print(f"   Project: {p.name} ({p.project_id})")
            
            # Try to describe project to see if it has chat references
            try:
                proj_detail = client.describe_project(project_id=p.project_id)
                # Check if there's any reference to our chat ID
                proj_str = str(vars(proj_detail))
                if search_term in proj_str:
                    print(f"      ✓ Reference found in project details!")
                    found = True
            except:
                pass
            
            # For AI_AGENT projects, check deployments
            if getattr(p, 'use_case', '') == 'AI_AGENT':
                try:
                    deployments = client.list_deployments(project_id=p.project_id)
                    if deployments:
                        for d in deployments:
                            convos = client.list_deployment_conversations(deployment_id=d.deployment_id)
                            if convos:
                                for c in convos:
                                    cid = c.deployment_conversation_id
                                    cname = getattr(c, 'name', '')
                                    if search_term.lower() in str(cid).lower() or search_term.lower() in str(cname).lower():
                                        print(f"      ✓ MATCH in deployment: {cname} ({cid})")
                                        found = True
                except:
                    pass
    except Exception as e:
        print(f"   ✗ Error: {e}")
    print()
    
    # 4. Try as deployment conversation
    print("4️⃣  Trying as deployment conversation...")
    try:
        # List all deployments across all projects
        projects = client.list_projects()
        for p in projects:
            try:
                deployments = client.list_deployments(project_id=p.project_id)
                for d in deployments:
                    try:
                        convo = client.get_deployment_conversation(deployment_conversation_id=search_term)
                        print(f"   ✓ FOUND as deployment conversation!")
                        print(f"   ID: {search_term}")
                        found = True
                        return convo
                    except:
                        pass
            except:
                pass
    except Exception as e:
        print(f"   ✗ Error: {e}")
    print()
    
    if not found:
        print("❌ Chat not found through any API method")
        print()
        print("This could mean:")
        print("  1. The ID format in the UI doesn't match the API")
        print("  2. The chat is accessed through a different endpoint")
        print("  3. The chat is in a different organization/account")
        print()
        print("Next step: Use browser DevTools to see what API calls the web UI makes")
    
    return None


def main():
    API_KEY = os.environ.get("ABACUS_API_KEY")
    if not API_KEY:
        print("❌ Error: ABACUS_API_KEY environment variable is required")
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("Usage: python search_chat.py <chat_id_or_name>")
        print()
        print("Examples:")
        print("  python search_chat.py '7fb27921f'")
        print("  python search_chat.py 'GPU Cost Crisis Solution'")
        sys.exit(1)
    
    search_term = sys.argv[1]
    client = ApiClient(API_KEY)
    
    result = search_for_chat(client, search_term)
    
    if result:
        print()
        print("=" * 70)
        print("✅ SUCCESS - Chat found!")
        print("=" * 70)
        print()
        print("You can export it with:")
        print(f"  python export_single_chat.py '{search_term}'")
    else:
        print()
        print("=" * 70)
        print("💡 DEBUG INSTRUCTIONS")
        print("=" * 70)
        print()
        print("To find the correct API endpoint:")
        print("1. Open Abacus.AI in your browser")
        print("2. Press F12 to open Developer Tools")
        print("3. Go to the Network tab")
        print("4. Click on the chat: 'GPU Cost Crisis Solution'")
        print("5. Look for XHR/Fetch requests")
        print("6. Find requests to api.abacus.ai")
        print("7. Note the endpoint path (e.g., /api/v0/getChatSession)")
        print("8. Share that with me and I'll update the scripts")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
