"""
LocalAI Assistant - Memory Service
Service for managing generative memory, summaries, and user patterns
Author: Lucas Andre S & Manus AI
"""

import json
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy import select, and_, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.memory import Memory, MemorySummary, UserPattern, ContextWindow
from ..models.conversation import Conversation, Message
from ..schemas.memory import (
    MemoryCreate, MemoryUpdate, MemorySummaryCreate,
    UserPatternCreate, UserPatternUpdate, ContextWindowCreate,
    MemoryRetrievalRequest
)
from ..services.llm_service import LLMService

logger = logging.getLogger(__name__)


class MemoryService:
    """Service for managing generative memory and learning patterns."""
    
    def __init__(self):
        self.llm_service = LLMService()
        self.max_context_tokens = 2048
        self.summary_threshold = 10  # Summarize after 10 messages
    
    # ==================== MEMORY MANAGEMENT ====================
    
    async def create_memory(
        self,
        db: AsyncSession,
        conversation_id: int,
        memory_data: MemoryCreate
    ) -> Memory:
        """Create a new memory entry."""
        memory = Memory(
            conversation_id=conversation_id,
            memory_type=memory_data.memory_type,
            content=memory_data.content,
            importance_score=memory_data.importance_score,
            relevance_score=memory_data.relevance_score,
            embedding=memory_data.embedding,
        )
        db.add(memory)
        await db.commit()
        await db.refresh(memory)
        logger.info(f"Created memory: {memory.uuid}")
        return memory
    
    async def get_memory(self, db: AsyncSession, memory_uuid: str) -> Optional[Memory]:
        """Get a memory by UUID."""
        result = await db.execute(
            select(Memory).where(Memory.uuid == memory_uuid)
        )
        memory = result.scalar_one_or_none()
        if memory:
            memory.access_count += 1
            memory.last_accessed = datetime.utcnow()
            await db.commit()
        return memory
    
    async def get_conversation_memories(
        self,
        db: AsyncSession,
        conversation_id: int,
        memory_type: Optional[str] = None,
        limit: int = 20
    ) -> List[Memory]:
        """Get all memories for a conversation."""
        query = select(Memory).where(
            and_(
                Memory.conversation_id == conversation_id,
                Memory.is_active == True
            )
        )
        
        if memory_type:
            query = query.where(Memory.memory_type == memory_type)
        
        query = query.order_by(desc(Memory.importance_score)).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def update_memory(
        self,
        db: AsyncSession,
        memory_uuid: str,
        memory_data: MemoryUpdate
    ) -> Optional[Memory]:
        """Update a memory entry."""
        result = await db.execute(
            select(Memory).where(Memory.uuid == memory_uuid)
        )
        memory = result.scalar_one_or_none()
        
        if not memory:
            return None
        
        update_data = memory_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(memory, field, value)
        
        memory.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(memory)
        return memory
    
    async def delete_memory(self, db: AsyncSession, memory_uuid: str) -> bool:
        """Delete a memory (soft delete by setting is_active to False)."""
        result = await db.execute(
            select(Memory).where(Memory.uuid == memory_uuid)
        )
        memory = result.scalar_one_or_none()
        
        if not memory:
            return False
        
        memory.is_active = False
        memory.updated_at = datetime.utcnow()
        await db.commit()
        return True
    
    # ==================== SUMMARY GENERATION ====================
    
    async def generate_conversation_summary(
        self,
        db: AsyncSession,
        conversation_id: int
    ) -> Optional[MemorySummary]:
        """Generate a summary of a conversation."""
        # Get conversation and messages
        result = await db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            return None
        
        # Get all messages
        msg_result = await db.execute(
            select(Message).where(Message.conversation_id == conversation_id)
        )
        messages = msg_result.scalars().all()
        
        if len(messages) < self.summary_threshold:
            return None  # Don't summarize short conversations
        
        # Build conversation text
        conversation_text = "\n".join([
            f"{msg.role}: {msg.content}" for msg in messages
        ])
        
        # Generate summary using LLM
        summary_prompt = f"""Summarize this conversation in 3-4 sentences, highlighting the main topics and key points:

{conversation_text}

Provide:
1. A concise summary
2. Key points (as a JSON list)
3. Named entities mentioned (people, places, concepts as a JSON object)"""
        
        response = await self.llm_service.generate(
            prompt=summary_prompt,
            model="dolphin-mistral",
            temperature=0.3,
            max_tokens=500
        )
        
        summary_content = response.get("response", "")
        
        # Parse the response to extract structured data
        key_points = self._extract_key_points(summary_content)
        entities = self._extract_entities(summary_content)
        
        # Calculate compression ratio
        original_tokens = sum(len(msg.content.split()) for msg in messages)
        summary_tokens = len(summary_content.split())
        compression_ratio = original_tokens / max(summary_tokens, 1)
        
        # Create summary
        summary = MemorySummary(
            conversation_id=conversation_id,
            summary=summary_content,
            key_points=key_points,
            entities=entities,
            original_message_count=len(messages),
            compression_ratio=compression_ratio
        )
        
        db.add(summary)
        await db.commit()
        await db.refresh(summary)
        logger.info(f"Generated summary for conversation {conversation_id}")
        return summary
    
    async def get_latest_summary(
        self,
        db: AsyncSession,
        conversation_id: int
    ) -> Optional[MemorySummary]:
        """Get the latest summary for a conversation."""
        result = await db.execute(
            select(MemorySummary)
            .where(MemorySummary.conversation_id == conversation_id)
            .order_by(desc(MemorySummary.created_at))
            .limit(1)
        )
        return result.scalar_one_or_none()
    
    # ==================== PATTERN LEARNING ====================
    
    async def learn_user_pattern(
        self,
        db: AsyncSession,
        pattern_data: UserPatternCreate
    ) -> UserPattern:
        """Learn and store a user pattern."""
        # Check if pattern already exists
        result = await db.execute(
            select(UserPattern).where(
                UserPattern.pattern_name == pattern_data.pattern_name
            )
        )
        existing_pattern = result.scalar_one_or_none()
        
        if existing_pattern:
            # Update existing pattern
            existing_pattern.frequency += 1
            existing_pattern.confidence_score = min(
                existing_pattern.confidence_score + 0.05, 1.0
            )
            existing_pattern.last_used = datetime.utcnow()
            existing_pattern.updated_at = datetime.utcnow()
            await db.commit()
            await db.refresh(existing_pattern)
            return existing_pattern
        
        # Create new pattern
        pattern = UserPattern(
            pattern_name=pattern_data.pattern_name,
            pattern_type=pattern_data.pattern_type,
            description=pattern_data.description,
            pattern_data=pattern_data.pattern_data,
            confidence_score=pattern_data.confidence_score,
            frequency=1
        )
        db.add(pattern)
        await db.commit()
        await db.refresh(pattern)
        logger.info(f"Learned pattern: {pattern.pattern_name}")
        return pattern
    
    async def get_user_patterns(
        self,
        db: AsyncSession,
        min_confidence: float = 0.3,
        limit: int = 10
    ) -> List[UserPattern]:
        """Get all learned user patterns above confidence threshold."""
        result = await db.execute(
            select(UserPattern)
            .where(UserPattern.confidence_score >= min_confidence)
            .order_by(desc(UserPattern.confidence_score))
            .limit(limit)
        )
        return result.scalars().all()
    
    async def detect_user_preferences(
        self,
        db: AsyncSession,
        conversation_id: int
    ) -> List[UserPattern]:
        """Detect user preferences from conversation history."""
        # Get all messages
        msg_result = await db.execute(
            select(Message).where(Message.conversation_id == conversation_id)
        )
        messages = msg_result.scalars().all()
        
        if not messages:
            return []
        
        # Analyze messages for patterns
        patterns = []
        
        # Check for technical preference
        technical_keywords = ['code', 'python', 'javascript', 'algorithm', 'database', 'api']
        technical_count = sum(
            1 for msg in messages
            if msg.role == 'user' and any(kw in msg.content.lower() for kw in technical_keywords)
        )
        
        if technical_count > len([m for m in messages if m.role == 'user']) * 0.3:
            pattern_data = await self.learn_user_pattern(
                db,
                UserPatternCreate(
                    pattern_name="prefers_technical_answers",
                    pattern_type="preference",
                    description="User prefers technical and detailed explanations",
                    pattern_data={"technical_keyword_ratio": technical_count / max(len([m for m in messages if m.role == 'user']), 1)},
                    confidence_score=0.7
                )
            )
            patterns.append(pattern_data)
        
        return patterns
    
    # ==================== CONTEXT MANAGEMENT ====================
    
    async def create_context_window(
        self,
        db: AsyncSession,
        conversation_id: int,
        context_data: ContextWindowCreate
    ) -> ContextWindow:
        """Create a context window for efficient token usage."""
        context = ContextWindow(
            conversation_id=conversation_id,
            context_content=context_data.context_content,
            context_type=context_data.context_type,
            token_count=context_data.token_count,
            relevance_score=context_data.relevance_score
        )
        db.add(context)
        await db.commit()
        await db.refresh(context)
        return context
    
    async def get_optimal_context(
        self,
        db: AsyncSession,
        conversation_id: int,
        max_tokens: int = 2048
    ) -> str:
        """Get the optimal context for a conversation within token limit."""
        # Get recent messages
        msg_result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(desc(Message.created_at))
            .limit(10)
        )
        recent_messages = list(reversed(msg_result.scalars().all()))
        
        # Get latest summary
        summary = await self.get_latest_summary(db, conversation_id)
        
        # Get relevant memories
        memories = await self.get_conversation_memories(
            db, conversation_id, limit=5
        )
        
        # Get user patterns
        patterns = await self.get_user_patterns(db, min_confidence=0.5, limit=3)
        
        # Build context
        context_parts = []
        
        # Add summary if available
        if summary:
            context_parts.append(f"Previous conversation summary:\n{summary.summary}\n")
        
        # Add recent messages
        recent_text = "\n".join([
            f"{msg.role}: {msg.content}" for msg in recent_messages[-3:]
        ])
        context_parts.append(f"Recent messages:\n{recent_text}\n")
        
        # Add relevant memories
        if memories:
            memory_text = "\n".join([
                f"- {mem.content}" for mem in memories
            ])
            context_parts.append(f"Relevant context:\n{memory_text}\n")
        
        # Add user patterns
        if patterns:
            pattern_text = "\n".join([
                f"- {pat.description}" for pat in patterns
            ])
            context_parts.append(f"User preferences:\n{pattern_text}\n")
        
        return "\n".join(context_parts)
    
    # ==================== HELPER METHODS ====================
    
    def _extract_key_points(self, text: str) -> List[str]:
        """Extract key points from summary text."""
        # Simple extraction - can be improved with NLP
        lines = text.split('\n')
        key_points = [line.strip() for line in lines if line.strip() and len(line.strip()) > 10]
        return key_points[:5]  # Return top 5
    
    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities from text."""
        # Simplified entity extraction
        return {
            "topics": [],
            "people": [],
            "places": [],
            "concepts": []
        }
    
    async def cleanup_old_memories(
        self,
        db: AsyncSession,
        days_old: int = 30
    ) -> int:
        """Clean up old memories that are no longer relevant."""
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        
        result = await db.execute(
            select(Memory).where(
                and_(
                    Memory.updated_at < cutoff_date,
                    Memory.access_count < 2,
                    Memory.importance_score < 0.3
                )
            )
        )
        old_memories = result.scalars().all()
        
        count = 0
        for memory in old_memories:
            memory.is_active = False
            count += 1
        
        await db.commit()
        logger.info(f"Cleaned up {count} old memories")
        return count
