"""
LocalAI Assistant - Routers Package
API endpoint routers
Author: Lucas Andre S
"""

from .conversations import router as conversations_router
from .chat import router as chat_router
from .models import router as models_router
from .prompts import router as prompts_router

__all__ = [
    "conversations_router",
    "chat_router",
    "models_router",
    "prompts_router",
]
