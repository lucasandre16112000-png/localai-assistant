"""
LocalAI Assistant - Conversations Router
API endpoints for conversation management
Author: Lucas Andre S
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_db
from ..schemas.conversation import (
    ConversationCreate,
    ConversationUpdate,
    ConversationResponse,
    ConversationWithMessages,
    MessageResponse,
    MessageUpdate,
    DashboardStats,
)
from ..services.conversation_service import conversation_service

router = APIRouter(prefix="/conversations", tags=["Conversations"])


@router.post("/", response_model=ConversationResponse, status_code=201)
async def create_conversation(
    data: ConversationCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new conversation.
    
    - **title**: Conversation title (optional, defaults to "New Conversation")
    - **model**: LLM model to use (optional, defaults to configured default)
    - **system_prompt**: Custom system prompt (optional)
    - **temperature**: Sampling temperature 0.0-2.0 (optional)
    - **top_p**: Top-p sampling 0.0-1.0 (optional)
    - **top_k**: Top-k sampling 1-100 (optional)
    - **max_tokens**: Maximum response tokens (optional)
    """
    conversation = await conversation_service.create_conversation(db, data)
    return conversation


@router.get("/", response_model=List[ConversationResponse])
async def list_conversations(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    include_archived: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """
    List all conversations with pagination.
    
    - **skip**: Number of conversations to skip (default: 0)
    - **limit**: Maximum number of conversations to return (default: 50, max: 100)
    - **include_archived**: Include archived conversations (default: false)
    """
    conversations = await conversation_service.list_conversations(
        db, skip=skip, limit=limit, include_archived=include_archived
    )
    return conversations


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    """
    Get dashboard statistics.
    
    Returns aggregated statistics including:
    - Total conversations, messages, and tokens
    - Average response time
    - Today's activity metrics
    """
    stats = await conversation_service.get_dashboard_stats(db)
    return stats


@router.get("/search", response_model=List[ConversationResponse])
async def search_conversations(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """
    Search conversations by title.
    
    - **q**: Search query string
    - **limit**: Maximum results to return (default: 20)
    """
    conversations = await conversation_service.search_conversations(db, q, limit)
    return conversations


@router.get("/{conversation_uuid}", response_model=ConversationWithMessages)
async def get_conversation(
    conversation_uuid: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific conversation with all messages.
    
    - **conversation_uuid**: UUID of the conversation
    """
    conversation = await conversation_service.get_conversation(db, conversation_uuid)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.patch("/{conversation_uuid}", response_model=ConversationResponse)
async def update_conversation(
    conversation_uuid: str,
    data: ConversationUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a conversation.
    
    - **conversation_uuid**: UUID of the conversation
    - All fields are optional, only provided fields will be updated
    """
    conversation = await conversation_service.update_conversation(
        db, conversation_uuid, data
    )
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.delete("/{conversation_uuid}", status_code=204)
async def delete_conversation(
    conversation_uuid: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a conversation and all its messages.
    
    - **conversation_uuid**: UUID of the conversation
    """
    success = await conversation_service.delete_conversation(db, conversation_uuid)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return None


@router.get("/{conversation_uuid}/messages", response_model=List[MessageResponse])
async def get_messages(
    conversation_uuid: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db)
):
    """
    Get messages for a conversation.
    
    - **conversation_uuid**: UUID of the conversation
    - **skip**: Number of messages to skip
    - **limit**: Maximum messages to return
    """
    conversation = await conversation_service.get_conversation(db, conversation_uuid)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = await conversation_service.get_messages(
        db, conversation.id, skip=skip, limit=limit
    )
    return messages


@router.patch("/messages/{message_uuid}", response_model=MessageResponse)
async def update_message(
    message_uuid: str,
    data: MessageUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a message content.
    
    - **message_uuid**: UUID of the message
    - **content**: New message content
    """
    message = await conversation_service.update_message(db, message_uuid, data.content)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message


@router.delete("/messages/{message_uuid}", status_code=204)
async def delete_message(
    message_uuid: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a message.
    
    - **message_uuid**: UUID of the message
    """
    success = await conversation_service.delete_message(db, message_uuid)
    if not success:
        raise HTTPException(status_code=404, detail="Message not found")
    return None


@router.post("/{conversation_uuid}/pin", response_model=ConversationResponse)
async def pin_conversation(
    conversation_uuid: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Pin a conversation.
    """
    conversation = await conversation_service.update_conversation(
        db, conversation_uuid, ConversationUpdate(is_pinned=True)
    )
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.post("/{conversation_uuid}/unpin", response_model=ConversationResponse)
async def unpin_conversation(
    conversation_uuid: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Unpin a conversation.
    """
    conversation = await conversation_service.update_conversation(
        db, conversation_uuid, ConversationUpdate(is_pinned=False)
    )
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.post("/{conversation_uuid}/archive", response_model=ConversationResponse)
async def archive_conversation(
    conversation_uuid: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Archive a conversation.
    """
    conversation = await conversation_service.update_conversation(
        db, conversation_uuid, ConversationUpdate(is_archived=True)
    )
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.post("/{conversation_uuid}/unarchive", response_model=ConversationResponse)
async def unarchive_conversation(
    conversation_uuid: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Unarchive a conversation.
    """
    conversation = await conversation_service.update_conversation(
        db, conversation_uuid, ConversationUpdate(is_archived=False)
    )
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation
