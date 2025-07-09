"""
Configuration management for the BCI Research Assistant.
"""

import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Application settings."""
    
    # API Keys
    anthropic_api_key: str = Field(description="Anthropic API key")
    openai_api_key: Optional[str] = Field(None, description="OpenAI API key")
    huggingface_api_token: Optional[str] = Field(
        None, description="Hugging Face API token"
    )
    
    # Database
    database_url: str = Field(
        "sqlite:///./bci_assistant.db", description="Database URL"
    )
    redis_url: str = Field("redis://localhost:6379", description="Redis URL")
    
    # Application
    app_name: str = Field(
        "BCI Research Assistant", description="Application name"
    )
    app_version: str = Field("1.0.0", description="Application version")
    debug: bool = Field(False, description="Debug mode")
    log_level: str = Field("INFO", description="Log level")
    
    # Server
    host: str = Field("0.0.0.0", description="Server host")
    port: int = Field(8000, description="Server port")
    reload: bool = Field(False, description="Auto-reload on changes")
    
    # Streamlit
    streamlit_port: int = Field(8501, description="Streamlit port")
    
    # File Upload
    max_upload_size: str = Field("100MB", description="Max upload size")
    upload_dir: Path = Field(Path("./uploads"), description="Upload directory")
    
    # Dataset APIs
    openneuro_api_url: str = Field(
        "https://openneuro.org/crn/api", description="OpenNeuro API URL"
    )
    physionet_api_url: str = Field(
        "https://physionet.org/api", description="PhysioNet API URL"
    )
    
    # Security
    secret_key: str = Field(description="Secret key for JWT tokens")
    access_token_expire_minutes: int = Field(
        30, description="Access token expiration time"
    )
    
    # Monitoring
    sentry_dsn: Optional[str] = Field(None, description="Sentry DSN")
    enable_metrics: bool = Field(True, description="Enable metrics collection")
    
    # Cache
    cache_ttl: int = Field(3600, description="Cache TTL in seconds")
    enable_cache: bool = Field(True, description="Enable caching")
    
    # Rate Limiting
    rate_limit_per_minute: int = Field(
        100, description="Rate limit per minute"
    )
    enable_rate_limiting: bool = Field(
        True, description="Enable rate limiting"
    )
    
    @classmethod
    def from_env(cls) -> "Settings":
        """Create settings from environment variables."""
        return cls(
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            huggingface_api_token=os.getenv("HUGGINGFACE_API_TOKEN"),
            database_url=os.getenv("DATABASE_URL", "sqlite:///./bci_assistant.db"),
            redis_url=os.getenv("REDIS_URL", "redis://localhost:6379"),
            app_name=os.getenv("APP_NAME", "BCI Research Assistant"),
            app_version=os.getenv("APP_VERSION", "1.0.0"),
            debug=os.getenv("DEBUG", "False").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8000")),
            reload=os.getenv("RELOAD", "False").lower() == "true",
            streamlit_port=int(os.getenv("STREAMLIT_PORT", "8501")),
            max_upload_size=os.getenv("MAX_UPLOAD_SIZE", "100MB"),
            upload_dir=Path(os.getenv("UPLOAD_DIR", "./uploads")),
            openneuro_api_url=os.getenv(
                "OPENNEURO_API_URL", "https://openneuro.org/crn/api"
            ),
            physionet_api_url=os.getenv(
                "PHYSIONET_API_URL", "https://physionet.org/api"
            ),
            secret_key=os.getenv("SECRET_KEY", ""),
            access_token_expire_minutes=int(
                os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
            ),
            sentry_dsn=os.getenv("SENTRY_DSN"),
            enable_metrics=os.getenv("ENABLE_METRICS", "True").lower() == "true",
            cache_ttl=int(os.getenv("CACHE_TTL", "3600")),
            enable_cache=os.getenv("ENABLE_CACHE", "True").lower() == "true",
            rate_limit_per_minute=int(os.getenv("RATE_LIMIT_PER_MINUTE", "100")),
            enable_rate_limiting=os.getenv(
                "ENABLE_RATE_LIMITING", "True"
            ).lower() == "true",
        )
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings.from_env()


def get_settings() -> Settings:
    """Get application settings."""
    return settings


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


def get_data_dir() -> Path:
    """Get the data directory."""
    return get_project_root() / "data"


def get_logs_dir() -> Path:
    """Get the logs directory."""
    logs_dir = get_project_root() / "logs"
    logs_dir.mkdir(exist_ok=True)
    return logs_dir
