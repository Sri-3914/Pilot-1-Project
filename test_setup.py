#!/usr/bin/env python3
"""
Test script to verify the setup and configuration
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests imported successfully")
    except ImportError as e:
        print(f"❌ Requests import failed: {e}")
        return False
    
    try:
        import openai
        print("✅ OpenAI imported successfully")
    except ImportError as e:
        print(f"❌ OpenAI import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\n🔍 Testing configuration...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = [
            "IHUB_API_KEY", "IHUB_BASE_URL", 
            "AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_DEPLOYMENT_NAME"
        ]
        
        missing_vars = []
        for var in required_vars:
            value = os.getenv(var)
            if not value:
                missing_vars.append(var)
            else:
                # Mask the value for security
                masked_value = value[:8] + "..." if len(value) > 8 else "***"
                print(f"✅ {var}: {masked_value}")
        
        if missing_vars:
            print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_project_files():
    """Test if all required project files exist"""
    print("\n🔍 Testing project files...")
    
    required_files = [
        "main.py",
        "orchestrator.py", 
        "XXXX_client.py",
        "config.py",
        "streamlit_app.py",
        "requirements.txt",
        "env.example"
    ]
    
    missing_files = []
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            missing_files.append(file)
    
    return len(missing_files) == 0

def test_api_connectivity():
    """Test basic API connectivity (if services are running)"""
    print("\n🔍 Testing API connectivity...")
    
    try:
        import requests
        
        # Test FastAPI health endpoint
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ FastAPI backend is running")
                return True
            else:
                print(f"⚠️  FastAPI responded with status {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("⚠️  FastAPI backend is not running (this is OK if you haven't started it yet)")
        except Exception as e:
            print(f"⚠️  FastAPI test failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ API connectivity test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 XXXX Query Orchestrator - Setup Test")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test imports
    if not test_imports():
        all_tests_passed = False
    
    # Test configuration
    if not test_config():
        all_tests_passed = False
    
    # Test project files
    if not test_project_files():
        all_tests_passed = False
    
    # Test API connectivity
    if not test_api_connectivity():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("✅ All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Run: python start_services.py")
        print("2. Open: http://localhost:8501")
    else:
        print("❌ Some tests failed. Please check the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
