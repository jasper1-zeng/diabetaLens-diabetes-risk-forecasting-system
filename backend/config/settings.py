"""
DiabetaLens Backend Configuration

Main configuration file for the DiabetaLens backend application.
Handles environment variables, API keys, and application settings.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Load environment variables from .env file FIRST
env_path = PROJECT_ROOT / ".env"
if env_path.exists():
    load_dotenv(env_path)

class Settings:
    """Application settings and configuration"""
    
    # Application Settings
    APP_NAME: str = "DiabetaLens API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "localhost")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # Claude AI Configuration
    CLAUDE_API_KEY: Optional[str] = os.getenv("CLAUDE_API_KEY")
    CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
    CLAUDE_MAX_TOKENS: int = int(os.getenv("CLAUDE_MAX_TOKENS", "1000"))
    CLAUDE_TIMEOUT: int = int(os.getenv("CLAUDE_TIMEOUT", "30"))
    
    # Model Paths
    MODELS_DIR: Path = PROJECT_ROOT / "models" / "optimized"
    
    # Data Paths
    DATA_DIR: Path = PROJECT_ROOT / "data"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # CORS Settings
    CORS_ORIGINS: list = [
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    def validate_claude_config(self) -> bool:
        """Validate Claude API configuration"""
        if not self.CLAUDE_API_KEY:
            return False
        return True
    
    def get_cors_origins(self) -> list:
        """Get CORS origins, including any from environment"""
        origins = self.CORS_ORIGINS.copy()
        env_origins = os.getenv("CORS_ORIGINS", "")
        if env_origins:
            origins.extend(env_origins.split(","))
        return origins

# Global settings instance
settings = Settings()

# Environment validation
def validate_environment():
    """Validate required environment variables"""
    errors = []
    
    if not settings.CLAUDE_API_KEY:
        errors.append("CLAUDE_API_KEY environment variable is required")
    
    if not settings.MODELS_DIR.exists():
        errors.append(f"Models directory not found: {settings.MODELS_DIR}")
    
    if errors:
        raise EnvironmentError("\n".join(errors))

if __name__ == "__main__":
    print(f"DiabetaLens Backend Configuration")
    print(f"App: {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"Debug: {settings.DEBUG}")
    print(f"Models Dir: {settings.MODELS_DIR}")
    print(f"Claude Model: {settings.CLAUDE_MODEL}")
    print(f"CORS Origins: {settings.get_cors_origins()}")
    
    try:
        validate_environment()
        print("✅ Configuration validation passed")
    except EnvironmentError as e:
        print(f"❌ Configuration errors:\n{e}") 