"""
LocalAI Assistant - Projects Router
API endpoints para geração automática de projetos
Author: Manus AI
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from ..services.project_generator import project_generator

router = APIRouter(prefix="/projects", tags=["Project Generation"])


class ReactProjectRequest(BaseModel):
    """Request model for React project"""
    project_name: str
    use_typescript: bool = True
    include_tailwind: bool = True
    include_router: bool = True


class FastAPIProjectRequest(BaseModel):
    """Request model for FastAPI project"""
    project_name: str
    include_auth: bool = True
    include_db: bool = True
    include_testing: bool = True


class FullStackProjectRequest(BaseModel):
    """Request model for Full Stack project"""
    project_name: str
    frontend_framework: str = "react"
    backend_framework: str = "fastapi"
    database: str = "sqlite"


@router.post("/react")
async def create_react_project(request: ReactProjectRequest):
    """
    Criar projeto React.
    
    - **project_name**: Nome do projeto
    - **use_typescript**: Usar TypeScript
    - **include_tailwind**: Incluir Tailwind CSS
    - **include_router**: Incluir React Router
    """
    if not request.project_name.strip():
        raise HTTPException(status_code=400, detail="Project name cannot be empty")
    
    result = await project_generator.generate_react_project(
        request.project_name,
        request.use_typescript,
        request.include_tailwind,
        request.include_router
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/fastapi")
async def create_fastapi_project(request: FastAPIProjectRequest):
    """
    Criar projeto FastAPI.
    
    - **project_name**: Nome do projeto
    - **include_auth**: Incluir autenticação
    - **include_db**: Incluir banco de dados
    - **include_testing**: Incluir testes
    """
    if not request.project_name.strip():
        raise HTTPException(status_code=400, detail="Project name cannot be empty")
    
    result = await project_generator.generate_fastapi_project(
        request.project_name,
        request.include_auth,
        request.include_db,
        request.include_testing
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/fullstack")
async def create_fullstack_project(request: FullStackProjectRequest):
    """
    Criar projeto Full Stack.
    
    - **project_name**: Nome do projeto
    - **frontend_framework**: Framework frontend
    - **backend_framework**: Framework backend
    - **database**: Banco de dados
    """
    if not request.project_name.strip():
        raise HTTPException(status_code=400, detail="Project name cannot be empty")
    
    result = await project_generator.generate_fullstack_project(
        request.project_name,
        request.frontend_framework,
        request.backend_framework,
        request.database
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/mobile")
async def create_mobile_project(
    project_name: str = Query(...),
    framework: str = Query("react-native")
):
    """
    Criar projeto Mobile.
    
    - **project_name**: Nome do projeto
    - **framework**: Framework mobile
    """
    result = await project_generator.generate_mobile_project(project_name, framework)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/cli")
async def create_cli_project(
    project_name: str = Query(...),
    language: str = Query("python")
):
    """
    Criar projeto CLI.
    
    - **project_name**: Nome do projeto
    - **language**: Linguagem de programação
    """
    result = await project_generator.generate_cli_project(project_name, language)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.get("/templates")
async def list_templates():
    """Listar templates de projeto disponíveis"""
    return await project_generator.list_project_templates()
