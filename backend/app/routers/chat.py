"""
LocalAI Assistant - Chat Router
API endpoints for chat completions with streaming support
Author: Lucas Andre S
"""

import json
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_db
from ..schemas.conversation import (
    ChatRequest,
    ChatResponse,
    ConversationCreate,
    MessageResponse,
)
from ..services.llm_service import llm_service
from ..services.conversation_service import conversation_service

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/completions", response_model=ChatResponse)
async def chat_completion(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate a chat completion.
    """
    try:
        # Get or create conversation
        conversation = None
        if request.conversation_id:
            conversation = await conversation_service.get_conversation(
                db, request.conversation_id
            )
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            conv_data = ConversationCreate(
                title="New Conversation",
                model=request.model or "dolphin-mistral",
                temperature=request.temperature or 0.7,
                top_p=request.top_p or 0.9,
                top_k=request.top_k or 40,
                max_tokens=request.max_tokens or 2048,
            )
            conversation = await conversation_service.create_conversation(db, conv_data)
        
        # Store conversation data
        conv_id = conversation.id
        conv_uuid = conversation.uuid
        conv_model = conversation.model
        conv_temp = conversation.temperature
        conv_top_p = conversation.top_p
        conv_top_k = conversation.top_k
        conv_max_tokens = conversation.max_tokens
        conv_system_prompt = conversation.system_prompt
        conv_message_count = conversation.message_count
        
        # Add user message
        await conversation_service.add_message(
            db,
            conv_id,
            role="user",
            content=request.message,
            tokens=len(request.message.split())
        )
        
        # Build message history for context
        messages = await conversation_service.get_messages(db, conv_id)
        chat_messages = []
        
        if conv_system_prompt:
            chat_messages.append({
                "role": "system",
                "content": conv_system_prompt
            })
        
        for msg in messages:
            chat_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Generate response
        model = request.model or conv_model
        temperature = request.temperature or conv_temp
        top_p = request.top_p or conv_top_p
        top_k = request.top_k or conv_top_k
        max_tokens = request.max_tokens or conv_max_tokens
        
        response = await llm_service.chat(
            messages=chat_messages,
            model=model,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_tokens=max_tokens,
        )
        
        # Extract response content
        assistant_content = response.get("message", {}).get("content", "") or response.get("response", "")
        generation_time = response.get("generation_time", 0)
        eval_count = response.get("eval_count", len(assistant_content.split()))
        
        # Add assistant message and get data immediately
        assistant_message = await conversation_service.add_message(
            db,
            conv_id,
            role="assistant",
            content=assistant_content,
            model=model,
            tokens=eval_count,
            generation_time=generation_time,
        )
        
        # Store message data before session closes
        msg_id = assistant_message.id
        msg_uuid = assistant_message.uuid
        msg_conv_id = assistant_message.conversation_id
        msg_role = assistant_message.role
        msg_content = assistant_message.content
        msg_model = assistant_message.model
        msg_tokens = assistant_message.tokens
        msg_gen_time = assistant_message.generation_time
        msg_is_edited = assistant_message.is_edited
        msg_created = assistant_message.created_at
        msg_updated = assistant_message.updated_at
        
        # Auto-generate title if first message
        if conv_message_count <= 1:
            title = request.message[:50]
            if len(request.message) > 50:
                title += "..."
            from ..schemas.conversation import ConversationUpdate
            await conversation_service.update_conversation(
                db, conv_uuid, ConversationUpdate(title=title)
            )
        
        return ChatResponse(
            conversation_id=conv_uuid,
            message=MessageResponse(
                id=msg_id,
                uuid=msg_uuid,
                conversation_id=msg_conv_id,
                role=msg_role,
                content=msg_content,
                model=msg_model,
                tokens=msg_tokens,
                generation_time=msg_gen_time,
                is_edited=msg_is_edited,
                created_at=msg_created,
                updated_at=msg_updated,
            ),
            model=model,
            tokens=eval_count,
            generation_time=generation_time,
        )
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/completions/stream")
async def chat_completion_stream(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate a streaming chat completion.
    """
    try:
        # Get or create conversation
        conversation = None
        if request.conversation_id:
            conversation = await conversation_service.get_conversation(
                db, request.conversation_id
            )
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            conv_data = ConversationCreate(
                title="New Conversation",
                model=request.model or "dolphin-mistral",
            )
            conversation = await conversation_service.create_conversation(db, conv_data)
        
        # Store conversation data
        conv_id = conversation.id
        conv_uuid = conversation.uuid
        conv_model = conversation.model
        conv_temp = conversation.temperature
        conv_top_p = conversation.top_p
        conv_top_k = conversation.top_k
        conv_max_tokens = conversation.max_tokens
        conv_system_prompt = conversation.system_prompt
        
        # Add user message
        await conversation_service.add_message(
            db,
            conv_id,
            role="user",
            content=request.message,
            tokens=len(request.message.split())
        )
        
        # Build message history
        messages = await conversation_service.get_messages(db, conv_id)
        chat_messages = []
        
        if conv_system_prompt:
            chat_messages.append({
                "role": "system",
                "content": conv_system_prompt
            })
        
        for msg in messages:
            chat_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        model = request.model or conv_model
        
        async def generate():
            full_response = ""
            total_tokens = 0
            
            async for chunk in llm_service.chat_stream(
                messages=chat_messages,
                model=model,
                temperature=request.temperature or conv_temp,
                top_p=request.top_p or conv_top_p,
                top_k=request.top_k or conv_top_k,
                max_tokens=request.max_tokens or conv_max_tokens,
            ):
                content = chunk.get("message", {}).get("content", "") or chunk.get("response", "")
                full_response += content
                
                data = {
                    "content": content,
                    "done": chunk.get("done", False),
                    "conversation_id": conv_uuid,
                }
                yield f"data: {json.dumps(data)}\n\n"
                
                if chunk.get("done"):
                    total_tokens = chunk.get("eval_count", len(full_response.split()))
            
            yield f"data: {json.dumps({'done': True, 'conversation_id': conv_uuid})}\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/regenerate/{message_uuid}")
async def regenerate_response(
    message_uuid: str,
    db: AsyncSession = Depends(get_db)
):
    """Regenerate an assistant response."""
    raise HTTPException(
        status_code=501,
        detail="Regenerate feature coming soon"
    )
