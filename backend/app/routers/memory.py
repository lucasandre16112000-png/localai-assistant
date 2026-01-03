"""
LocalAI Assistant - Memory API
API endpoints for generative memory management
Author: Lucas Andre S & Manus AI
"""

import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_db
from ..schemas.memory import (
    MemoryCreate, MemoryUpdate, MemoryResponse,
    MemorySummaryCreate, MemorySummaryResponse,
    UserPatternCreate, UserPatternUpdate, UserPatternResponse,
    ContextWindowCreate, ContextWindowResponse,
    MemoryRetrievalRequest, MemoryRetrievalResponse,
    GenerativeMemoryState
)
from ..services.memory_service import MemoryService
from ..models.conversation import Conversation
from ..models.memory import Memory, MemorySummary, UserPattern, ContextWindow
from sqlalchemy import select

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/memory", tags=["memory"])
memory_service = MemoryService()


@router.post("/memories", response_model=MemoryResponse)
async def create_memory(
    conversation_id: int,
    memory_data: MemoryCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new memory entry for a conversation."""
    try:
        # Verify conversation exists
        result = await db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        memory = await memory_service.create_memory(db, conversation_id, memory_data)
        return memory
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/memories/{memory_uuid}", response_model=MemoryResponse)
async def get_memory(
    memory_uuid: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific memory by UUID."""
    try:
        memory = await memory_service.get_memory(db, memory_uuid)
        if not memory:
            raise HTTPException(status_code=404, detail="Memory not found")
        return memory
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}/memories", response_model=dict)
async def get_conversation_memories(
    conversation_id: int,
    memory_type: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get all memories for a conversation."""
    try:
        # Verify conversation exists
        result = await db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        memories = await memory_service.get_conversation_memories(
            db, conversation_id, memory_type, limit
        )
        return {
            "memories": memories,
            "total_count": len(memories),
            "conversation_id": conversation_id
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation memories: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/memories/{memory_uuid}", response_model=MemoryResponse)
async def update_memory(
    memory_uuid: str,
    memory_data: MemoryUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a memory entry."""
    try:
        memory = await memory_service.update_memory(db, memory_uuid, memory_data)
        if not memory:
            raise HTTPException(status_code=404, detail="Memory not found")
        return memory
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/memories/{memory_uuid}")
async def delete_memory(
    memory_uuid: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete a memory entry."""
    try:
        success = await memory_service.delete_memory(db, memory_uuid)
        if not success:
            raise HTTPException(status_code=404, detail="Memory not found")
        return {"status": "success", "message": "Memory deleted"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== SUMMARIES ====================

@router.post("/conversations/{conversation_id}/summarize", response_model=MemorySummaryResponse)
async def generate_summary(
    conversation_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Generate a summary of a conversation."""
    try:
        summary = await memory_service.generate_conversation_summary(db, conversation_id)
        if not summary:
            raise HTTPException(status_code=400, detail="Conversation too short to summarize")
        return summary
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}/summary", response_model=Optional[MemorySummaryResponse])
async def get_latest_summary(
    conversation_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get the latest summary for a conversation."""
    try:
        summary = await memory_service.get_latest_summary(db, conversation_id)
        return summary
    except Exception as e:
        logger.error(f"Error getting summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== USER PATTERNS ====================

@router.post("/patterns", response_model=UserPatternResponse)
async def learn_pattern(
    pattern_data: UserPatternCreate,
    db: AsyncSession = Depends(get_db)
):
    """Learn and store a user pattern."""
    try:
        pattern = await memory_service.learn_user_pattern(db, pattern_data)
        return pattern
    except Exception as e:
        logger.error(f"Error learning pattern: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patterns", response_model=dict)
async def get_user_patterns(
    min_confidence: float = Query(0.3, ge=0, le=1),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """Get all learned user patterns."""
    try:
        patterns = await memory_service.get_user_patterns(db, min_confidence, limit)
        return {
            "patterns": patterns,
            "total_count": len(patterns)
        }
    except Exception as e:
        logger.error(f"Error getting patterns: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conversations/{conversation_id}/detect-preferences", response_model=dict)
async def detect_preferences(
    conversation_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Detect user preferences from conversation history."""
    try:
        patterns = await memory_service.detect_user_preferences(db, conversation_id)
        return {
            "detected_patterns": patterns,
            "total_count": len(patterns)
        }
    except Exception as e:
        logger.error(f"Error detecting preferences: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== CONTEXT MANAGEMENT ====================

@router.post("/context-windows", response_model=ContextWindowResponse)
async def create_context_window(
    conversation_id: int,
    context_data: ContextWindowCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a context window for efficient token usage."""
    try:
        # Verify conversation exists
        result = await db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        context = await memory_service.create_context_window(db, conversation_id, context_data)
        return context
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating context window: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}/optimal-context")
async def get_optimal_context(
    conversation_id: int,
    max_tokens: int = Query(2048, ge=256, le=4096),
    db: AsyncSession = Depends(get_db)
):
    """Get the optimal context for a conversation within token limit."""
    try:
        context = await memory_service.get_optimal_context(db, conversation_id, max_tokens)
        return {
            "context": context,
            "conversation_id": conversation_id,
            "max_tokens": max_tokens
        }
    except Exception as e:
        logger.error(f"Error getting optimal context: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== MEMORY STATE ====================

@router.get("/conversations/{conversation_id}/state", response_model=GenerativeMemoryState)
async def get_memory_state(
    conversation_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get the current generative memory state for a conversation."""
    try:
        # Get all memories
        memories = await memory_service.get_conversation_memories(db, conversation_id, limit=100)
        active_memories = [m for m in memories if m.is_active]
        
        # Get summary
        summary = await memory_service.get_latest_summary(db, conversation_id)
        
        # Get patterns
        patterns = await memory_service.get_user_patterns(db, min_confidence=0.3, limit=10)
        
        # Get context windows
        result = await db.execute(
            select(ContextWindow).where(ContextWindow.conversation_id == conversation_id)
        )
        context_windows = result.scalars().all()
        
        return GenerativeMemoryState(
            conversation_id=conversation_id,
            total_memories=len(memories),
            active_memories=len(active_memories),
            summaries=[summary] if summary else [],
            user_patterns=patterns,
            context_windows=context_windows,
            last_updated=datetime.utcnow()
        )
    except Exception as e:
        logger.error(f"Error getting memory state: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== MAINTENANCE ====================

@router.post("/cleanup")
async def cleanup_old_memories(
    days_old: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db)
):
    """Clean up old memories that are no longer relevant."""
    try:
        count = await memory_service.cleanup_old_memories(db, days_old)
        return {
            "status": "success",
            "cleaned_count": count,
            "message": f"Cleaned up {count} old memories"
        }
    except Exception as e:
        logger.error(f"Error cleaning up memories: {e}")
        raise HTTPException(status_code=500, detail=str(e))


from datetime import datetime
