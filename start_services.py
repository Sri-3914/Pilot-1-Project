#!/usr/bin/env python3
"""
Startup script to run both FastAPI backend and Streamlit frontend
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import fastapi
        import streamlit
        import requests
        import openai
        from dotenv import load_dotenv
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        print("Please copy env.example to .env and fill in your credentials")
        return False
    
    # Load and check environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        "IHUB_API_KEY", "IHUB_BASE_URL", 
        "AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_DEPLOYMENT_NAME"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please update your .env file with the required credentials")
        return False
    
    print("✅ Environment configuration is valid")
    return True

def start_fastapi():
    """Start the FastAPI backend"""
    print("🚀 Starting FastAPI backend...")
    try:
        # Start FastAPI server
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
        print("✅ FastAPI backend started on http://localhost:8000")
        return process
    except Exception as e:
        print(f"❌ Failed to start FastAPI: {e}")
        return None

def start_streamlit():
    """Start the Streamlit frontend"""
    print("🚀 Starting Streamlit frontend...")
    try:
        # Wait a moment for FastAPI to start
        time.sleep(3)
        
        # Start Streamlit
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
        print("✅ Streamlit frontend started on http://localhost:8501")
        return process
    except Exception as e:
        print(f"❌ Failed to start Streamlit: {e}")
        return None

def main():
    """Main startup function"""
    print("🔍 Stravito Query Orchestrator Startup")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment
    if not check_env_file():
        sys.exit(1)
    
    print("\n🚀 Starting services...")
    
    # Start FastAPI
    fastapi_process = start_fastapi()
    if not fastapi_process:
        sys.exit(1)
    
    # Start Streamlit
    streamlit_process = start_streamlit()
    if not streamlit_process:
        fastapi_process.terminate()
        sys.exit(1)
    
    print("\n✅ Both services are running!")
    print("📊 FastAPI Backend: http://localhost:8000")
    print("📊 API Documentation: http://localhost:8000/docs")
    print("🖥️  Streamlit UI: http://localhost:8501")
    print("\nPress Ctrl+C to stop both services")
    
    try:
        # Wait for both processes
        while True:
            time.sleep(1)
            if fastapi_process.poll() is not None:
                print("❌ FastAPI process stopped unexpectedly")
                break
            if streamlit_process.poll() is not None:
                print("❌ Streamlit process stopped unexpectedly")
                break
    except KeyboardInterrupt:
        print("\n🛑 Shutting down services...")
        fastapi_process.terminate()
        streamlit_process.terminate()
        print("✅ Services stopped")

if __name__ == "__main__":
    main()
