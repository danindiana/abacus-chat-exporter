#!/usr/bin/env python3
"""
Find ALL deployment conversations across all projects

Usage:
    export ABACUS_API_KEY="your-key"
    python find_all_deployment_conversations.py
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
    
    print("🔍 Finding ALL Deployment Conversations")
    print("=" * 70)
    print()
    
    total_conversations = 0
    projects_with_convos = []
    
    projects = client.list_projects()
    
    for p in projects:
        project_id = p.project_id
        project_name = p.name
        use_case = getattr(p, 'use_case', 'UNKNOWN')
        
        print(f"📁 Project: {project_name}")
        print(f"   ID: {project_id}")
        print(f"   Type: {use_case}")
        
        # List deployments for this project
        try:
            deployments = client.list_deployments(project_id=project_id)
            
            if not deployments:
                print(f"   ✗ No deployments")
                print()
                continue
            
            print(f"   ✓ Found {len(deployments)} deployment(s)")
            
            for d in deployments:
                deploy_id = d.deployment_id
                deploy_name = d.name
                print(f"      📦 Deployment: {deploy_name} ({deploy_id})")
                
                # List conversations for this deployment
                try:
                    convos = client.list_deployment_conversations(deployment_id=deploy_id)
                    
                    if convos:
                        print(f"         ✅ {len(convos)} conversation(s)!")
                        total_conversations += len(convos)
                        
                        projects_with_convos.append({
                            'project': project_name,
                            'project_id': project_id,
                            'deployment': deploy_name,
                            'deployment_id': deploy_id,
                            'count': len(convos),
                            'conversations': convos
                        })
                        
                        for c in convos[:5]:  # Show first 5
                            cid = c.deployment_conversation_id
                            cname = getattr(c, 'name', 'Untitled')
                            created = getattr(c, 'created_at', 'Unknown')
                            print(f"           • {cname}")
                            print(f"             ID: {cid}")
                            print(f"             Created: {created}")
                        
                        if len(convos) > 5:
                            print(f"           ... and {len(convos) - 5} more")
                    else:
                        print(f"         ✗ No conversations")
                
                except Exception as e:
                    print(f"         ✗ Error: {e}")
        
        except Exception as e:
            print(f"   ✗ Error listing deployments: {e}")
        
        print()
    
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"Total conversations found: {total_conversations}")
    print()
    
    if total_conversations > 0:
        print("✅ SUCCESS! Found conversations to export:")
        print()
        for item in projects_with_convos:
            print(f"Project: {item['project']}")
            print(f"  Deployment: {item['deployment']} ({item['deployment_id']})")
            print(f"  Conversations: {item['count']}")
            print()
        
        print("To export ALL conversations:")
        print("  python bulk_export_all_deployment_conversations.py")
        print()
        print("To export from a specific deployment:")
        for item in projects_with_convos:
            print(f"  export DEPLOYMENT_ID='{item['deployment_id']}'")
            print(f"  python bulk_export_deployment_convos.py")
            break
    else:
        print("❌ No deployment conversations found")
        print()
        print("This means:")
        print("  1. Deployments exist but have no conversations yet")
        print("  2. You need to interact with a deployed agent to create conversations")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
