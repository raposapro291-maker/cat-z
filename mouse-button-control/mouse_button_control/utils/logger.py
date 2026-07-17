"""Logging system for the application."""

import logging
import os
from pathlib import Path
from datetime import datetime
import coloredlogs


class Logger:
    """Logger utility class."""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not Logger._initialized:
            self.setup_logging()
            Logger._initialized = True

    @staticmethod
    def setup_logging(log_level=logging.INFO):
        """Configure logging for the application."""
        logs_dir = Path.home() / ".config" / "mouse-button-control" / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)

        log_file = logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"

        # Create logger
        logger = logging.getLogger("mouse_button_control")
        logger.setLevel(log_level)

        # Create formatters
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_formatter = coloredlogs.ColoredFormatter(
            "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )

        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        return logger

    @staticmethod
    def get_logger(name=None):
        """Get a logger instance."""
        return logging.getLogger(name or "mouse_button_control")
