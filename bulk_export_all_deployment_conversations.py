#!/usr/bin/env python3
"""
Export ALL deployment conversations from ALL projects

Usage:
    export ABACUS_API_KEY="your-key"
    python bulk_export_all_deployment_conversations.py
"""

import os
import sys
import pathlib
import time
from abacusai import ApiClient


def sanitize_filename(name: str, max_len: int = 80) -> str:
    """Sanitize a string for use in filenames"""
    return name.replace("/", "_").replace(" ", "_").replace(":", "-").replace("(", "").replace(")", "")[:max_len]


def main():
    API_KEY = os.environ.get("ABACUS_API_KEY")
    if not API_KEY:
        raise ValueError("ABACUS_API_KEY environment variable is required")
    
    print("🚀 Exporting ALL Deployment Conversations")
    print("=" * 70)
    print()
    
    client = ApiClient(API_KEY)
    
    # Create base output directory
    OUT_BASE = pathlib.Path("deployment_conversations_export")
    OUT_BASE.mkdir(parents=True, exist_ok=True)
    
    projects = client.list_projects()
    total_exported = 0
    
    for p in projects:
        project_id = p.project_id
        project_name = sanitize_filename(p.name or f"project_{project_id}")
        
        print(f"\n{'='*70}")
        print(f"📁 Project: {p.name}")
        print(f"{'='*70}\n")
        
        try:
            deployments = client.list_deployments(project_id=project_id)
            
            if not deployments:
                print("   ✗ No deployments")
                continue
            
            for d in deployments:
                deploy_id = d.deployment_id
                deploy_name = sanitize_filename(d.name or f"deployment_{deploy_id}")
                
                print(f"📦 Deployment: {d.name}")
                print(f"   ID: {deploy_id}")
                
                try:
                    convos = client.list_deployment_conversations(deployment_id=deploy_id)
                    
                    if not convos:
                        print(f"   ✗ No conversations\n")
                        continue
                    
                    print(f"   ✅ Found {len(convos)} conversation(s)")
                    print()
                    
                    # Create output directory for this deployment
                    OUT = OUT_BASE / f"{project_name}" / f"{deploy_name}_{deploy_id}"
                    OUT.mkdir(parents=True, exist_ok=True)
                    
                    for idx, c in enumerate(convos, 1):
                        cid = c.deployment_conversation_id
                        cname = sanitize_filename(getattr(c, 'name', f"convo_{cid}"))
                        stamp = sanitize_filename(getattr(c, 'created_at', str(time.time())))
                        
                        filename = f"{stamp}__{cname}__{cid}.html"
                        filepath = OUT / filename
                        
                        # Show progress
                        if idx % 50 == 0 or idx <= 5 or idx == len(convos):
                            print(f"   [{idx}/{len(convos)}] Exporting: {getattr(c, 'name', 'Untitled')[:60]}...")
                        
                        try:
                            export = client.export_deployment_conversation(deployment_conversation_id=cid)
                            html = export.conversation_export_html
                            
                            if not html:
                                html = f"<html><body><h1>Empty Export</h1><p>Conversation ID: {cid}</p></body></html>"
                            
                            with open(filepath, "w", encoding="utf-8") as f:
                                f.write(html)
                            
                            total_exported += 1
                        
                        except Exception as e:
                            print(f"   ✗ Export failed for {cid}: {e}")
                    
                    print(f"   ✓ Exported {len(convos)} conversations from {d.name}")
                    print(f"   📁 Saved to: {OUT.resolve()}")
                    print()
                
                except Exception as e:
                    print(f"   ✗ Error getting conversations: {e}\n")
        
        except Exception as e:
            print(f"   ✗ Error getting deployments: {e}\n")
    
    print("=" * 70)
    print(f"✅ EXPORT COMPLETE!")
    print("=" * 70)
    print(f"Total conversations exported: {total_exported}")
    print(f"📁 All files saved in: {OUT_BASE.resolve()}")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Export interrupted by user.")
        print(f"Partial export may be available in: deployment_conversations_export/")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
