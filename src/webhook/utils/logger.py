import logging
from ..config import settings

# Map string log levels to logging constants
LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}

# Get log level from settings, default to INFO if invalid level provided
log_level = LOG_LEVELS.get(settings.LOG_LEVEL.lower(), logging.INFO)

# Configure logging
logging.basicConfig(
    level=log_level,
    format=f"%(asctime)s - [{settings.ENVIRONMENT}] - %(name)s - %(levelname)s - %(message)s",
)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: The name for the logger, typically __name__ from the calling module
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    return logger