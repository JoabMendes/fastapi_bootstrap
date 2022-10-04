import logging
import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, BaseSettings

log = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    prefix_api_v1: str = "/api/v1"
    environment: str = "dev"
    app_name: str
    app_description: str
    log_level: str = "INFO"

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> BaseSettings:
    settings = Settings()
    log.info("Loading config settings from the environment...")
    log.info(f"Running on {settings.environment} environment.")
    return settings


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOG_FORMAT: str = (
        "%(levelprefix)s | %(asctime)s | %(module)s | %(message)s"
    )

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "": {
            "handlers": ["default"],
            "level": get_settings().log_level,
            "propagate": True,
        },
    }
