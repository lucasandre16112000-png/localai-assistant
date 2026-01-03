"""
LocalAI Assistant - Memory Schemas
Pydantic schemas for memory-related API requests and responses
Author: Lucas Andre S & Manus AI
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class MemoryCreate(BaseModel):
    """Schema for creating a new memory."""
    memory_type: str  # 'summary', 'pattern', 'preference', 'context'
    content: str
    importance_score: float = Field(default=0.5, ge=0, le=1)
    relevance_score: float = Field(default=0.5, ge=0, le=1)
    embedding: Optional[List[float]] = None


class MemoryUpdate(BaseModel):
    """Schema for updating a memory."""
    content: Optional[str] = None
    importance_score: Optional[float] = Field(None, ge=0, le=1)
    relevance_score: Optional[float] = Field(None, ge=0, le=1)
    is_active: Optional[bool] = None


class MemoryResponse(BaseModel):
    """Schema for memory response."""
    id: int
    uuid: str
    conversation_id: int
    memory_type: str
    content: str
    importance_score: float
    relevance_score: float
    access_count: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_accessed: datetime
    
    class Config:
        from_attributes = True


class MemorySummaryCreate(BaseModel):
    """Schema for creating a memory summary."""
    summary: str
    key_points: List[str]
    entities: Dict[str, List[str]]
    original_message_count: int


class MemorySummaryResponse(BaseModel):
    """Schema for memory summary response."""
    id: int
    uuid: str
    conversation_id: int
    summary: str
    key_points: List[str]
    entities: Dict[str, List[str]]
    original_message_count: int
    compression_ratio: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserPatternCreate(BaseModel):
    """Schema for creating a user pattern."""
    pattern_name: str
    pattern_type: str  # 'preference', 'behavior', 'style', 'topic'
    description: str
    pattern_data: Dict[str, Any]
    confidence_score: float = Field(default=0.5, ge=0, le=1)


class UserPatternUpdate(BaseModel):
    """Schema for updating a user pattern."""
    description: Optional[str] = None
    pattern_data: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = Field(None, ge=0, le=1)
    frequency: Optional[int] = None


class UserPatternResponse(BaseModel):
    """Schema for user pattern response."""
    id: int
    uuid: str
    pattern_name: str
    pattern_type: str
    description: str
    pattern_data: Dict[str, Any]
    confidence_score: float
    frequency: int
    created_at: datetime
    updated_at: datetime
    last_used: datetime
    
    class Config:
        from_attributes = True


class ContextWindowCreate(BaseModel):
    """Schema for creating a context window."""
    context_content: str
    context_type: str  # 'summary', 'recent_messages', 'relevant_memories', 'user_profile'
    token_count: int
    relevance_score: float = Field(default=0.5, ge=0, le=1)


class ContextWindowResponse(BaseModel):
    """Schema for context window response."""
    id: int
    uuid: str
    conversation_id: int
    context_content: str
    context_type: str
    token_count: int
    relevance_score: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MemoryRetrievalRequest(BaseModel):
    """Schema for retrieving relevant memories."""
    query: str
    memory_type: Optional[str] = None
    limit: int = Field(default=5, ge=1, le=20)
    min_relevance: float = Field(default=0.3, ge=0, le=1)


class MemoryRetrievalResponse(BaseModel):
    """Schema for memory retrieval response."""
    memories: List[MemoryResponse]
    total_count: int
    search_query: str
    retrieval_time_ms: float


class GenerativeMemoryState(BaseModel):
    """Schema for the current generative memory state."""
    conversation_id: int
    total_memories: int
    active_memories: int
    summaries: List[MemorySummaryResponse]
    user_patterns: List[UserPatternResponse]
    context_windows: List[ContextWindowResponse]
    last_updated: datetime
