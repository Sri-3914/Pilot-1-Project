import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Stravito API Configuration
IHUB_API_KEY = os.getenv("IHUB_API_KEY")
IHUB_BASE_URL = os.getenv("IHUB_BASE_URL")

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

# Polling Configuration for Stravito API
# Maximum time to wait for message completion (in seconds)
STRAVITO_POLL_MAX_RETRIES = int(os.getenv("STRAVITO_POLL_MAX_RETRIES", "60"))  # 60 polls = 2 minutes
STRAVITO_POLL_INTERVAL = int(os.getenv("STRAVITO_POLL_INTERVAL", "2"))  # Poll every 2 seconds

# Validate required environment variables
required_vars = [
    "IHUB_API_KEY", "IHUB_BASE_URL", 
    "AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_DEPLOYMENT_NAME"
]

missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
