import requests
from typing import Dict, Any
import json
from config import IHUB_API_KEY, IHUB_BASE_URL

headers = {"x-api-key": IHUB_API_KEY, "Content-Type": "application/json"}

def create_conversation(query: str) -> Dict[str, Any]:
    """Create a new conversation with Stravito API"""
    url = f"{IHUB_BASE_URL}/assistant/conversations"
    print(f"[STRAVITO_CLIENT] Creating conversation for query: {query[:50]}...")
    r = requests.post(url, headers=headers, json={"message": query})
    r.raise_for_status()
    response_data = r.json()
    print(f"[STRAVITO_CLIENT] Conversation created: ID={response_data.get('conversationId')}")
    return response_data

def get_message(conversation_id: str, message_id: str) -> Dict[str, Any]:
    """Get a specific message from a conversation"""
    url = f"{IHUB_BASE_URL}/assistant/conversations/{conversation_id}/messages/{message_id}"
    print(f"[STRAVITO_CLIENT] Fetching message: conversation={conversation_id}, message={message_id}")
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    response_data = r.json()
    
    # Log source information
    sources = response_data.get('sources', [])
    print(f"[STRAVITO_CLIENT] Message retrieved:")
    print(f"[STRAVITO_CLIENT]   - Content length: {len(response_data.get('content', ''))}")
    print(f"[STRAVITO_CLIENT]   - Sources found: {len(sources)}")
    
    if sources:
        print(f"[STRAVITO_CLIENT]   - Source details:")
        for i, source in enumerate(sources):
            print(f"[STRAVITO_CLIENT]     [{i+1}] ID: {source.get('sourceId', 'N/A')}, Title: {source.get('title', 'N/A')[:50]}")
    else:
        print(f"[STRAVITO_CLIENT]   - WARNING: No sources in response!")
        print(f"[STRAVITO_CLIENT]   - Response keys: {list(response_data.keys())}")
    
    return response_data

def send_followup(conversation_id: str, query: str) -> Dict[str, Any]:
    """Send a follow-up message to an existing conversation"""
    url = f"{IHUB_BASE_URL}/assistant/conversations/{conversation_id}/messages"
    r = requests.post(url, headers=headers, json={"message": query})
    r.raise_for_status()
    return r.json()

def give_feedback(message_id: str, feedback: str = "success") -> Dict[str, Any]:
    """Provide feedback on a message"""
    url = f"{IHUB_BASE_URL}/assistant/messages/{message_id}/feedback"
    r = requests.post(url, headers=headers, json={"feedback": feedback})
    r.raise_for_status()
    return r.json()
