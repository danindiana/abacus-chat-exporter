#!/usr/bin/env python3
import os
from abacusai import ApiClient

client = ApiClient(os.environ['ABACUS_API_KEY'])

print('Testing list_chat_sessions with different parameters...\n')

# Try default
sessions1 = client.list_chat_sessions()
print(f'list_chat_sessions(): {len(sessions1) if sessions1 else 0} sessions')

# Try with most_recent_per_project=False
try:
    sessions2 = client.list_chat_sessions(most_recent_per_project=False)
    print(f'list_chat_sessions(most_recent_per_project=False): {len(sessions2) if sessions2 else 0} sessions')
except Exception as e:
    print(f'most_recent_per_project=False: Error - {e}')

# Try with most_recent_per_project=True
try:
    sessions3 = client.list_chat_sessions(most_recent_per_project=True)
    print(f'list_chat_sessions(most_recent_per_project=True): {len(sessions3) if sessions3 else 0} sessions')
except Exception as e:
    print(f'most_recent_per_project=True: Error - {e}')

print('\n' + '='*70)
print('CONCLUSION:')
print('='*70)
print("""
If all methods return 0 sessions, this means:
1. You haven't created any chat sessions yet in Abacus.AI
2. OR the chats are in a different part of the UI

Please visit https://abacus.AI and check:
- Do you see any chats in the web interface?
- If yes, what URL do they have when you click on them?
- If no, you need to create a chat first before you can export
""")
