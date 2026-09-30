from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE_MB: int

    model_config = SettingsConfigDict(env_file=ENV_FILE)


def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
