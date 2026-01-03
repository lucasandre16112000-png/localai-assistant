"""
LocalAI Assistant - Memory Model
Generative memory model for storing conversation summaries and patterns
Author: Lucas Andre S & Manus AI
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..core.database import Base


class Memory(Base):
    """
    Generative memory model for storing conversation summaries and user patterns.
    Enables the AI to remember and learn from past interactions.
    """
    __tablename__ = "memories"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    
    # Reference to conversation
    conversation_id = Column(Integer, ForeignKey("conversations.id"), index=True)
    conversation = relationship("Conversation", back_populates="memories")
    
    # Memory type: 'summary', 'pattern', 'preference', 'context'
    memory_type = Column(String, index=True)  # summary, pattern, preference, context
    
    # Memory content
    content = Column(Text)  # The actual memory/summary
    
    # Metadata
    importance_score = Column(Float, default=0.5)  # 0-1 score for importance
    relevance_score = Column(Float, default=0.5)  # 0-1 score for relevance
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    
    # Decay and expiration
    access_count = Column(Integer, default=0)  # How many times this memory was used
    is_active = Column(Boolean, default=True)  # Can be deactivated
    
    # Embeddings for semantic search (stored as JSON)
    embedding = Column(JSON, nullable=True)  # Vector embedding for similarity search
    
    def __repr__(self):
        return f"<Memory(uuid={self.uuid}, type={self.memory_type}, importance={self.importance_score})>"


class MemorySummary(Base):
    """
    Stores summarized versions of conversations for efficient context retrieval.
    """
    __tablename__ = "memory_summaries"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    
    # Reference to conversation
    conversation_id = Column(Integer, ForeignKey("conversations.id"), index=True)
    conversation = relationship("Conversation", back_populates="summaries")
    
    # Summary content
    summary = Column(Text)  # The summary of the conversation
    key_points = Column(JSON)  # List of key points
    entities = Column(JSON)  # Named entities mentioned (people, places, concepts)
    
    # Metadata
    original_message_count = Column(Integer)  # How many messages were summarized
    compression_ratio = Column(Float)  # Original tokens / summary tokens
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<MemorySummary(uuid={self.uuid}, messages={self.original_message_count})>"


class UserPattern(Base):
    """
    Stores learned patterns about user behavior and preferences.
    Enables personalization and better responses.
    """
    __tablename__ = "user_patterns"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    
    # Pattern identifier
    pattern_name = Column(String, index=True)  # e.g., 'prefers_technical_answers'
    pattern_type = Column(String)  # 'preference', 'behavior', 'style', 'topic'
    
    # Pattern details
    description = Column(Text)  # Human-readable description
    pattern_data = Column(JSON)  # Structured pattern data
    
    # Scoring
    confidence_score = Column(Float, default=0.5)  # 0-1 confidence in this pattern
    frequency = Column(Integer, default=1)  # How often this pattern occurs
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_used = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<UserPattern(name={self.pattern_name}, confidence={self.confidence_score})>"


class ContextWindow(Base):
    """
    Manages the context window for efficient token usage.
    Stores relevant context that should be included in prompts.
    """
    __tablename__ = "context_windows"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    
    # Reference to conversation
    conversation_id = Column(Integer, ForeignKey("conversations.id"), index=True)
    conversation = relationship("Conversation", back_populates="context_windows")
    
    # Context content
    context_content = Column(Text)  # The context to include
    context_type = Column(String)  # 'summary', 'recent_messages', 'relevant_memories', 'user_profile'
    
    # Metadata
    token_count = Column(Integer)  # Estimated token count
    relevance_score = Column(Float, default=0.5)  # How relevant this context is
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<ContextWindow(uuid={self.uuid}, type={self.context_type}, tokens={self.token_count})>"
