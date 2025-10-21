#!/usr/bin/env python3
"""
Bulk export all Abacus.AI Chat Sessions (Data Science Copilot chats)

Usage:
    export ABACUS_API_KEY="your-api-key-here"
    python bulk_export_ai_chat.py

Output:
    Creates abacus_ai_chat_exports/ directory with:
    - {timestamp}__{name}__{id}.html - Human-readable chat history
    - {timestamp}__{name}__{id}.json - Full fidelity data
"""

import os
import sys
import json
import pathlib
import time

# Add debugging for segfault issues
print("Initializing bulk export script...", file=sys.stderr)
print(f"Python version: {sys.version}", file=sys.stderr)

try:
    from abacusai import ApiClient
    print("✓ ApiClient imported successfully", file=sys.stderr)
except Exception as e:
    print(f"✗ Failed to import ApiClient: {e}", file=sys.stderr)
    sys.exit(1)


def sanitize_filename(name: str, max_len: int = 80) -> str:
    """Sanitize a string for use in filenames"""
    return name.replace("/", "_").replace(" ", "_").replace(":", "-")[:max_len]


def export_chat_sessions():
    # Configuration
    API_KEY = os.environ.get("ABACUS_API_KEY")
    if not API_KEY:
        raise ValueError("ABACUS_API_KEY environment variable is required")
    
    OUT = pathlib.Path("abacus_ai_chat_exports")
    OUT.mkdir(parents=True, exist_ok=True)
    
    # Initialize client
    print("Initializing API client...", file=sys.stderr)
    try:
        client = ApiClient(API_KEY)
        print("✓ Client initialized", file=sys.stderr)
    except Exception as e:
        print(f"✗ Client initialization failed: {e}", file=sys.stderr)
        raise
    
    print("Fetching chat sessions...")
    
    # 1) List all chat sessions
    sessions = client.list_chat_sessions()
    
    if not sessions:
        print("No chat sessions found.")
        return
    
    print(f"Found {len(sessions)} chat session(s). Starting export...\n")
    
    for idx, s in enumerate(sessions, 1):
        sid = s.chat_session_id
        name = sanitize_filename(s.name or f"session_{sid}")
        stamp = sanitize_filename(s.created_at or str(time.time()))
        base = OUT / f"{stamp}__{name}__{sid}"
        
        print(f"[{idx}/{len(sessions)}] Exporting: {name} ({sid})")
        
        # 2a) Save raw JSON (full fidelity)
        try:
            with open(f"{base}.json", "w", encoding="utf-8") as f:
                json.dump(s.to_dict(), f, ensure_ascii=False, indent=2)
            print(f"  ✓ Saved JSON: {base}.json")
        except Exception as e:
            print(f"  ✗ JSON export failed: {e}")
        
        # 2b) Export to HTML
        try:
            # Try the official export endpoint first
            resp = client.export_chat_session(chat_session_id=sid)
            
            if isinstance(resp, (bytes, bytearray)):
                html = resp.decode("utf-8", errors="ignore")
                with open(f"{base}.html", "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"  ✓ Saved HTML: {base}.html")
            elif isinstance(resp, str):
                with open(f"{base}.html", "w", encoding="utf-8") as f:
                    f.write(resp)
                print(f"  ✓ Saved HTML: {base}.html")
            else:
                # Fallback: render from get_chat_session()
                raise RuntimeError("SDK returned non-body response; using fallback.")
        
        except Exception as e:
            print(f"  ⚠ Export API failed ({e}), using fallback renderer...")
            try:
                # Fallback: render HTML from raw chat data
                full = client.get_chat_session(chat_session_id=sid)
                msgs = full.chat_history or []
                
                html_parts = [
                    "<!DOCTYPE html>",
                    "<html><head><meta charset='utf-8'>",
                    f"<title>{name}</title>",
                    "<style>",
                    "body { font-family: sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; }",
                    "h1 { color: #333; }",
                    "h3 { color: #666; margin-top: 20px; }",
                    "pre { background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }",
                    "hr { border: none; border-top: 1px solid #ddd; margin: 20px 0; }",
                    "</style></head><body>",
                    f"<h1>{name}</h1>",
                    f"<p><em>Session ID: {sid}</em></p>",
                    f"<p><em>Created: {s.created_at or 'Unknown'}</em></p>",
                    "<hr/>"
                ]
                
                for m in msgs:
                    who = m.role or "user"
                    # Handle text that may be in various formats
                    if hasattr(m, 'text') and m.text:
                        if isinstance(m.text, list):
                            text = "\n".join(
                                t.get("text", "") if isinstance(t, dict) else str(t) 
                                for t in m.text
                            )
                        else:
                            text = str(m.text)
                    else:
                        text = str(m)
                    
                    html_parts.append(f"<h3>{who.upper()}</h3>")
                    html_parts.append(f"<pre>{text}</pre>")
                    html_parts.append("<hr/>")
                
                html_parts.append("</body></html>")
                
                with open(f"{base}.html", "w", encoding="utf-8") as f:
                    f.write("\n".join(html_parts))
                print(f"  ✓ Saved HTML (fallback): {base}.html")
            
            except Exception as fallback_error:
                print(f"  ✗ Fallback HTML render failed: {fallback_error}")
        
        print()
    
    print(f"✅ Done! Exported {len(sessions)} session(s).")
    print(f"📁 Files saved in: {OUT.resolve()}")


if __name__ == "__main__":
    try:
        export_chat_sessions()
    except KeyboardInterrupt:
        print("\n\n⚠ Export interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
