import logging
import logging.config
import os

LOG_DIR = os.path.join(os.path.dirname(__file__), "../logs")
os.makedirs(LOG_DIR, exist_ok=True)  # Crée le répertoire des logs s'il n'existe pas

LOG_FILE = os.path.join(LOG_DIR, "application.log")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - [%(levelname)s] - %(filename)s:%(lineno)d - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOG_FILE,
            "formatter": "detailed",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"],
    },
}


def configure_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
