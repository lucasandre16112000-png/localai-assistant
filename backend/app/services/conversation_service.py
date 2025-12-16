"""
LocalAI Assistant - Conversation Service
Business logic for conversation management
Author: Lucas Andre S
"""

import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.conversation import Conversation, Message, Analytics
from ..schemas.conversation import (
    ConversationCreate,
    ConversationUpdate,
    MessageCreate,
    DashboardStats,
)


class ConversationService:
    """
    Service class for conversation operations.
    Handles CRUD operations and business logic for conversations and messages.
    """
    
    async def create_conversation(
        self,
        db: AsyncSession,
        data: ConversationCreate
    ) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(
            uuid=str(uuid.uuid4()),
            title=data.title,
            model=data.model,
            system_prompt=data.system_prompt,
            temperature=data.temperature,
            top_p=data.top_p,
            top_k=data.top_k,
            max_tokens=data.max_tokens,
        )
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
        return conversation
    
    async def get_conversation(
        self,
        db: AsyncSession,
        conversation_uuid: str
    ) -> Optional[Conversation]:
        """Get a conversation by UUID."""
        result = await db.execute(
            select(Conversation)
            .where(Conversation.uuid == conversation_uuid)
            .options(selectinload(Conversation.messages))
        )
        return result.scalar_one_or_none()
    
    async def get_conversation_by_id(
        self,
        db: AsyncSession,
        conversation_id: int
    ) -> Optional[Conversation]:
        """Get a conversation by ID."""
        result = await db.execute(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .options(selectinload(Conversation.messages))
        )
        return result.scalar_one_or_none()
    
    async def list_conversations(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 50,
        include_archived: bool = False
    ) -> List[Conversation]:
        """List all conversations with pagination."""
        query = select(Conversation).order_by(desc(Conversation.updated_at))
        
        if not include_archived:
            query = query.where(Conversation.is_archived == False)
        
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def update_conversation(
        self,
        db: AsyncSession,
        conversation_uuid: str,
        data: ConversationUpdate
    ) -> Optional[Conversation]:
        """Update a conversation."""
        conversation = await self.get_conversation(db, conversation_uuid)
        if not conversation:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(conversation, field, value)
        
        conversation.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(conversation)
        return conversation
    
    async def delete_conversation(
        self,
        db: AsyncSession,
        conversation_uuid: str
    ) -> bool:
        """Delete a conversation and all its messages."""
        conversation = await self.get_conversation(db, conversation_uuid)
        if not conversation:
            return False
        
        await db.delete(conversation)
        await db.commit()
        return True
    
    async def add_message(
        self,
        db: AsyncSession,
        conversation_id: int,
        role: str,
        content: str,
        model: Optional[str] = None,
        tokens: int = 0,
        generation_time: Optional[float] = None
    ) -> Message:
        """Add a message to a conversation."""
        message = Message(
            uuid=str(uuid.uuid4()),
            conversation_id=conversation_id,
            role=role,
            content=content,
            model=model,
            tokens=tokens,
            generation_time=generation_time,
        )
        db.add(message)
        
        # Update conversation stats
        result = await db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalar_one_or_none()
        if conversation:
            conversation.message_count += 1
            conversation.total_tokens += tokens
            conversation.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(message)
        return message
    
    async def update_message(
        self,
        db: AsyncSession,
        message_uuid: str,
        content: str
    ) -> Optional[Message]:
        """Update a message content."""
        result = await db.execute(
            select(Message).where(Message.uuid == message_uuid)
        )
        message = result.scalar_one_or_none()
        
        if not message:
            return None
        
        if not message.is_edited:
            message.original_content = message.content
        
        message.content = content
        message.is_edited = True
        message.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(message)
        return message
    
    async def delete_message(
        self,
        db: AsyncSession,
        message_uuid: str
    ) -> bool:
        """Delete a message."""
        result = await db.execute(
            select(Message).where(Message.uuid == message_uuid)
        )
        message = result.scalar_one_or_none()
        
        if not message:
            return False
        
        # Update conversation stats
        result = await db.execute(
            select(Conversation).where(Conversation.id == message.conversation_id)
        )
        conversation = result.scalar_one_or_none()
        if conversation:
            conversation.message_count -= 1
            conversation.total_tokens -= message.tokens
        
        await db.delete(message)
        await db.commit()
        return True
    
    async def get_messages(
        self,
        db: AsyncSession,
        conversation_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Message]:
        """Get messages for a conversation."""
        result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def search_conversations(
        self,
        db: AsyncSession,
        query: str,
        limit: int = 20
    ) -> List[Conversation]:
        """Search conversations by title or message content."""
        # Search in conversation titles
        result = await db.execute(
            select(Conversation)
            .where(Conversation.title.ilike(f"%{query}%"))
            .order_by(desc(Conversation.updated_at))
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_dashboard_stats(self, db: AsyncSession) -> DashboardStats:
        """Get dashboard statistics."""
        # Total conversations
        total_conv = await db.execute(select(func.count(Conversation.id)))
        total_conversations = total_conv.scalar() or 0
        
        # Total messages
        total_msg = await db.execute(select(func.count(Message.id)))
        total_messages = total_msg.scalar() or 0
        
        # Total tokens
        total_tok = await db.execute(select(func.sum(Conversation.total_tokens)))
        total_tokens = total_tok.scalar() or 0
        
        # Average response time
        avg_time = await db.execute(
            select(func.avg(Message.generation_time))
            .where(Message.role == "assistant")
            .where(Message.generation_time.isnot(None))
        )
        avg_response_time = avg_time.scalar() or 0.0
        
        # Today's stats
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        conv_today = await db.execute(
            select(func.count(Conversation.id))
            .where(Conversation.created_at >= today)
        )
        conversations_today = conv_today.scalar() or 0
        
        msg_today = await db.execute(
            select(func.count(Message.id))
            .where(Message.created_at >= today)
        )
        messages_today = msg_today.scalar() or 0
        
        tok_today = await db.execute(
            select(func.sum(Message.tokens))
            .where(Message.created_at >= today)
        )
        tokens_today = tok_today.scalar() or 0
        
        return DashboardStats(
            total_conversations=total_conversations,
            total_messages=total_messages,
            total_tokens=total_tokens,
            active_model="dolphin-mistral",
            avg_response_time=round(avg_response_time, 2),
            conversations_today=conversations_today,
            messages_today=messages_today,
            tokens_today=tokens_today,
        )
    
    async def auto_generate_title(
        self,
        db: AsyncSession,
        conversation_id: int
    ) -> Optional[str]:
        """Auto-generate a title based on the first message."""
        messages = await self.get_messages(db, conversation_id, limit=1)
        if messages:
            first_message = messages[0].content[:50]
            title = first_message.strip()
            if len(first_message) >= 50:
                title += "..."
            return title
        return None


# Singleton instance
conversation_service = ConversationService()
