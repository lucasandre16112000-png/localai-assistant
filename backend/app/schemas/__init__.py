"""
LocalAI Assistant - Schemas Package
Pydantic schemas for data validation
Author: Lucas Andre S
"""

from .conversation import (
    MessageBase,
    MessageCreate,
    MessageUpdate,
    MessageResponse,
    ConversationBase,
    ConversationCreate,
    ConversationUpdate,
    ConversationResponse,
    ConversationWithMessages,
    ChatRequest,
    ChatResponse,
    StreamChunk,
    SystemPromptBase,
    SystemPromptCreate,
    SystemPromptUpdate,
    SystemPromptResponse,
    AnalyticsResponse,
    DashboardStats,
    ModelInfo,
    ModelList,
    AppSettings,
)

__all__ = [
    "MessageBase",
    "MessageCreate",
    "MessageUpdate",
    "MessageResponse",
    "ConversationBase",
    "ConversationCreate",
    "ConversationUpdate",
    "ConversationResponse",
    "ConversationWithMessages",
    "ChatRequest",
    "ChatResponse",
    "StreamChunk",
    "SystemPromptBase",
    "SystemPromptCreate",
    "SystemPromptUpdate",
    "SystemPromptResponse",
    "AnalyticsResponse",
    "DashboardStats",
    "ModelInfo",
    "ModelList",
    "AppSettings",
]
