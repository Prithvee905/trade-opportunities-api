import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Store configuration parameters."""
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    API_SECRET_KEY: str = os.getenv("API_SECRET_KEY", "appscrip-secret-key")

config = Config()
