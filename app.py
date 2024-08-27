import asyncio
import logging

from fastapi import FastAPI
from uvicorn import Config, Server
from pydantic_settings import BaseSettings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AppSettings(BaseSettings):
    service_name: str = "llm-tracing"
    version: str = "0.1.0"
    log_level: str = "INFO"
    rest_port: int = 8080

app_settings = AppSettings()

app = FastAPI(title=app_settings.service_name)


@app.get("/")
@app.get("/health/")
async def health() -> dict:
    logger.info("Health check")
    return {"status": "up"}


async def serve():
    logger.info(
        f"Starting {app_settings.service_name} {app_settings.version} REST server on port {app_settings.rest_port}"
    )
    rest_server = Server(
        Config(
            app=app,
            host="0.0.0.0",
            port=app_settings.rest_port,
            loop="asyncio",
            workers=1,
            # log_config=LOGGING,
            log_level="warning",
        )
    )

    await rest_server.serve()

if __name__ == "__main__":
    asyncio.run(serve())