# utils/logger.py
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logging():
    # Create logs directory
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logs_dir = os.path.join(current_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Clear any existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s UTC - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File Handler (with rotation)
    file_handler = RotatingFileHandler(
        os.path.join(logs_dir, 'search_menu.log'),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5  # Keep 5 backup files
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create a getter function to get the logger
def get_logger():
    return logging.getLogger(__name__)