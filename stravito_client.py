import requests
from typing import Dict, Any, List
from config import IHUB_API_KEY, IHUB_BASE_URL

headers = {"x-api-key": IHUB_API_KEY, "Content-Type": "application/json"}

def create_conversation(query: str) -> Dict[str, Any]:
    """Create a new conversation with XXXX API"""
    url = f"{IHUB_BASE_URL}/assistant/conversations"
    r = requests.post(url, headers=headers, json={"message": query})
    r.raise_for_status()
    return r.json()

def extract_sources(response: Dict[str, Any]) -> List[Dict[str, str]]:
    """Extract and format source URLs from iHub response."""
    sources = []
    for src in response.get("sources", []):
        title = src.get("title", "View Source")
        url = src.get("url", "")
        if url:
            sources.append({"title": title, "url": url})
    return sources

def get_message(conversation_id: str, message_id: str) -> Dict[str, Any]:
    """Get a specific message from a conversation"""
    url = f"{IHUB_BASE_URL}/assistant/conversations/{conversation_id}/messages/{message_id}"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    data = r.json()
    data["sources_extracted"] = extract_sources(data)
    return data

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
