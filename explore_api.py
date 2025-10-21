#!/usr/bin/env python3
"""
Interactive explorer for Abacus.AI API methods

This script lists all available API methods on the ApiClient
and lets you test them interactively to find where your chats are.

Usage:
    export ABACUS_API_KEY="your-api-key"
    python explore_api.py
"""

import os
import sys
from abacusai import ApiClient
import inspect

def main():
    API_KEY = os.environ.get("ABACUS_API_KEY")
    if not API_KEY:
        print("❌ Error: ABACUS_API_KEY environment variable is required")
        sys.exit(1)
    
    client = ApiClient(API_KEY)
    
    print("🔍 Exploring Abacus.AI API Client Methods")
    print("=" * 60)
    print()
    
    # Get all methods that might be related to chats/conversations
    chat_related = []
    conversation_related = []
    message_related = []
    session_related = []
    other_list_methods = []
    
    for name in dir(client):
        if name.startswith('_'):
            continue
        
        attr = getattr(client, name)
        if not callable(attr):
            continue
        
        name_lower = name.lower()
        if 'chat' in name_lower:
            chat_related.append(name)
        elif 'conversation' in name_lower or 'convo' in name_lower:
            conversation_related.append(name)
        elif 'message' in name_lower:
            message_related.append(name)
        elif 'session' in name_lower:
            session_related.append(name)
        elif name.startswith('list_'):
            other_list_methods.append(name)
    
    print("📨 Chat-related methods:")
    for method in sorted(chat_related):
        print(f"  • {method}")
    print()
    
    print("💬 Conversation-related methods:")
    for method in sorted(conversation_related):
        print(f"  • {method}")
    print()
    
    print("✉️  Message-related methods:")
    for method in sorted(message_related):
        print(f"  • {method}")
    print()
    
    print("🔗 Session-related methods:")
    for method in sorted(session_related):
        print(f"  • {method}")
    print()
    
    print("📋 Other list_* methods (might contain chats):")
    for method in sorted(other_list_methods)[:20]:  # Show first 20
        print(f"  • {method}")
    if len(other_list_methods) > 20:
        print(f"  ... and {len(other_list_methods) - 20} more")
    print()
    
    # Try to call some promising methods
    print("=" * 60)
    print("🧪 Testing promising methods...")
    print("=" * 60)
    print()
    
    methods_to_test = [
        'list_chat_sessions',
        'list_conversations',
        'list_chat_messages',
        'list_deployments',
        'list_agents',
        'list_projects',
        'describe_chat_session',
    ]
    
    for method_name in methods_to_test:
        if hasattr(client, method_name):
            method = getattr(client, method_name)
            try:
                # Get method signature
                sig = inspect.signature(method)
                params = list(sig.parameters.keys())
                
                print(f"Testing: {method_name}()")
                print(f"  Parameters: {params if params else 'None'}")
                
                # Try to call with no args if it accepts none
                if not params or all(p in ['kwargs'] for p in params):
                    try:
                        result = method()
                        if result:
                            print(f"  ✓ Returned {len(result)} items")
                            if len(result) > 0:
                                print(f"  First item type: {type(result[0]).__name__}")
                                if hasattr(result[0], '__dict__'):
                                    keys = list(vars(result[0]).keys())[:5]
                                    print(f"  First item fields: {keys}")
                        else:
                            print(f"  ✓ Returned empty list")
                    except TypeError as e:
                        print(f"  ⚠ Needs parameters: {e}")
                else:
                    print(f"  ⚠ Requires parameters: {params}")
                
            except Exception as e:
                print(f"  ✗ Error: {e}")
            
            print()
    
    print("=" * 60)
    print("💡 Next Steps")
    print("=" * 60)
    print("""
1. Check the Abacus.AI web interface:
   - Visit https://abacus.ai
   - Open any chat you want to export
   - Look at the browser URL - it will show the structure
   
2. Common URL patterns:
   - AI Chat: /app/chat_llm/{chat_session_id}
   - Agent Chat: /app/agent/{agent_id}/playground
   - Deployment: /app/deployment/{deployment_id}
   
3. If you find chats in the UI, note the URL pattern and we can
   adapt the export script to use the correct API method.

4. Run the discovery script for more detailed analysis:
   python discover_chats.py
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
