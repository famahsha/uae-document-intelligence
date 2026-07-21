from dotenv import load_dotenv
import os

# Load all keys from .env file
load_dotenv()

# Get each key and store it
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")

# Check all keys are loaded
print("Google key loaded:", GOOGLE_API_KEY[:10])
print("Tavily key loaded:", TAVILY_API_KEY[:10])
print("Ollama URL:", OLLAMA_BASE_URL)