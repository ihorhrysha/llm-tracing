# These are the necessary import declarations
import logging
from random import randint

from opentelemetry import trace
from opentelemetry import metrics
from flask import Flask, request, jsonify
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase

from logger import config_logger
from settings import AppSettings
from qa_controller import QAController, QAService


# Primitive dependency graph
app_settings = AppSettings()
# config_logger(min_log_level=app_settings.log_level)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key=app_settings.openai_api_key)
db = SQLDatabase.from_uri(app_settings.db_uri)

qa_service = QAService(llm=llm, db=db)
qa_controller = QAController(qa_service=qa_service)



# custom tracer and meter
tracer = trace.get_tracer("diceroller.tracer")
meter = metrics.get_meter("diceroller.meter")
roll_counter = meter.create_counter(
    "dice.rolls",
    description="The number of rolls by roll value",
)

@app.route("/rolldice")
def roll_dice():
    def roll():
        return randint(1, 6)

    # This creates a new span that's the child of the current one
    with tracer.start_as_current_span("roll") as roll_span:
        player = request.args.get('player', default = None, type = str)
        result = str(roll())
        roll_span.set_attribute("roll.value", result)
        # This adds 1 to the counter for the given roll value
        roll_counter.add(1, {"roll.value": result})
        if player:
            logger.warning("{} is rolling the dice: {}", player, result)
        else:
            logger.warning("Anonymous player is rolling the dice: %s", result)
        return result


@app.route("/ask")
def ask():
    """
    Returns question about data in DB

    Examples:
        How many employees are there?
        http://localhost:8080/ask?question=How%20many%20employees%20are%20there?
    """
    question = request.args.get('question', default=None, type=str)
    if not question:
        return jsonify({"error": "Question parameter is required"}), 400

    logger.info(f"Asking question about data in DB: {question}")
    answer = qa_controller.answer(question)
    logger.warning(f"Answer: {answer}")
    return jsonify({"answer": answer})
