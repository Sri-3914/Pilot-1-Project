import requests
from typing import Dict, Any
import json
import time
from config import (
    IHUB_API_KEY, 
    IHUB_BASE_URL,
    STRAVITO_POLL_MAX_RETRIES,
    STRAVITO_POLL_INTERVAL
)

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

def get_message(conversation_id: str, message_id: str, max_retries: int = None, retry_interval: int = None) -> Dict[str, Any]:
    """
    Get a specific message from a conversation, polling until status is COMPLETED
    
    Args:
        conversation_id: The conversation ID
        message_id: The message ID
        max_retries: Maximum number of polling attempts (default: from config, 60 = 2 minutes)
        retry_interval: Seconds to wait between polls (default: from config, 2 seconds)
    
    Returns:
        The completed message data with sources
    """
    # Use config values if not specified
    if max_retries is None:
        max_retries = STRAVITO_POLL_MAX_RETRIES
    if retry_interval is None:
        retry_interval = STRAVITO_POLL_INTERVAL
    url = f"{IHUB_BASE_URL}/assistant/conversations/{conversation_id}/messages/{message_id}"
    print(f"[STRAVITO_CLIENT] Fetching message: conversation={conversation_id}, message={message_id}")
    
    retry_count = 0
    start_time = time.time()
    
    while retry_count < max_retries:
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            response_data = r.json()
            
            # IMPORTANT: The key is 'state' not 'status' in Stravito API
            state = response_data.get('state', '').upper()
            
            print(f"[STRAVITO_CLIENT] Poll #{retry_count + 1}: State = {state}")
            
            if state == 'COMPLETED':
                elapsed = time.time() - start_time
                print(f"[STRAVITO_CLIENT] ✅ Message completed in {elapsed:.1f}s after {retry_count + 1} polls")
                
                # Log source information
                sources = response_data.get('sources', [])
                message_content = response_data.get('message', '')
                print(f"[STRAVITO_CLIENT] Message retrieved:")
                print(f"[STRAVITO_CLIENT]   - Message length: {len(message_content)}")
                print(f"[STRAVITO_CLIENT]   - Sources found: {len(sources)}")
                
                if sources:
                    print(f"[STRAVITO_CLIENT]   - Source details:")
                    for i, source in enumerate(sources):
                        print(f"[STRAVITO_CLIENT]     [{i+1}] ID: {source.get('sourceId', 'N/A')}, Title: {source.get('title', 'N/A')[:50]}")
                else:
                    print(f"[STRAVITO_CLIENT]   - WARNING: No sources in completed response!")
                    print(f"[STRAVITO_CLIENT]   - Response keys: {list(response_data.keys())}")
                
                return response_data
            
            elif state == 'FAILED' or state == 'ERROR':
                print(f"[STRAVITO_CLIENT] ❌ Message processing failed with state: {state}")
                error_msg = response_data.get('error', 'Unknown error')
                print(f"[STRAVITO_CLIENT] Error message: {error_msg}")
                return response_data  # Return even if failed, orchestrator will handle
            
            elif state in ['PROCESSING', 'PENDING', 'IN_PROGRESS', '']:
                # Still processing, wait and retry
                if retry_count == 0:
                    print(f"[STRAVITO_CLIENT] ⏳ Message is processing, will poll every {retry_interval}s...")
                elif retry_count % 10 == 0:  # Log every 10 retries
                    elapsed = time.time() - start_time
                    print(f"[STRAVITO_CLIENT] ⏳ Still waiting... ({elapsed:.0f}s elapsed)")
                
                retry_count += 1
                time.sleep(retry_interval)
            
            else:
                print(f"[STRAVITO_CLIENT] ⚠️  Unknown state: {state}, treating as in-progress")
                retry_count += 1
                time.sleep(retry_interval)
        
        except requests.exceptions.RequestException as e:
            print(f"[STRAVITO_CLIENT] ⚠️  Request error on poll #{retry_count + 1}: {e}")
            retry_count += 1
            if retry_count < max_retries:
                time.sleep(retry_interval)
            else:
                raise
    
    # Timeout reached
    elapsed = time.time() - start_time
    print(f"[STRAVITO_CLIENT] ⏱️  Timeout after {elapsed:.1f}s ({max_retries} polls)")
    print(f"[STRAVITO_CLIENT] ⚠️  Message did not complete, returning last response")
    
    # Return the last response even if not completed
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
