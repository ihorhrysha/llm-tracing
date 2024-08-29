
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    service_name: str = "llm-tracing"
    version: str = "0.1.0"
    log_level: str = "INFO"
    rest_port: int = 8080
    openai_api_key: str = "fake_key"
    db_uri: str = "sqlite:///Chinook.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")