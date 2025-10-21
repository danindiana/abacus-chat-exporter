#!/usr/bin/env python3
"""
Detailed diagnostic - shows exactly what's in each project

Usage:
    export ABACUS_API_KEY="your-key"
    python debug_projects.py
"""

import os
import sys
from abacusai import ApiClient


def main():
    API_KEY = os.environ.get("ABACUS_API_KEY")
    if not API_KEY:
        print("❌ Error: ABACUS_API_KEY environment variable is required")
        sys.exit(1)
    
    client = ApiClient(API_KEY)
    
    print("🔍 Detailed Project Analysis")
    print("=" * 70)
    print()
    
    # Get all projects
    projects = client.list_projects()
    print(f"Found {len(projects)} projects\n")
    
    for i, p in enumerate(projects, 1):
        print(f"\n{'='*70}")
        print(f"PROJECT {i}: {p.name}")
        print(f"{'='*70}")
        print(f"ID: {p.project_id}")
        print(f"Use Case: {getattr(p, 'use_case', 'N/A')}")
        print()
        
        # For CHAT_LLM projects
        if getattr(p, 'use_case', '') == 'CHAT_LLM':
            print("📝 Type: CHAT_LLM (Chat Sessions)")
            print("-" * 70)
            
            # Try to list chat sessions (might need project filtering)
            try:
                print("Attempting: client.list_chat_sessions()")
                sessions = client.list_chat_sessions()
                if sessions:
                    print(f"✓ Found {len(sessions)} chat session(s) globally")
                    for s in sessions[:3]:
                        print(f"  - {s.name or 'Untitled'} ({s.chat_session_id})")
                        # Check if session belongs to this project
                        if hasattr(s, 'project_id'):
                            print(f"    Project: {s.project_id}")
                else:
                    print("✗ No chat sessions returned")
            except Exception as e:
                print(f"✗ Error: {e}")
            
            print()
            
            # Try with project_id if the method accepts it
            try:
                print(f"Attempting: client.list_chat_sessions(project_id='{p.project_id}')")
                sessions = client.list_chat_sessions(project_id=p.project_id)
                if sessions:
                    print(f"✓ Found {len(sessions)} session(s) for this project!")
                    for s in sessions[:5]:
                        print(f"  - {s.name or 'Untitled'} ({s.chat_session_id})")
                        print(f"    Created: {getattr(s, 'created_at', 'Unknown')}")
                else:
                    print("✗ No sessions for this project")
            except TypeError as e:
                print(f"⚠ Method doesn't accept project_id parameter: {e}")
            except Exception as e:
                print(f"✗ Error: {e}")
        
        # For AI_AGENT projects
        elif getattr(p, 'use_case', '') == 'AI_AGENT':
            print("🤖 Type: AI_AGENT (Agent Deployments)")
            print("-" * 70)
            
            # List agents
            try:
                print(f"Checking agents: client.list_agents(project_id='{p.project_id}')")
                agents = client.list_agents(project_id=p.project_id)
                if agents:
                    print(f"✓ Found {len(agents)} agent(s)")
                    for a in agents:
                        print(f"  Agent: {a.name} ({a.agent_id})")
                else:
                    print("✗ No agents in this project")
            except Exception as e:
                print(f"✗ Error listing agents: {e}")
            
            print()
            
            # List deployments
            try:
                print(f"Checking deployments: client.list_deployments(project_id='{p.project_id}')")
                deployments = client.list_deployments(project_id=p.project_id)
                if deployments:
                    print(f"✓ Found {len(deployments)} deployment(s)")
                    for d in deployments:
                        print(f"  Deployment: {d.name} ({d.deployment_id})")
                        
                        # Check for conversations in this deployment
                        try:
                            convos = client.list_deployment_conversations(deployment_id=d.deployment_id)
                            if convos:
                                print(f"    ✓ Has {len(convos)} conversation(s)!")
                                for c in convos[:3]:
                                    print(f"      - {getattr(c, 'name', 'Untitled')} ({c.deployment_conversation_id})")
                            else:
                                print(f"    ✗ No conversations")
                        except Exception as e:
                            print(f"    ✗ Error getting conversations: {e}")
                else:
                    print("✗ No deployments in this project")
            except Exception as e:
                print(f"✗ Error listing deployments: {e}")
        
        print()
    
    print("\n" + "="*70)
    print("💡 ANALYSIS")
    print("="*70)
    print("""
If you see:
- "No chat sessions returned" → Chats might not exist, or need different API call
- "No agents/deployments" → Project has no resources yet
- "Has X conversations" → These can be exported!

Next step: Check the Abacus.AI web UI to confirm chats actually exist.
    """)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
