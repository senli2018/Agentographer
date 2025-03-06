"""
Logger Utility Module

Provides unified logging configuration and access interface.
Supports both console output and file recording methods.
"""
import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from app.core.config import settings

# Log directory
LOG_DIR = Path(__file__).parent.parent.parent / "logs"

# Ensure log directory exists
if not LOG_DIR.exists():
    os.makedirs(LOG_DIR)

# Configure root logger
def setup_logging():
    """
    Set up logging system
    
    Configure log format, level and output targets
    """
    # Get log level
    log_level_str = settings.LOG_LEVEL.upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    
    # Clear existing handlers
    root_logger = logging.getLogger()
    if root_logger.handlers:
        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    
    # Create file handler - INFO level
    info_file_handler = RotatingFileHandler(
        LOG_DIR / "info.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    info_file_handler.setFormatter(formatter)
    info_file_handler.setLevel(logging.INFO)
    
    # Create file handler - ERROR level
    error_file_handler = RotatingFileHandler(
        LOG_DIR / "error.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    error_file_handler.setFormatter(formatter)
    error_file_handler.setLevel(logging.ERROR)
    
    # Add handlers to root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(info_file_handler)
    root_logger.addHandler(error_file_handler)
    
    # Set root logger level
    root_logger.setLevel(log_level)
    
    # Log startup information
    root_logger.info(f"Logging system initialized with level: {log_level_str}")
    root_logger.info(f"Log files location: {LOG_DIR}")
    
    return root_logger

# Initialize logging system
logger = setup_logging()

def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance
    
    Args:
        name: Logger name, usually the module name
        
    Returns:
        Configured logger instance
    """
    if name:
        return logging.getLogger(name)
    return logger 