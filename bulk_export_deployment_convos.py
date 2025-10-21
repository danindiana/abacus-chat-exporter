#!/usr/bin/env python3
"""
Bulk export all Deployment Conversations from an Abacus.AI deployment

Usage:
    export ABACUS_API_KEY="your-api-key-here"
    export DEPLOYMENT_ID="your-deployment-id"
    python bulk_export_deployment_convos.py

Output:
    Creates abacus_deployment_{DEPLOYMENT_ID}_exports/ directory with HTML files
"""

import os
import pathlib
import time
from abacusai import ApiClient


def sanitize_filename(name: str, max_len: int = 80) -> str:
    """Sanitize a string for use in filenames"""
    return name.replace("/", "_").replace(" ", "_").replace(":", "-")[:max_len]


def export_deployment_conversations():
    # Configuration
    API_KEY = os.environ.get("ABACUS_API_KEY")
    DEPLOYMENT_ID = os.environ.get("DEPLOYMENT_ID")
    
    if not API_KEY:
        raise ValueError("ABACUS_API_KEY environment variable is required")
    if not DEPLOYMENT_ID:
        raise ValueError("DEPLOYMENT_ID environment variable is required")
    
    # Initialize client
    client = ApiClient(API_KEY)
    
    # Create output directory
    OUT = pathlib.Path(f"abacus_deployment_{DEPLOYMENT_ID}_exports")
    OUT.mkdir(parents=True, exist_ok=True)
    
    print(f"Fetching conversations for deployment: {DEPLOYMENT_ID}...")
    
    # List all conversations for this deployment
    convos = client.list_deployment_conversations(deployment_id=DEPLOYMENT_ID)
    
    if not convos:
        print("No conversations found for this deployment.")
        return
    
    print(f"Found {len(convos)} conversation(s). Starting export...\n")
    
    for idx, c in enumerate(convos, 1):
        cid = c.deployment_conversation_id
        stamp = sanitize_filename(c.created_at or str(time.time()))
        name = sanitize_filename(c.name or f"convo_{cid}")
        
        filename = f"{stamp}__{name}__{cid}.html"
        filepath = OUT / filename
        
        print(f"[{idx}/{len(convos)}] Exporting: {name} ({cid})")
        
        try:
            # Export the conversation
            export = client.export_deployment_conversation(
                deployment_conversation_id=cid
            )
            
            # Get the HTML content
            html = export.conversation_export_html
            
            if not html:
                print(f"  ⚠ Warning: Empty HTML export for conversation {cid}")
                html = f"<html><body><h1>Empty Export</h1><p>Conversation ID: {cid}</p></body></html>"
            
            # Save to file
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)
            
            print(f"  ✓ Saved: {filename}")
        
        except Exception as e:
            print(f"  ✗ Export failed: {e}")
        
        print()
    
    print(f"✅ Done! Exported {len(convos)} conversation(s).")
    print(f"📁 Files saved in: {OUT.resolve()}")


if __name__ == "__main__":
    try:
        export_deployment_conversations()
    except KeyboardInterrupt:
        print("\n\n⚠ Export interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
