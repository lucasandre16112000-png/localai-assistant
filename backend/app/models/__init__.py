"""
LocalAI Assistant - Models Package
Database models for the application
Author: Lucas Andre S
"""

from .conversation import Conversation, Message, SystemPrompt, Analytics

__all__ = ["Conversation", "Message", "SystemPrompt", "Analytics"]
