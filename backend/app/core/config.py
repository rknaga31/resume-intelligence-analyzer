"""
Application configuration using Pydantic BaseSettings.

Reads from environment variables / .env file.
"""
from __future__ import annotations

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed, validated application settings read from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # -------------------------------------------------------------------------
    # Application
    # -------------------------------------------------------------------------
    app_name: str = "Resume Intelligence Analyzer"
    app_version: str = "1.0.0"
    app_env: str = "development"
    debug: bool = False
    log_level: str = "INFO"

    # -------------------------------------------------------------------------
    # API Server
    # -------------------------------------------------------------------------
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 1
    allowed_origins: str = "http://localhost:3000"

    # -------------------------------------------------------------------------
    # Database
    # -------------------------------------------------------------------------
    database_url: str = "sqlite+aiosqlite:///./resume_intelligence.db"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "resume_intelligence"
    postgres_user: str = "ria_user"
    postgres_password: str = "changeme"

    # -------------------------------------------------------------------------
    # Security
    # -------------------------------------------------------------------------
    app_secret_key: str = "change-me-in-production-use-openssl-rand-hex-32"
    jwt_secret_key: str = "change-me-in-production-use-openssl-rand-hex-32"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # -------------------------------------------------------------------------
    # File Upload
    # -------------------------------------------------------------------------
    upload_dir: str = "./uploads"
    max_upload_size_mb: int = 10
    allowed_resume_types: str = "pdf,docx,doc,txt"

    # -------------------------------------------------------------------------
    # LLM Providers
    # -------------------------------------------------------------------------
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-5-haiku-20241022"
    google_api_key: str = ""
    google_gemini_model: str = "gemini-2.0-flash-exp"

    # Default to rule-based fallback if no LLM key is configured
    llm_provider: str = "fallback"  # openai | anthropic | gemini | fallback

    # -------------------------------------------------------------------------
    # Embeddings
    # -------------------------------------------------------------------------
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_cache_dir: str = "./models"

    # -------------------------------------------------------------------------
    # Rate Limiting
    # -------------------------------------------------------------------------
    rate_limit_per_minute: int = 30

    @field_validator("app_env")
    @classmethod
    def validate_env(cls, v: str) -> str:
        """Validate the app environment value."""
        allowed = {"development", "staging", "production", "test"}
        if v not in allowed:
            raise ValueError(f"app_env must be one of {allowed}")
        return v

    @property
    def cors_origins(self) -> list[str]:
        """Parse comma-separated CORS origins into a list."""
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]

    @property
    def allowed_mime_types(self) -> set[str]:
        """Return a set of allowed MIME types for file uploads."""
        return {
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword",
            "text/plain",
        }

    @property
    def max_upload_size_bytes(self) -> int:
        """Convert MB to bytes."""
        return self.max_upload_size_mb * 1024 * 1024

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings singleton."""
    return Settings()
