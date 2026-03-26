"""
Configuration and initialization for the Langchain Tool Agent
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Config:
    """Configuration class for the Langchain Tool Agent"""
    
    # Database configuration
    DATABASE_PATH: str = os.getenv("DB_PATH", "agent.db")
    DATABASE_TIMEOUT: int = 30
    
    # File operations configuration
    BASE_FILE_PATH: str = os.getenv("BASE_FILE_PATH", "./data")
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS: list = [".txt", ".json", ".csv", ".log", ".md"]
    
    # Ollama LLM configuration
    LLM_PROVIDER: str = "ollama"  # Using Ollama instead of OpenAI
    LLM_MODEL: str = os.getenv("MODEL_NAME", "functiongemma:latest")
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "1.0"))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "2000"))
    OPENAI_API_KEY: Optional[str] = None  # Not used with Ollama
    
    # Agent configuration
    AGENT_VERBOSE: bool = os.getenv("AGENT_VERBOSE", "true").lower() == "true"
    AGENT_HANDLE_PARSING_ERRORS: bool = True
    
    # Math operations configuration
    MATH_PRECISION: int = 10  # Decimal places
    ALLOW_COMPLEX_NUMBERS: bool = False
    
    @classmethod
    def initialize(cls, **kwargs):
        """Initialize configuration with custom values"""
        for key, value in kwargs.items():
            if hasattr(cls, key):
                setattr(cls, key, value)
                logger.info(f"Configuration: {key} = {value}")
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get all configuration as a dictionary"""
        return {
            key: getattr(cls, key) for key in dir(cls)
            if not key.startswith('_') and key.isupper()
        }
    
    @classmethod
    def print_config(cls):
        """Print current configuration"""
        print("\n" + "="*60)
        print("AGENT CONFIGURATION")
        print("="*60)
        
        config = cls.get_config()
        for key, value in sorted(config.items()):
            print(f"{key}: {value}")
        
        print("="*60 + "\n")


def initialize_agent_environment():
    """Initialize the agent environment"""
    logger.info("Initializing agent environment...")
    
    # Create base directories
    Path(Config.BASE_FILE_PATH).mkdir(parents=True, exist_ok=True)
    Path(Config.DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Agent environment initialized")
    logger.info(f"  - Base file path: {Config.BASE_FILE_PATH}")
    logger.info(f"  - Database path: {Config.DATABASE_PATH}")


def validate_file_path(file_path: str) -> bool:
    """Validate if a file path is allowed"""
    path = Path(file_path)
    
    # Check if file extension is allowed
    if path.suffix and path.suffix not in Config.ALLOWED_EXTENSIONS:
        logger.warning(f"File extension {path.suffix} not in allowed list")
        return False
    
    return True


def validate_file_size(file_path: str) -> bool:
    """Validate if a file size is within limits"""
    try:
        size = Path(file_path).stat().st_size
        if size > Config.MAX_FILE_SIZE:
            logger.warning(f"File size {size} exceeds maximum {Config.MAX_FILE_SIZE}")
            return False
        return True
    except FileNotFoundError:
        return True  # File doesn't exist yet


if __name__ == "__main__":
    # Display configuration
    Config.print_config()
    
    # Initialize environment
    initialize_agent_environment()
