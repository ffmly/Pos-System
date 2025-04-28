"""
Logging utility for the POS system.
"""

import logging
import os
from datetime import datetime
from config import LOGGING

def setup_logger(name):
    """
    Set up and configure a logger instance.
    
    Args:
        name (str): The name of the logger
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOGGING['level'])
    
    # Create handlers
    file_handler = logging.FileHandler(LOGGING['file'], encoding='utf-8')
    console_handler = logging.StreamHandler()
    
    # Create formatters
    formatter = logging.Formatter(LOGGING['format'])
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def log_error(logger, error, context=None):
    """
    Log an error with context information.
    
    Args:
        logger (logging.Logger): Logger instance
        error (Exception): The error to log
        context (dict, optional): Additional context information
    """
    error_msg = f"Error: {str(error)}"
    if context:
        error_msg += f" | Context: {context}"
    logger.error(error_msg, exc_info=True)

def log_info(logger, message, context=None):
    """
    Log an informational message with context.
    
    Args:
        logger (logging.Logger): Logger instance
        message (str): The message to log
        context (dict, optional): Additional context information
    """
    info_msg = message
    if context:
        info_msg += f" | Context: {context}"
    logger.info(info_msg)

def log_warning(logger, message, context=None):
    """
    Log a warning message with context.
    
    Args:
        logger (logging.Logger): Logger instance
        message (str): The message to log
        context (dict, optional): Additional context information
    """
    warning_msg = message
    if context:
        warning_msg += f" | Context: {context}"
    logger.warning(warning_msg) 