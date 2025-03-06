import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    """Application configuration class"""
    # Application configuration
    APP_NAME: str = os.getenv("APP_NAME", "Agentographer")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Server configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    RELOAD: bool = os.getenv("RELOAD", "True").lower() == "true"
    
    # Dify configuration
    DIFY_API_KEY: str = os.getenv("DIFY_API_KEY", "")
    DIFY_API_URL: str = os.getenv("DIFY_API_URL", "")
    
    # WebSocket configuration
    WEBSOCKET_HEARTBEAT_INTERVAL: int = int(os.getenv("WEBSOCKET_HEARTBEAT_INTERVAL", "30"))
    WEBSOCKET_HEARTBEAT_TIMEOUT: int = int(os.getenv("WEBSOCKET_HEARTBEAT_TIMEOUT", "120"))
    WEBSOCKET_CONNECTION_TIMEOUT: int = int(os.getenv("WEBSOCKET_CONNECTION_TIMEOUT", "10"))
    WEBSOCKET_RECEIVE_TIMEOUT: int = int(os.getenv("WEBSOCKET_RECEIVE_TIMEOUT", "60"))
    
    # Mock mode configuration
    MOCK_MODE: bool = os.getenv("MOCK_MODE", "False").lower() == "true"
    
    # Other configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings instance
settings = Settings()

# Export settings instance for easy import by other modules
def get_settings() -> Settings:
    """Get application configuration"""
    return settings 