from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE_MB: int
    FILE_DEFAULT_CHUNK_SIZE_MB: int
    MONGODB_URL: str
    MONGODB_DB_NAME: str

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    OPENAI_API_KEY: str
    COHERE_API_KEY: str

    OPENAI_API_BASE_URL: str

    LLM_ID: str
    EMBEDDING_MODEL_ID: str
    EMBEDDING_MODEL_SIZE: int

    DEFAULT_MAX_INPUT_CARACTERS: int
    DEFAULT_OUTPUT_MAX_TOKENS: int
    DEFAULT_TEMPERATURE: float

    model_config = SettingsConfigDict(env_file=ENV_FILE)


def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
