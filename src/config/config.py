from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    model_config = SettingsConfigDict(env_file=ENV_FILE)


def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
