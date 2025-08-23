import logging
import os
from pathlib import Path
import sys

# Configure environment variables
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DIR = os.getenv("LOG_DIR", "./logs")  # Default to "./logs" if not set

# Ensure log directory exists
log_path = Path(LOG_DIR)
log_path.mkdir(parents=True, exist_ok=True)

# Create a logger instance
def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger instance with handlers for different log levels.
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # Avoid adding multiple handlers to the same logger
    if not logger.handlers:
        # Create a formatter
        formatter = logging.Formatter(LOG_FORMAT)

        # Info handler
        info_handler = logging.FileHandler(log_path / "info.log")
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(formatter)

        # Error handler
        error_handler = logging.FileHandler(log_path / "error.log")
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)

        # Optionally, add console handler (optional)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(LOG_LEVEL)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        logger.addHandler(info_handler)
        logger.addHandler(error_handler)
        logger.addHandler(console_handler)

    return logger



