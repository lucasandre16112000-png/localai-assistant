"""
LocalAI Assistant - Code Execution Router
API endpoints for executing code (Python, JavaScript, Shell)
Author: Manus AI
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from ..services.code_executor import code_executor

router = APIRouter(prefix="/execute", tags=["Code Execution"])


class PythonExecutionRequest(BaseModel):
    """Request model for Python execution"""
    code: str
    timeout: Optional[int] = None
    sandbox: bool = True


class JavaScriptExecutionRequest(BaseModel):
    """Request model for JavaScript execution"""
    code: str
    timeout: Optional[int] = None


class ShellExecutionRequest(BaseModel):
    """Request model for Shell execution"""
    command: str
    timeout: Optional[int] = None


class CodeWithInputRequest(BaseModel):
    """Request model for code with input"""
    code: str
    language: str
    input_data: str = ""
    timeout: Optional[int] = None


@router.post("/python")
async def execute_python(request: PythonExecutionRequest):
    """
    Execute Python code.
    
    - **code**: Python code to execute
    - **timeout**: Execution timeout in seconds
    - **sandbox**: Whether to sandbox execution
    """
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    result = await code_executor.execute_python(
        request.code,
        request.timeout,
        request.sandbox
    )
    
    return result


@router.post("/javascript")
async def execute_javascript(request: JavaScriptExecutionRequest):
    """
    Execute JavaScript code.
    
    - **code**: JavaScript code to execute
    - **timeout**: Execution timeout in seconds
    """
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    result = await code_executor.execute_javascript(
        request.code,
        request.timeout
    )
    
    return result


@router.post("/shell")
async def execute_shell(request: ShellExecutionRequest):
    """
    Execute shell command.
    
    - **command**: Shell command to execute
    - **timeout**: Execution timeout in seconds
    """
    if not request.command.strip():
        raise HTTPException(status_code=400, detail="Command cannot be empty")
    
    result = await code_executor.execute_shell(
        request.command,
        request.timeout
    )
    
    return result


@router.post("/with-input")
async def execute_with_input(request: CodeWithInputRequest):
    """
    Execute code with input data.
    
    - **code**: Code to execute
    - **language**: Programming language (python, javascript)
    - **input_data**: Input data for the program
    - **timeout**: Execution timeout
    """
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    if request.language not in ["python", "javascript"]:
        raise HTTPException(status_code=400, detail="Unsupported language")
    
    result = await code_executor.execute_with_input(
        request.code,
        request.language,
        request.input_data,
        request.timeout
    )
    
    return result
