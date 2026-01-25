"""
LocalAI Assistant - Documentation Router
API endpoints para geração de documentação
Author: Manus AI
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from ..services.documentation_service import documentation_service

router = APIRouter(prefix="/docs", tags=["Documentation"])


class MarkdownRequest(BaseModel):
    """Request model for Markdown generation"""
    title: str
    content: List[Dict[str, str]]
    include_toc: bool = True
    include_metadata: bool = True


class PDFRequest(BaseModel):
    """Request model for PDF generation"""
    title: str
    content: str
    author: str = "Manus AI"
    include_toc: bool = True


class SlidesRequest(BaseModel):
    """Request model for Slides generation"""
    title: str
    slides: List[Dict[str, Any]]
    theme: str = "default"
    output_format: str = "html"


class DiagramRequest(BaseModel):
    """Request model for Diagram generation"""
    title: str
    diagram_type: str
    content: str
    output_format: str = "png"


@router.post("/markdown")
async def generate_markdown(request: MarkdownRequest):
    """
    Gerar documento Markdown.
    
    - **title**: Título do documento
    - **content**: Seções com conteúdo
    - **include_toc**: Incluir índice
    - **include_metadata**: Incluir metadados
    """
    if not request.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    result = await documentation_service.generate_markdown(
        request.title,
        request.content,
        request.include_toc,
        request.include_metadata
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/pdf")
async def generate_pdf(request: PDFRequest):
    """
    Gerar documento PDF.
    
    - **title**: Título do documento
    - **content**: Conteúdo
    - **author**: Autor
    - **include_toc**: Incluir índice
    """
    if not request.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    result = await documentation_service.generate_pdf(
        request.title,
        request.content,
        request.author,
        request.include_toc
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/slides")
async def generate_slides(request: SlidesRequest):
    """
    Gerar apresentação em slides.
    
    - **title**: Título da apresentação
    - **slides**: Lista de slides
    - **theme**: Tema
    - **output_format**: Formato de saída
    """
    if not request.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    result = await documentation_service.generate_slides(
        request.title,
        request.slides,
        request.theme,
        request.output_format
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/diagram")
async def generate_diagram(request: DiagramRequest):
    """
    Gerar diagrama.
    
    - **title**: Título do diagrama
    - **diagram_type**: Tipo de diagrama
    - **content**: Definição do diagrama
    - **output_format**: Formato de saída
    """
    if not request.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    result = await documentation_service.generate_diagram(
        request.title,
        request.diagram_type,
        request.content,
        request.output_format
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/report")
async def generate_report(
    title: str = Query(...),
    sections: List[Dict[str, str]] = None,
    include_summary: bool = True,
    include_recommendations: bool = True
):
    """
    Gerar relatório.
    
    - **title**: Título do relatório
    - **sections**: Seções do relatório
    - **include_summary**: Incluir resumo
    - **include_recommendations**: Incluir recomendações
    """
    if not title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    result = await documentation_service.generate_report(
        title,
        sections or [],
        include_summary,
        include_recommendations
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result
