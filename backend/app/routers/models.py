"""
LocalAI Assistant - Models Router
API endpoints for LLM model management
Author: Lucas Andre S
"""

from typing import List
from fastapi import APIRouter, HTTPException

from ..schemas.conversation import ModelInfo, ModelList
from ..services.llm_service import llm_service

router = APIRouter(prefix="/models", tags=["Models"])


@router.get("/", response_model=ModelList)
async def list_models():
    """
    List all available LLM models.
    
    Returns a list of models available in Ollama.
    """
    models = await llm_service.list_models()
    return ModelList(
        models=[
            ModelInfo(
                name=m.get("name", "unknown"),
                modified_at=m.get("modified_at"),
                size=m.get("size"),
                digest=m.get("digest"),
                details=m.get("details"),
            )
            for m in models
        ]
    )


@router.get("/{model_name}", response_model=ModelInfo)
async def get_model(model_name: str):
    """
    Get information about a specific model.
    
    - **model_name**: Name of the model
    """
    models = await llm_service.list_models()
    for model in models:
        if model.get("name") == model_name:
            return ModelInfo(
                name=model.get("name", "unknown"),
                modified_at=model.get("modified_at"),
                size=model.get("size"),
                digest=model.get("digest"),
                details=model.get("details"),
            )
    
    raise HTTPException(status_code=404, detail="Model not found")


@router.get("/recommended", response_model=List[ModelInfo])
async def get_recommended_models():
    """
    Get list of recommended uncensored models.
    
    Returns curated list of best models for unrestricted use.
    """
    recommended = [
        ModelInfo(
            name="dolphin-mistral",
            details={
                "family": "mistral",
                "parameter_size": "7B",
                "description": "Uncensored Mistral fine-tune, excellent for general tasks",
                "recommended_for": ["general", "coding", "analysis"]
            }
        ),
        ModelInfo(
            name="wizardlm-uncensored",
            details={
                "family": "llama",
                "parameter_size": "13B",
                "description": "Powerful uncensored model for complex reasoning",
                "recommended_for": ["reasoning", "writing", "research"]
            }
        ),
        ModelInfo(
            name="codellama",
            details={
                "family": "llama",
                "parameter_size": "7B-34B",
                "description": "Specialized for code generation and analysis",
                "recommended_for": ["coding", "debugging", "code review"]
            }
        ),
        ModelInfo(
            name="nous-hermes",
            details={
                "family": "llama",
                "parameter_size": "7B-13B",
                "description": "Excellent conversational model",
                "recommended_for": ["conversation", "roleplay", "creative"]
            }
        ),
        ModelInfo(
            name="orca-2-uncensored",
            details={
                "family": "orca",
                "parameter_size": "7B-13B",
                "description": "Microsoft Orca without restrictions",
                "recommended_for": ["analysis", "reasoning", "education"]
            }
        ),
    ]
    return recommended
