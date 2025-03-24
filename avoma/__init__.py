"""
Avoma API Client

A Python client for the Avoma API (https://api.avoma.com/docs).
"""

from .client import AvomaClient
from .logging import create_logger, DEFAULT_FORMAT

__version__ = "0.1.0"
__all__ = ["AvomaClient", "create_logger", "DEFAULT_FORMAT"]
