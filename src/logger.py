from logging import config

from pythonjsonlogger.jsonlogger import JsonFormatter

def config_logger(min_log_level:str) -> None:
    config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": JsonFormatter,
                    "format": "%(name)s %(asctime)s %(levelname)s %(module)s %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "level": min_log_level,
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                "root": {
                    "level": min_log_level,
                    "handlers": ["console"],
                },
            },
        }
    )



