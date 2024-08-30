from random import randint
from flask import Flask, request, jsonify
import logging

from opentelemetry import trace
from opentelemetry import metrics

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    
@app.route("/")
def status():
    return jsonify({"status": "alive"})