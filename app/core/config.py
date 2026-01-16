"""Configuración global del proyecto."""

# Pydantic Settings
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, ValidationError

# Exceptions
from app.core.exceptions import SecretNotFoundError

class Settings(BaseSettings):
    PROJECT_NAME: str = "PUCP API"
    LOG_LEVEL: str = "INFO"

    MODEL_API_KEY: str = Field(default=...)
    MODEL_TEMPERATURE: float = 0.7

    AZURE_SEARCH_SERVICE_NAME: str = Field(default=...)
    AZURE_SEARCH_API_KEY: str = Field(default=...)
    AZURE_SEARCH_INDEX_NAME: str = Field(default=...)
    AZURE_SEARCH_TOP_K: int = 5

    AZURE_FORM_SERVICE_NAME: str = Field(default=...)
    AZURE_FORM_API_KEY: str = Field(default=...)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

try:
    settings = Settings()
except ValidationError as e:
    raise SecretNotFoundError(f"Error de configuración: {e}") from e
