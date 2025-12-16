"""
LocalAI Assistant - Core Package
Core configuration and utilities
Author: Lucas Andre S
"""

from .config import settings, get_settings
from .database import Base, get_db, init_db, close_db

__all__ = ["settings", "get_settings", "Base", "get_db", "init_db", "close_db"]
