"""
LocalAI Assistant - Chat API
API endpoints for chat completions with streaming support
Author: Lucas Andre S
"""

import json
import logging
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

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
stopped_generations = set()

def is_generation_stopped(conversation_id: str) -> bool:
    """Check if generation was stopped for this conversation."""
    return conversation_id in stopped_generations

def clear_stopped_generation(conversation_id: str):
    """Clear the stopped flag for this conversation."""
    stopped_generations.discard(conversation_id)

@router.post("/stop-generation", response_model=dict)
async def stop_generation(
    conversation_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Stop the current generation and save partial response.
    This endpoint is called when user clicks the STOP button.
    """
    if conversation_id:
        stopped_generations.add(conversation_id)
        logger.info(f"✅ STOP requested for conversation: {conversation_id}")
        return {
            "status": "success",
            "message": f"Generation stopped successfully for {conversation_id}"
        }
    else:
        logger.warning("Stop requested but no conversation_id provided")
        return {
            "status": "error",
            "message": "No conversation_id provided"
        }

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
        conv_uuid = str(conversation.uuid)  # Convert to string for comparison
        conv_model = conversation.model
        conv_temp = conversation.temperature
        conv_top_p = conversation.top_p
        conv_top_k = conversation.top_k
        conv_max_tokens = conversation.max_tokens
        conv_system_prompt = conversation.system_prompt
        conv_message_count = conversation.message_count
        
        # Add user message
        user_msg = await conversation_service.add_message(
            db,
            conv_id,
            role="user",
            content=request.message,
            tokens=len(request.message.split())
        )
        
        # Build message history (get fresh from DB)
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
        
        # Auto-generate title if first message (check after adding message)
        if conv_message_count == 0:  # First message just added
            title = request.message[:50]
            if len(request.message) > 50:
                title += "..."
            from ..schemas.conversation import ConversationUpdate
            await conversation_service.update_conversation(
                db, conv_uuid, ConversationUpdate(title=title)
            )
            # Refresh conversation to get updated title
            conversation = await conversation_service.get_conversation(db, conv_uuid)
        
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
        logger.error(f"Error in chat completion: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/completions/stream")
async def chat_completion_stream_new(
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
                temperature=request.temperature or 0.7,
                top_p=request.top_p or 0.9,
                top_k=request.top_k or 40,
                max_tokens=request.max_tokens or 2048,
            )
            conversation = await conversation_service.create_conversation(db, conv_data)
        
        # Store conversation data
        conv_id = conversation.id
        conv_uuid = str(conversation.uuid)  # Convert to string for comparison
        conv_model = conversation.model
        conv_temp = conversation.temperature
        conv_top_p = conversation.top_p
        conv_top_k = conversation.top_k
        conv_max_tokens = conversation.max_tokens
        conv_system_prompt = conversation.system_prompt
        conv_message_count = conversation.message_count
        
        # Add user message
        user_msg = await conversation_service.add_message(
            db,
            conv_id,
            role="user",
            content=request.message,
            tokens=len(request.message.split())
        )
        
        # Build message history (get fresh from DB)
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
                    # Check if generation was stopped
                    if is_generation_stopped(conv_uuid):
                        logger.info(f"Generation stopped for conversation {conv_uuid}")
                        clear_stopped_generation(conv_uuid)
                        break
                    
                    content = chunk.get("message", {}).get("content", "") or chunk.get("response", "")
                    full_response += content
                    
                    if content:  # Only send non-empty content
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
            
            # Save assistant message to database (even if partial)
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
            
            # Auto-generate title if first message
            if conv_message_count == 0:
                title = request.message[:50]
                if len(request.message) > 50:
                    title += "..."
                from ..schemas.conversation import ConversationUpdate
                await conversation_service.update_conversation(
                    db, conv_uuid, ConversationUpdate(title=title)
                )
            
            # Send final completion signal with metadata
            final_data = json.dumps({"done": True, "conversation_id": conv_uuid, "tokens": total_tokens, "generation_time": generation_time})
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


@router.post("/regenerate/{message_uuid}")
async def regenerate_response(
    message_uuid: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Regenerate a response for a specific message.
    """
    try:
        # Get the message
        message = await conversation_service.get_message(db, message_uuid)
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        
        # Get the conversation
        conversation = await conversation_service.get_conversation(db, message.conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Get all messages up to (but not including) this one
        all_messages = await conversation_service.get_messages(db, message.conversation_id)
        messages_before = [m for m in all_messages if m.id < message.id]
        
        # Build chat messages
        chat_messages = []
        if conversation.system_prompt:
            chat_messages.append({
                "role": "system",
                "content": conversation.system_prompt
            })
        
        for msg in messages_before:
            chat_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Generate new response
        response = await llm_service.chat(
            messages=chat_messages,
            model=conversation.model,
            temperature=conversation.temperature,
            top_p=conversation.top_p,
            top_k=conversation.top_k,
            max_tokens=conversation.max_tokens,
        )
        
        # Extract response content
        assistant_content = response.get("message", {}).get("content", "") or response.get("response", "")
        generation_time = response.get("generation_time", 0)
        eval_count = response.get("eval_count", len(assistant_content.split()))
        
        # Update the message
        updated_message = await conversation_service.update_message(db, message_uuid, assistant_content)
        
        return {
            "status": "success",
            "message": {
                "id": updated_message.id,
                "uuid": updated_message.uuid,
                "content": updated_message.content,
                "tokens": eval_count,
                "generation_time": generation_time,
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error regenerating response: {e}")
        raise HTTPException(status_code=500, detail=str(e))
