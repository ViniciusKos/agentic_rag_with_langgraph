import os
from dotenv import load_dotenv
from typing import Optional
from pydantic_settings import BaseSettings

def load_config():
    """Load configuration from environment variables"""
    load_dotenv()
    
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "user_agent": os.getenv("USER_AGENT", "scoras-academy-app")
    }

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    USER_AGENT: Optional[str] = "scoras-academy-app"