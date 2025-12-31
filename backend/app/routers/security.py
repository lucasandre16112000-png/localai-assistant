"""
LocalAI Assistant - Security Router
API endpoints para análise de segurança
Author: Manus AI
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from ..services.security_analyzer import security_analyzer

router = APIRouter(prefix="/security", tags=["Security"])


class CodeSecurityRequest(BaseModel):
    """Request model for code security analysis"""
    code: str
    language: str = "python"


@router.post("/analyze-code")
async def analyze_code_security(request: CodeSecurityRequest):
    """
    Analisar segurança de código.
    
    - **code**: Código a analisar
    - **language**: Linguagem de programação
    """
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    result = await security_analyzer.analyze_code_security(
        request.code,
        request.language
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/check-dependencies")
async def check_dependencies(requirements_file: str = Query(...)):
    """
    Verificar vulnerabilidades em dependências.
    
    - **requirements_file**: Arquivo de dependências
    """
    result = await security_analyzer.dependency_check(requirements_file)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/analyze-performance")
async def analyze_performance(request: CodeSecurityRequest):
    """
    Analisar performance de código.
    
    - **code**: Código a analisar
    - **language**: Linguagem de programação
    """
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    result = await security_analyzer.performance_analysis(
        request.code,
        request.language
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/analyze-quality")
async def analyze_quality(request: CodeSecurityRequest):
    """
    Analisar qualidade de código.
    
    - **code**: Código a analisar
    - **language**: Linguagem de programação
    """
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    result = await security_analyzer.code_quality_analysis(
        request.code,
        request.language
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/owasp-analysis")
async def owasp_analysis(code: str = Query(...)):
    """
    Análise OWASP Top 10.
    
    - **code**: Código a analisar
    """
    result = await security_analyzer.owasp_analysis(code)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/generate-report")
async def generate_security_report(request: CodeSecurityRequest):
    """
    Gerar relatório completo de segurança.
    
    - **code**: Código a analisar
    - **language**: Linguagem de programação
    """
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    result = await security_analyzer.generate_security_report(
        request.code,
        request.language
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result
