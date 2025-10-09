import requests
from typing import Dict, Any
from config import IHUB_API_KEY, IHUB_BASE_URL

headers = {"x-api-key": IHUB_API_KEY, "Content-Type": "application/json"}

def create_conversation(query: str) -> Dict[str, Any]:
    """Create a new conversation with XXXX API"""
    url = f"{IHUB_BASE_URL}/assistant/conversations"
    r = requests.post(url, headers=headers, json={"message": query})
    r.raise_for_status()
    return r.json()

def get_message(conversation_id: str, message_id: str) -> Dict[str, Any]:
    """Get a specific message from a conversation"""
    url = f"{IHUB_BASE_URL}/assistant/conversations/{conversation_id}/messages/{message_id}"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()

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
