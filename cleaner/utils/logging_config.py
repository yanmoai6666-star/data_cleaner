# Logging Configuration
"""
Functions and configuration for setting up logging across the project.
"""

import logging
import os
from datetime import datetime
from typing import Dict, Optional

# Default logging configuration
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO"
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "detailed",
            "level": "DEBUG",
            "filename": "data_cleaner.log"
        }
    },
    "loggers": {
        "data_cleaner": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": True
        }
    }
}

def setup_logging(config: Optional[Dict] = None, log_file_path: Optional[str] = None) -> None:
    """
    Set up logging configuration for the project.
    
    Args:
        config (Dict, optional): Custom logging configuration.
        log_file_path (str, optional): Path to log file.
    """
    # Use provided config or default
    if config is None:
        config = logging_config.copy()
    
    # Update log file path if provided
    if log_file_path:
        # Ensure directory exists
        log_dir = os.path.dirname(log_file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Update file handler
        if "file" in config["handlers"]:
            config["handlers"]["file"]["filename"] = log_file_path
    
    # Configure logging
    logging.config.dictConfig(config)
    
    # Create root logger
    root_logger = logging.getLogger("data_cleaner")
    root_logger.info("Logging setup completed")

def get_logger(name: str = "data_cleaner") -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name (str): Logger name.
        
    Returns:
        logging.Logger: Logger instance.
    """
    return logging.getLogger(name)

def create_rotating_log_handler(log_file_path: str, max_bytes: int = 10485760, backup_count: int = 5) -> logging.handlers.RotatingFileHandler:
    """
    Create a rotating log handler.
    
    Args:
        log_file_path (str): Path to log file.
        max_bytes (int): Maximum size of log file before rotating.
        backup_count (int): Number of backup log files to keep.
        
    Returns:
        logging.handlers.RotatingFileHandler: Rotating log handler.
    """
    # Ensure directory exists
    log_dir = os.path.dirname(log_file_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    return logging.handlers.RotatingFileHandler(
        log_file_path,
        maxBytes=max_bytes,
        backupCount=backup_count
    )

def create_timed_rotating_log_handler(log_file_path: str, when: str = "midnight", interval: int = 1, backup_count: int = 7) -> logging.handlers.TimedRotatingFileHandler:
    """
    Create a timed rotating log handler.
    
    Args:
        log_file_path (str): Path to log file.
        when (str): When to rotate logs (S, M, H, D, midnight, W0-W6).
        interval (int): Interval for log rotation.
        backup_count (int): Number of backup log files to keep.
        
    Returns:
        logging.handlers.TimedRotatingFileHandler: Timed rotating log handler.
    """
    # Ensure directory exists
    log_dir = os.path.dirname(log_file_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    return logging.handlers.TimedRotatingFileHandler(
        log_file_path,
        when=when,
        interval=interval,
        backupCount=backup_count
    )

def configure_logging_levels(levels: Dict[str, str]) -> None:
    """
    Configure logging levels for specific loggers.
    
    Args:
        levels (Dict[str, str]): Dictionary mapping logger names to log levels.
    """
    for logger_name, level in levels.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(level.upper())

def add_file_handler(logger_name: str, log_file_path: str, level: str = "DEBUG", formatter_name: str = "detailed") -> None:
    """
    Add a file handler to a logger.
    
    Args:
        logger_name (str): Logger name.
        log_file_path (str): Path to log file.
        level (str): Log level for the handler.
        formatter_name (str): Formatter name to use.
    """
    logger = logging.getLogger(logger_name)
    
    # Create file handler
    handler = logging.FileHandler(log_file_path)
    handler.setLevel(level.upper())
    
    # Create formatter
    if formatter_name == "detailed":
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s")
    else:
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def add_console_handler(logger_name: str, level: str = "INFO", formatter_name: str = "standard") -> None:
    """
    Add a console handler to a logger.
    
    Args:
        logger_name (str): Logger name.
        level (str): Log level for the handler.
        formatter_name (str): Formatter name to use.
    """
    logger = logging.getLogger(logger_name)
    
    # Create console handler
    handler = logging.StreamHandler()
    handler.setLevel(level.upper())
    
    # Create formatter
    if formatter_name == "detailed":
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s")
    else:
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def create_log_dir(base_dir: str = "./logs") -> str:
    """
    Create a log directory with timestamp.
    
    Args:
        base_dir (str): Base directory for logs.
        
    Returns:
        str: Path to the created log directory.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = os.path.join(base_dir, timestamp)
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    return log_dir
