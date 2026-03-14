import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# App Configuration
PAGE_TITLE = "Financed Emissions & Climate Risk Advisor"
PAGE_ICON = "🌍"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
