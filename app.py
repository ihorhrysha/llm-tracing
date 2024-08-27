import asyncio
import logging
from typing import Annotated

from fastapi import FastAPI, Query
from uvicorn import Config, Server
from settings import AppSettings
from qa_controller import QAController, QAService
from langchain_openai import ChatOpenAI
from logger import config_logger
from langchain_community.utilities import SQLDatabase

# Primitive dependency graph
app_settings = AppSettings()
config_logger(min_log_level=app_settings.log_level)

app = FastAPI(title=app_settings.service_name)
logger = logging.getLogger(__name__)

llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key=app_settings.openai_api_key)
db = SQLDatabase.from_uri(app_settings.db_uri)

qa_service = QAService(llm=llm, db=db)
qa_controller = QAController(qa_service=qa_service)

# Rest API
@app.get("/")
@app.get("/health/")
async def health() -> dict:
    logger.info("Health check")
    return {"status": "up"}

@app.get("/ask/")
async def ask(question: Annotated[str | None, Query(min_length=10, examples=["How many employees are there?"])]) -> dict:
    """
    Returns question about data in DB

    Examples:
    * How many employees are there?
    * list the most popular albums
    """
    
    answer = qa_controller.answer(question)
    logger.info(str(answer))
    return {"answer": answer}


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
            log_level="warning",
        )
    )

    await rest_server.serve()

if __name__ == "__main__":
    asyncio.run(serve())