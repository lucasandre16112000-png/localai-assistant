"""
LocalAI Assistant - LLM Integration Router
API endpoints for querying local LLM models
100% LOCAL, SEM LIMITAÇÕES, LIBERDADE TOTAL
Author: Manus AI
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from ..services.llm_integration import llm_integration

router = APIRouter(prefix="/llm", tags=["LLM Integration"])


class LLMQueryRequest(BaseModel):
    """Request model for LLM query"""
    prompt: str
    model: str = "dolphin-mistral"
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40
    system_prompt: Optional[str] = None
    stream: bool = False


class ContextualQueryRequest(BaseModel):
    """Request model for contextual query"""
    prompt: str
    context: str
    model: str = "dolphin-mistral"
    temperature: float = 0.7


class MultiModelQueryRequest(BaseModel):
    """Request model for multi-model query"""
    prompt: str
    models: Optional[List[str]] = None
    temperature: float = 0.7


class CustomModelRequest(BaseModel):
    """Request model for creating custom model"""
    name: str
    base_model: str
    system_prompt: str
    parameters: Optional[dict] = None


@router.get("/models")
async def get_available_models():
    """
    Obter lista de modelos disponíveis localmente.
    """
    result = await llm_integration.get_available_models()
    return result


@router.post("/query")
async def query_local_model(request: LLMQueryRequest):
    """
    Query um modelo local.
    100% LOCAL, SEM LIMITAÇÕES, LIBERDADE TOTAL.
    
    - **prompt**: Prompt do usuário
    - **model**: Modelo a usar
    - **temperature**: Temperatura de sampling
    - **top_p**: Top-p sampling
    - **top_k**: Top-k sampling
    - **system_prompt**: System prompt (opcional)
    - **stream**: Se deve fazer streaming
    """
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    result = await llm_integration.query_local_model(
        request.prompt,
        request.model,
        request.temperature,
        request.top_p,
        request.top_k,
        request.system_prompt,
        request.stream
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/query-with-context")
async def query_with_context(request: ContextualQueryRequest):
    """
    Query modelo com contexto adicional.
    
    - **prompt**: Prompt do usuário
    - **context**: Contexto adicional
    - **model**: Modelo a usar
    - **temperature**: Temperatura
    """
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    result = await llm_integration.query_with_context(
        request.prompt,
        request.context,
        request.model,
        request.temperature
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/compare-models")
async def compare_models(request: MultiModelQueryRequest):
    """
    Query múltiplos modelos e compare respostas.
    
    - **prompt**: Prompt do usuário
    - **models**: Lista de modelos a consultar
    - **temperature**: Temperatura
    """
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    result = await llm_integration.query_multiple_models(
        request.prompt,
        request.models,
        request.temperature
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/create-custom-model")
async def create_custom_model(request: CustomModelRequest):
    """
    Criar um modelo customizado.
    
    - **name**: Nome do novo modelo
    - **base_model**: Modelo base
    - **system_prompt**: System prompt customizado
    - **parameters**: Parâmetros customizados
    """
    result = await llm_integration.create_custom_model(
        request.name,
        request.base_model,
        request.system_prompt,
        request.parameters
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.get("/capabilities")
async def get_capabilities():
    """
    Listar todas as capacidades disponíveis.
    """
    result = await llm_integration.list_all_capabilities()
    return result


@router.post("/fine-tune")
async def fine_tune_model(
    model: str = Query(...),
    training_data: List[dict] = None
):
    """
    Fine-tune um modelo local.
    
    - **model**: Modelo a fazer fine-tune
    - **training_data**: Dados de treinamento
    """
    if not training_data:
        raise HTTPException(status_code=400, detail="Training data required")
    
    result = await llm_integration.fine_tune_model(model, training_data)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result
