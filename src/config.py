from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    USER_AGENT: str = "langgraph_scoras_academy"

def load_config() -> dict:
    settings =  Settings()
    return settings

if __name__ == "__main__":
    config = load_config()
    print(config)