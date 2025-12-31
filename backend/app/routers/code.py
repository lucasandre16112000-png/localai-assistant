"""
LocalAI Assistant - Code Router
API endpoints for code analysis, fixing, and optimization
Author: Manus AI
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from ..services.code_analyzer import code_analyzer
from ..services.code_fixer import code_fixer

router = APIRouter(prefix="/code", tags=["Code Analysis"])


class CodeRequest(BaseModel):
    """Request model for code operations"""
    code: str
    language: str = "python"


class CodeFixRequest(BaseModel):
    """Request model for code fixing"""
    code: str
    language: str = "python"
    auto_format: bool = True


@router.post("/analyze")
async def analyze_code(request: CodeRequest):
    """
    Analyze code for issues, complexity, and quality.
    
    - **code**: Source code to analyze
    - **language**: Programming language (python, javascript, etc)
    """
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    try:
        result = await code_analyzer.analyze_code(request.code, request.language)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fix")
async def fix_code(request: CodeFixRequest):
    """
    Fix code issues automatically.
    
    - **code**: Source code to fix
    - **language**: Programming language
    - **auto_format**: Whether to auto-format the code
    """
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    try:
        result = await code_fixer.fix_code(request.code, request.language, request.auto_format)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize")
async def optimize_code(request: CodeRequest):
    """
    Suggest code optimizations.
    
    - **code**: Source code to optimize
    - **language**: Programming language
    """
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    try:
        result = await code_fixer.optimize_code(request.code)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain")
async def explain_code(request: CodeRequest):
    """
    Generate explanation of code structure.
    
    - **code**: Source code to explain
    - **language**: Programming language
    """
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    try:
        result = await code_fixer.explain_code(request.code)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-and-fix")
async def analyze_and_fix(request: CodeFixRequest):
    """
    Analyze code and fix all issues automatically.
    
    - **code**: Source code to analyze and fix
    - **language**: Programming language
    - **auto_format**: Whether to auto-format the code
    """
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    try:
        # First analyze
        analysis = await code_analyzer.analyze_code(request.code, request.language)
        
        # Then fix
        fixed = await code_fixer.fix_code(request.code, request.language, request.auto_format)
        
        # Then optimize
        optimized = await code_fixer.optimize_code(fixed["fixed_code"])
        
        return {
            "analysis": analysis,
            "fixed": fixed,
            "optimizations": optimized,
            "summary": f"Found {len(analysis['issues'])} issue(s), fixed {len(fixed['changes'])} change(s), "
                      f"suggested {len(optimized['suggestions'])} optimization(s)"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
