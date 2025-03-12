import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # ✅ Ensured variable name is correct

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN is not set in .env")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in .env")
