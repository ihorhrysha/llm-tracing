from logging import config
from typing import Any, Dict

from pythonjsonlogger.jsonlogger import JsonFormatter

from settings import app_settings

def config_logger() -> None:
    config.dictConfig(LOGGING)


class CustomJsonFormatter(JsonFormatter):
    def process_log_record(self, log_record: Dict[str, Any]):
        log_record["level"] = log_record.pop("levelname")
        log_record["service"] = app_settings.service_name
        log_record["version"] = app_settings.version

        return log_record


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": CustomJsonFormatter,
            "format": "%(name)s %(asctime)s %(levelname)s %(module)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": app_settings.log_level,
            "class": "logging.StreamHandler",
            "formatter": "json",
            # "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "root": {
            "level": app_settings.log_level,
            "handlers": ["console"],
        },
    },
}

