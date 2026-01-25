"""
LocalAI Assistant - Chat API (FIXED VERSION)
API endpoints for chat completions with REAL streaming stop support
Author: Lucas Andre S & Manus AI
"""

import json
import logging
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

logger = logging.getLogger(__name__)

from ..core.database import get_db
from ..schemas.conversation import (
    ChatRequest,
    ChatResponse,
    MessageResponse,
    ConversationCreate,
)
from ..services.conversation_service import ConversationService
from ..services.llm_service import LLMService

router = APIRouter(prefix="/chat", tags=["chat"])
conversation_service = ConversationService()
llm_service = LLMService()

# Global variable to track stopped generations
stopped_generations = {}

@router.post("/stop-generation", response_model=dict)
async def stop_generation(
    conversation_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Stop the current generation and save partial response.
    """
    if conversation_id:
        stopped_generations[conversation_id] = True
        logger.info(f"Stop requested for conversation: {conversation_id}")
    
    return {
        "status": "success",
        "message": "Generation stopped successfully"
    }

def is_generation_stopped(conversation_id: str) -> bool:
    """Check if generation was stopped."""
    return stopped_generations.get(conversation_id, False)

def clear_stopped_generation(conversation_id: str):
    """Clear the stopped flag."""
    stopped_generations.pop(conversation_id, None)

@router.post("/completions-stream")
async def chat_completion_stream(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate a streaming chat completion with REAL stop support.
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
        
        # Add user message
        user_msg = await conversation_service.add_message(
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
        
        # Generate response
        model = request.model or conv_model
        temperature = request.temperature or conv_temp
        top_p = request.top_p or conv_top_p
        top_k = request.top_k or conv_top_k
        max_tokens = request.max_tokens or conv_max_tokens
        
        async def generate():
            full_response = ""
            total_tokens = 0
            generation_time = 0
            
            try:
                async for chunk in llm_service.chat_stream(
                    messages=chat_messages,
                    model=model,
                    temperature=temperature,
                    top_p=top_p,
                    top_k=top_k,
                    max_tokens=max_tokens,
                ):
                    # CHECK IF GENERATION WAS STOPPED
                    if is_generation_stopped(conv_uuid):
                        logger.info(f"Generation stopped for conversation {conv_uuid}")
                        clear_stopped_generation(conv_uuid)
                        break
                    
                    content = chunk.get("message", {}).get("content", "") or chunk.get("response", "")
                    full_response += content
                    
                    if content:
                        data = {
                            "content": content,
                            "done": False,
                            "conversation_id": conv_uuid,
                        }
                        yield f"data: {json.dumps(data)}\n\n"
                    
                    if chunk.get("done"):
                        total_tokens = chunk.get("eval_count", len(full_response.split()))
                        generation_time = chunk.get("generation_time", 0)
            
            except Exception as e:
                logger.error(f"Error during streaming: {e}")
                clear_stopped_generation(conv_uuid)
            
            # SAVE RESPONSE (even if partial)
            if full_response:
                await conversation_service.add_message(
                    db,
                    conv_id,
                    role="assistant",
                    content=full_response,
                    model=model,
                    tokens=total_tokens,
                    generation_time=generation_time,
                )
                logger.info(f"Saved response for conversation {conv_uuid}: {len(full_response)} chars")
            
            # AUTO-GENERATE TITLE if first message
            if conversation.message_count == 1:  # Just added user message
                title = request.message[:50]
                if len(request.message) > 50:
                    title += "..."
                from ..schemas.conversation import ConversationUpdate
                await conversation_service.update_conversation(
                    db, conv_uuid, ConversationUpdate(title=title)
                )
                logger.info(f"Auto-generated title for conversation {conv_uuid}: {title}")
            
            # Send final completion signal
            final_data = json.dumps({
                "done": True,
                "conversation_id": conv_uuid,
                "tokens": total_tokens,
                "generation_time": generation_time
            })
            yield f"data: {final_data}\n\n"
        
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
        logger.error(f"Error in streaming: {e}")
        raise HTTPException(status_code=500, detail=str(e))
