"""
Diagnostic script to troubleshoot startup issues
Run this before starting the FastAPI server to check configuration
"""

import sys
import os
from pathlib import Path

def print_section(title):
    """Print a section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def check_environment_file():
    """Check if .env file exists"""
    print_section("1. Checking .env File")
    
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("✅ .env file found")
        return True
    else:
        print("❌ .env file NOT found")
        if env_example.exists():
            print("ℹ️  Found env.example - copy it to .env and fill in your credentials")
            print("   Command: cp env.example .env")
        return False

def check_environment_variables():
    """Check if all required environment variables are set"""
    print_section("2. Checking Environment Variables")
    
    # Load .env if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ dotenv loaded successfully")
    except ImportError:
        print("❌ python-dotenv not installed")
        print("   Run: pip install python-dotenv")
        return False
    
    required_vars = {
        "IHUB_API_KEY": "Stravito API Key",
        "IHUB_BASE_URL": "Stravito Base URL",
        "AZURE_OPENAI_API_KEY": "Azure OpenAI API Key",
        "AZURE_OPENAI_ENDPOINT": "Azure OpenAI Endpoint",
        "AZURE_OPENAI_DEPLOYMENT_NAME": "Azure OpenAI Deployment Name"
    }
    
    optional_vars = {
        "AZURE_OPENAI_API_VERSION": "Azure OpenAI API Version (defaults to 2024-02-15-preview)"
    }
    
    print("\nRequired Variables:")
    all_present = True
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if "KEY" in var or "SECRET" in var:
                display_value = value[:8] + "..." if len(value) > 8 else "***"
            else:
                display_value = value[:50] + "..." if len(value) > 50 else value
            print(f"  ✅ {var}: {display_value}")
        else:
            print(f"  ❌ {var}: NOT SET ({description})")
            all_present = False
    
    print("\nOptional Variables:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var}: {value}")
        else:
            print(f"  ℹ️  {var}: Using default ({description})")
    
    return all_present

def check_dependencies():
    """Check if all required packages are installed"""
    print_section("3. Checking Dependencies")
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "streamlit",
        "requests",
        "openai",
        "pydantic",
        "python-dotenv"
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - NOT INSTALLED")
            all_installed = False
    
    if not all_installed:
        print("\nInstall missing packages with:")
        print("  pip install -r requirements.txt")
    
    return all_installed

def check_config_import():
    """Try to import config module"""
    print_section("4. Testing Configuration Import")
    
    try:
        import config
        print("✅ Config module imported successfully")
        
        # Check if key values are accessible
        if hasattr(config, 'AZURE_OPENAI_ENDPOINT'):
            print(f"✅ Azure OpenAI Endpoint: {config.AZURE_OPENAI_ENDPOINT[:30]}...")
        if hasattr(config, 'IHUB_BASE_URL'):
            print(f"✅ Stravito Base URL: {config.IHUB_BASE_URL}")
        
        return True
    except ValueError as e:
        print(f"❌ Config import failed: {e}")
        print("\nThis is the error preventing your server from starting!")
        return False
    except Exception as e:
        print(f"❌ Unexpected error importing config: {e}")
        return False

def check_orchestrator_import():
    """Try to import and initialize orchestrator"""
    print_section("5. Testing Orchestrator Import")
    
    try:
        from orchestrator import QueryOrchestrator
        print("✅ Orchestrator module imported successfully")
        
        orchestrator = QueryOrchestrator()
        print("✅ Orchestrator initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Orchestrator import/init failed: {e}")
        print("\nError details:")
        import traceback
        traceback.print_exc()
        return False

def check_fastapi_import():
    """Try to import FastAPI app"""
    print_section("6. Testing FastAPI App Import")
    
    try:
        from main import app
        print("✅ FastAPI app imported successfully")
        print(f"✅ App title: {app.title}")
        print(f"✅ App version: {app.version}")
        return True
    except Exception as e:
        print(f"❌ FastAPI app import failed: {e}")
        print("\nError details:")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all diagnostic checks"""
    print("\n" + "█"*80)
    print("  🔍 STRAVITO QUERY ORCHESTRATOR - STARTUP DIAGNOSTICS")
    print("█"*80)
    
    checks = [
        ("Environment File", check_environment_file),
        ("Environment Variables", check_environment_variables),
        ("Dependencies", check_dependencies),
        ("Config Import", check_config_import),
        ("Orchestrator Import", check_orchestrator_import),
        ("FastAPI App", check_fastapi_import),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error during {name} check: {e}")
            results.append((name, False))
    
    # Summary
    print_section("DIAGNOSTIC SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nChecks Passed: {passed}/{total}\n")
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")
    
    print("\n" + "="*80)
    
    if passed == total:
        print("\n✅ ALL CHECKS PASSED!")
        print("\nYou can now start the server with:")
        print("  python main.py")
        print("  or")
        print("  uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
    else:
        print("\n❌ SOME CHECKS FAILED")
        print("\nPlease fix the issues above before starting the server.")
        print("\nCommon fixes:")
        print("  1. Copy env.example to .env: cp env.example .env")
        print("  2. Edit .env and add your API keys and endpoints")
        print("  3. Install dependencies: pip install -r requirements.txt")
        print("  4. Make sure you're in the correct directory")
    
    print("\n" + "="*80 + "\n")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

