#!/usr/bin/env python3
"""
Explore all methods related to projects and chats

Usage:
    export ABACUS_API_KEY="your-key"
    python explore_project_methods.py
"""

import os
import sys
import inspect
from abacusai import ApiClient


def main():
    API_KEY = os.environ.get("ABACUS_API_KEY")
    if not API_KEY:
        print("❌ Error: ABACUS_API_KEY environment variable is required")
        sys.exit(1)
    
    client = ApiClient(API_KEY)
    
    print("🔍 Exploring Project and Chat Methods")
    print("=" * 70)
    print()
    
    # Get a sample project to work with
    projects = client.list_projects()
    if not projects:
        print("No projects found")
        return
    
    sample_project = projects[0]
    project_id = sample_project.project_id
    
    print(f"Using sample project: {sample_project.name} ({project_id})")
    print()
    
    # Find all methods that might get chats from a project
    potential_methods = []
    
    for name in dir(client):
        if name.startswith('_'):
            continue
        
        attr = getattr(client, name)
        if not callable(attr):
            continue
        
        name_lower = name.lower()
        
        # Look for methods that might relate to project content
        if any(keyword in name_lower for keyword in [
            'chat', 'conversation', 'message', 'session',
            'history', 'thread', 'dialog', 'project'
        ]):
            try:
                sig = inspect.signature(attr)
                params = list(sig.parameters.keys())
                potential_methods.append((name, params))
            except:
                potential_methods.append((name, ['?']))
    
    print("📋 Potentially Relevant Methods:")
    print("-" * 70)
    for method_name, params in sorted(potential_methods):
        has_project_id = 'project_id' in params
        marker = " ⭐" if has_project_id else ""
        print(f"{method_name}({', '.join(params)}){marker}")
    
    print()
    print("⭐ = Accepts project_id parameter")
    print()
    
    # Now let's check if there's a way to get chat_session_ids from a project
    print("=" * 70)
    print("🧪 Testing Project-Specific Methods")
    print("=" * 70)
    print()
    
    # Check if project object has any chat-related attributes
    print(f"Project object attributes:")
    proj_attrs = [a for a in dir(sample_project) if not a.startswith('_')]
    for attr in proj_attrs:
        val = getattr(sample_project, attr, None)
        if not callable(val):
            print(f"  {attr}: {type(val).__name__} = {str(val)[:100]}")
    
    print()
    
    # Try get_project to see if it has more details
    try:
        print(f"Testing: client.describe_project(project_id='{project_id}')")
        full_project = client.describe_project(project_id=project_id)
        print("✓ Success! Full project details:")
        full_attrs = [a for a in dir(full_project) if not a.startswith('_')]
        for attr in full_attrs[:20]:  # Show first 20
            val = getattr(full_project, attr, None)
            if not callable(val):
                print(f"  {attr}: {str(val)[:100]}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print()
    print("=" * 70)
    print("💡 Next Steps")
    print("=" * 70)
    print("""
1. Check the Abacus.AI web interface:
   - Do you actually see chats when you log in?
   - What URL do they have? (e.g., /app/chat_llm/xxx)
   
2. If chats exist in the UI but not via API:
   - The web UI might use different endpoints
   - Open browser DevTools (F12) → Network tab
   - Click on a chat and see what API calls are made
   
3. Try creating a test chat:
   - Go to one of your CHAT_LLM projects
   - Start a new chat conversation
   - Run this script again to see if it appears
    """)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
