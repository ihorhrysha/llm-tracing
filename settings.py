
from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    service_name: str = "llm-tracing"
    version: str = "0.1.0"
    log_level: str = "INFO"
    rest_port: int = 8080

app_settings = AppSettings()