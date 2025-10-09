#!/usr/bin/env python3
"""
Test script to debug XXXX API connection
"""

import requests
import json
from config import IHUB_API_KEY, IHUB_BASE_URL

def test_XXXX_api():
    """Test XXXX API connection and endpoints"""
    print("🧪 Testing XXXX API Connection")
    print("=" * 50)
    
    # Check configuration
    print(f"📋 Configuration:")
    print(f"  Base URL: {IHUB_BASE_URL}")
    print(f"  API Key: {IHUB_API_KEY[:10]}..." if IHUB_API_KEY else "  API Key: NOT SET")
    print()
    
    if not IHUB_API_KEY or not IHUB_BASE_URL:
        print("❌ Missing API configuration!")
        return
    
    headers = {"x-api-key": IHUB_API_KEY, "Content-Type": "application/json"}
    
    # Test 1: Simple health check
    print("🔍 Test 1: Health Check")
    try:
        health_url = f"{IHUB_BASE_URL}/health"
        print(f"  URL: {health_url}")
        response = requests.get(health_url, headers=headers, timeout=10)
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.text[:200]}...")
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
    print()
    
    # Test 2: Create conversation
    print("🔍 Test 2: Create Conversation")
    try:
        conv_url = f"{IHUB_BASE_URL}/assistant/conversations"
        print(f"  URL: {conv_url}")
        print(f"  Headers: {headers}")
        
        test_query = "What is artificial intelligence?"
        payload = {"query": test_query}
        print(f"  Payload: {payload}")
        
        response = requests.post(conv_url, headers=headers, json=payload, timeout=30)
        print(f"  Status: {response.status_code}")
        print(f"  Response Headers: {dict(response.headers)}")
        print(f"  Response Body: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Success! Conversation ID: {data.get('conversation_id')}")
            return data
        else:
            print(f"  ❌ Failed with status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Request Error: {str(e)}")
    except Exception as e:
        print(f"  ❌ General Error: {str(e)}")
    print()
    
    # Test 3: Check API documentation endpoint
    print("🔍 Test 3: API Documentation")
    try:
        docs_url = f"{IHUB_BASE_URL}/docs"
        print(f"  URL: {docs_url}")
        response = requests.get(docs_url, timeout=10)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            print(f"  ✅ API docs available")
        else:
            print(f"  ⚠️ API docs not available")
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
    print()

if __name__ == "__main__":
    test_XXXX_api()
