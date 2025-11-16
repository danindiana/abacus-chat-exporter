#!/usr/bin/env python3
"""
Export all chats from all projects in your Abacus.AI account

This version iterates through all projects and exports chats from each one.

Usage:
    export ABACUS_API_KEY="your-api-key"
    python bulk_export_all_projects.py
"""

import os
import sys
import json
import pathlib
import time
from abacusai import ApiClient


def sanitize_filename(name: str, max_len: int = 80) -> str:
    """Sanitize a string for use in filenames"""
    return name.replace("/", "_").replace(" ", "_").replace(":", "-").replace("(", "").replace(")", "")[:max_len]


def export_project_chats(client, project):
    """Export chats from a specific project"""
    project_id = project.project_id
    project_name = sanitize_filename(project.name or f"project_{project_id}")
    use_case = getattr(project, 'use_case', 'UNKNOWN')
    
    print(f"\n{'='*70}")
    print(f"📁 Project: {project.name}")
    print(f"   ID: {project_id}")
    print(f"   Type: {use_case}")
    print(f"{'='*70}\n")
    
    # Create output directory for this project
    OUT = pathlib.Path(f"exports/{project_name}_{project_id}")
    OUT.mkdir(parents=True, exist_ok=True)
    
    total_exported = 0
    
    # Try different methods based on use case
    if use_case == 'CHAT_LLM':
        # Try to get chat sessions for this project
        try:
            # First try: list_chat_sessions with project filter
            print("   Checking for chat sessions...")
            sessions = client.list_chat_sessions()  # This might auto-filter by project
            
            if sessions:
                print(f"   ✓ Found {len(sessions)} chat session(s)")
                for idx, s in enumerate(sessions, 1):
                    sid = s.chat_session_id
                    name = sanitize_filename(s.name or f"session_{sid}")
                    stamp = sanitize_filename(getattr(s, 'created_at', str(time.time())))
                    base = OUT / f"{stamp}__{name}__{sid}"
                    
                    print(f"   [{idx}/{len(sessions)}] Exporting: {name}")
                    
                    # Save JSON
                    try:
                        with open(f"{base}.json", "w", encoding="utf-8") as f:
                            json.dump(s.to_dict(), f, ensure_ascii=False, indent=2)
                        print(f"      ✓ Saved JSON")
                    except Exception as e:
                        print(f"      ✗ JSON failed: {e}")
                    
                    # Export HTML
                    try:
                        resp = client.export_chat_session(chat_session_id=sid)
                        if isinstance(resp, (bytes, bytearray)):
                            html = resp.decode("utf-8", errors="ignore")
                        elif isinstance(resp, str):
                            html = resp
                        else:
                            raise RuntimeError("Using fallback")
                        
                        with open(f"{base}.html", "w", encoding="utf-8") as f:
                            f.write(html)
                        print(f"      ✓ Saved HTML")
                        total_exported += 1
                    except Exception as e:
                        print(f"      ⚠ Export API failed, using fallback...")
                        try:
                            full = client.get_chat_session(chat_session_id=sid)
                            msgs = getattr(full, 'chat_history', [])
                            
                            html_parts = [
                                "<!DOCTYPE html>",
                                "<html><head><meta charset='utf-8'>",
                                f"<title>{name}</title>",
                                "<style>body{font-family:sans-serif;max-width:900px;margin:40px auto;padding:20px;}",
                                "h3{color:#666;margin-top:20px;}pre{background:#f5f5f5;padding:15px;border-radius:5px;overflow-x:auto;}",
                                "hr{border:none;border-top:1px solid #ddd;margin:20px 0;}</style></head><body>",
                                f"<h1>{name}</h1><p><em>Session: {sid}</em></p><hr/>"
                            ]
                            
                            for m in msgs:
                                who = getattr(m, 'role', 'user')
                                text = str(getattr(m, 'text', m))
                                html_parts.append(f"<h3>{who.upper()}</h3><pre>{text}</pre><hr/>")
                            
                            html_parts.append("</body></html>")
                            
                            with open(f"{base}.html", "w", encoding="utf-8") as f:
                                f.write("\n".join(html_parts))
                            print(f"      ✓ Saved HTML (fallback)")
                            total_exported += 1
                        except Exception as fe:
                            print(f"      ✗ Fallback failed: {fe}")
            else:
                print("   ✗ No chat sessions in this project")
        except Exception as e:
            print(f"   ✗ Error accessing chats: {e}")
    
    elif use_case == 'AI_AGENT':
        # Try to get agents and their conversations
        try:
            print("   Checking for AI agents...")
            agents = client.list_agents(project_id=project_id)
            
            if agents:
                print(f"   ✓ Found {len(agents)} agent(s)")
                for agent in agents:
                    agent_id = agent.agent_id
                    agent_name = sanitize_filename(agent.name or f"agent_{agent_id}")
                    print(f"      Agent: {agent.name}")
                    
                    # Try to get deployments for this agent
                    try:
                        deployments = client.list_deployments(project_id=project_id)
                        if deployments:
                            for deploy in deployments:
                                deploy_id = deploy.deployment_id
                                print(f"         Deployment: {deploy.name} ({deploy_id})")
                                
                                # Get conversations
                                convos = client.list_deployment_conversations(deployment_id=deploy_id)
                                if convos:
                                    print(f"         ✓ Found {len(convos)} conversation(s)")
                                    for c in convos:
                                        cid = c.deployment_conversation_id
                                        stamp = sanitize_filename(getattr(c, 'created_at', str(time.time())))
                                        cname = sanitize_filename(getattr(c, 'name', f"convo_{cid}"))
                                        
                                        filepath = OUT / f"{stamp}__{agent_name}__{cname}__{cid}.html"
                                        
                                        export = client.export_deployment_conversation(deployment_conversation_id=cid)
                                        html = export.conversation_export_html
                                        
                                        with open(filepath, "w", encoding="utf-8") as f:
                                            f.write(html or "<html><body>Empty</body></html>")
                                        
                                        print(f"            ✓ Exported: {cname}")
                                        total_exported += 1
                                else:
                                    print(f"         ✗ No conversations")
                    except Exception as e:
                        print(f"         ✗ Error getting deployments: {e}")
            else:
                print("   ✗ No agents in this project")
        except Exception as e:
            print(f"   ✗ Error accessing agents: {e}")
    
    else:
        print(f"   ⚠ Unknown use case: {use_case}")
    
    if total_exported > 0:
        print(f"\n   ✅ Exported {total_exported} item(s) from this project")
        print(f"   📁 Saved to: {OUT.resolve()}")
    else:
        print(f"\n   ⚠ No chats exported from this project")
    
    return total_exported


def main():
    API_KEY = os.environ.get("ABACUS_API_KEY")
    if not API_KEY:
        raise ValueError("ABACUS_API_KEY environment variable is required")
    
    print("🚀 Abacus.AI Project-Based Chat Exporter")
    print("=" * 70)
    print()
    
    client = ApiClient(API_KEY)
    
    # Get all projects
    print("Fetching projects...")
    projects = client.list_projects()
    
    if not projects:
        print("❌ No projects found in your account")
        return
    
    print(f"✓ Found {len(projects)} project(s)\n")
    
    total_all = 0
    
    for project in projects:
        try:
            count = export_project_chats(client, project)
            total_all += count
        except Exception as e:
            print(f"   ❌ Error processing project: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 70)
    print(f"✅ COMPLETE! Exported {total_all} total chat(s)")
    print(f"📁 All exports saved in: exports/")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Export interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
