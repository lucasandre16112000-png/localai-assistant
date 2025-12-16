"""
LocalAI Assistant - Pydantic Schemas
Data validation and serialization schemas
Author: Lucas Andre S
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


# ============================================
# Message Schemas
# ============================================

class MessageBase(BaseModel):
    """Base schema for messages."""
    role: str = Field(..., description="Message role: user, assistant, or system")
    content: str = Field(..., description="Message content")


class MessageCreate(MessageBase):
    """Schema for creating a new message."""
    pass


class MessageUpdate(BaseModel):
    """Schema for updating a message."""
    content: str = Field(..., description="Updated message content")


class MessageResponse(MessageBase):
    """Schema for message response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    uuid: str
    conversation_id: int
    model: Optional[str] = None
    tokens: int = 0
    generation_time: Optional[float] = None
    is_edited: bool = False
    created_at: datetime
    updated_at: datetime


# ============================================
# Conversation Schemas
# ============================================

class ConversationBase(BaseModel):
    """Base schema for conversations."""
    title: str = Field(default="New Conversation", max_length=255)
    model: str = Field(default="dolphin-mistral")
    system_prompt: Optional[str] = None


class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation."""
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    top_k: int = Field(default=40, ge=1, le=100)
    max_tokens: int = Field(default=2048, ge=1, le=32768)


class ConversationUpdate(BaseModel):
    """Schema for updating a conversation."""
    title: Optional[str] = Field(None, max_length=255)
    model: Optional[str] = None
    system_prompt: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0)
    top_k: Optional[int] = Field(None, ge=1, le=100)
    max_tokens: Optional[int] = Field(None, ge=1, le=32768)
    is_pinned: Optional[bool] = None
    is_archived: Optional[bool] = None
    tags: Optional[Dict[str, Any]] = None


class ConversationResponse(ConversationBase):
    """Schema for conversation response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    uuid: str
    temperature: float
    top_p: float
    top_k: int
    max_tokens: int
    is_pinned: bool
    is_archived: bool
    tags: Optional[Dict[str, Any]] = None
    message_count: int
    total_tokens: int
    created_at: datetime
    updated_at: datetime


class ConversationWithMessages(ConversationResponse):
    """Schema for conversation with messages."""
    messages: List[MessageResponse] = []


# ============================================
# Chat Schemas
# ============================================

class ChatRequest(BaseModel):
    """Schema for chat completion request."""
    conversation_id: Optional[str] = None
    message: str = Field(..., min_length=1)
    model: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0)
    top_k: Optional[int] = Field(None, ge=1, le=100)
    max_tokens: Optional[int] = Field(None, ge=1, le=32768)
    stream: bool = False


class ChatResponse(BaseModel):
    """Schema for chat completion response."""
    conversation_id: str
    message: MessageResponse
    model: str
    tokens: int
    generation_time: float


class StreamChunk(BaseModel):
    """Schema for streaming response chunk."""
    content: str
    done: bool = False
    tokens: Optional[int] = None


# ============================================
# System Prompt Schemas
# ============================================

class SystemPromptBase(BaseModel):
    """Base schema for system prompts."""
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    content: str


class SystemPromptCreate(SystemPromptBase):
    """Schema for creating a system prompt."""
    is_default: bool = False


class SystemPromptUpdate(BaseModel):
    """Schema for updating a system prompt."""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    content: Optional[str] = None
    is_default: Optional[bool] = None


class SystemPromptResponse(SystemPromptBase):
    """Schema for system prompt response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_default: bool
    created_at: datetime
    updated_at: datetime


# ============================================
# Analytics Schemas
# ============================================

class AnalyticsResponse(BaseModel):
    """Schema for analytics response."""
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())
    
    total_conversations: int
    total_messages: int
    total_tokens: int
    model_usage: Dict[str, int]
    avg_response_time: Optional[float]
    date: datetime


class DashboardStats(BaseModel):
    """Schema for dashboard statistics."""
    total_conversations: int
    total_messages: int
    total_tokens: int
    active_model: str
    avg_response_time: float
    conversations_today: int
    messages_today: int
    tokens_today: int


# ============================================
# Model Schemas
# ============================================

class ModelInfo(BaseModel):
    """Schema for model information."""
    name: str
    modified_at: Optional[str] = None
    size: Optional[int] = None
    digest: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class ModelList(BaseModel):
    """Schema for list of models."""
    models: List[ModelInfo]


# ============================================
# Settings Schemas
# ============================================

class AppSettings(BaseModel):
    """Schema for application settings."""
    theme: str = "dark"
    language: str = "en"
    default_model: str = "dolphin-mistral"
    default_temperature: float = 0.7
    default_top_p: float = 0.9
    default_top_k: int = 40
    default_max_tokens: int = 2048
    auto_save: bool = True
    stream_responses: bool = True
