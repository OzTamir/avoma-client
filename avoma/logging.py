import logging
import sys
from typing import Optional


def create_logger(
    name: str = "avoma",
    level: int = logging.INFO,
    format_string: Optional[str] = None,
    handler: Optional[logging.Handler] = None,
) -> logging.Logger:
    """Create a logger for the Avoma client.

    Args:
        name: Logger name (default: "avoma")
        level: Logging level (default: INFO)
        format_string: Optional custom format string
        handler: Optional custom handler

    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        if handler is None:
            handler = logging.StreamHandler(sys.stdout)

        if format_string is None:
            format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        formatter = logging.Formatter(format_string)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(level)
    logger.propagate = False

    return logger


# Default format string that can be imported
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
