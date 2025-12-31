"""
LocalAI Assistant - DevOps Router
API endpoints para deploy e automação
Author: Manus AI
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, List, Any
from ..services.devops_service import devops_service

router = APIRouter(prefix="/devops", tags=["DevOps"])


class DockerfileRequest(BaseModel):
    """Request model for Dockerfile generation"""
    project_path: str
    language: str
    base_image: str = None


class DockerComposeRequest(BaseModel):
    """Request model for docker-compose generation"""
    services: List[Dict[str, Any]]


class DockerBuildRequest(BaseModel):
    """Request model for Docker image build"""
    dockerfile_path: str
    image_name: str
    tag: str = "latest"


class DeploymentRequest(BaseModel):
    """Request model for deployment"""
    image_name: str
    container_name: str
    port_mapping: Dict[int, int]


@router.post("/docker/dockerfile")
async def generate_dockerfile(request: DockerfileRequest):
    """
    Gerar Dockerfile para projeto.
    
    - **project_path**: Caminho do projeto
    - **language**: Linguagem de programação
    - **base_image**: Imagem base (opcional)
    """
    result = await devops_service.generate_dockerfile(
        request.project_path,
        request.language,
        request.base_image
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/docker/docker-compose")
async def generate_docker_compose(request: DockerComposeRequest):
    """
    Gerar docker-compose.yml.
    
    - **services**: Lista de serviços
    """
    result = await devops_service.generate_docker_compose(request.services)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/docker/build")
async def build_docker_image(request: DockerBuildRequest):
    """
    Construir imagem Docker.
    
    - **dockerfile_path**: Caminho do Dockerfile
    - **image_name**: Nome da imagem
    - **tag**: Tag da imagem
    """
    result = await devops_service.build_docker_image(
        request.dockerfile_path,
        request.image_name,
        request.tag
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/docker/deploy")
async def deploy_container(request: DeploymentRequest):
    """
    Fazer deploy de container.
    
    - **image_name**: Nome da imagem
    - **container_name**: Nome do container
    - **port_mapping**: Mapeamento de portas
    """
    result = await devops_service.deploy_container(
        request.image_name,
        request.container_name,
        request.port_mapping
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/kubernetes/manifest")
async def generate_kubernetes_manifest(
    app_name: str = Query(...),
    replicas: int = Query(3, ge=1, le=100)
):
    """
    Gerar manifesto Kubernetes.
    
    - **app_name**: Nome da aplicação
    - **replicas**: Número de réplicas
    """
    result = await devops_service.generate_kubernetes_manifest(app_name, replicas)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/ci-cd/pipeline")
async def generate_ci_cd_pipeline(
    project_name: str = Query(...),
    platform: str = Query("github")
):
    """
    Gerar pipeline CI/CD.
    
    - **project_name**: Nome do projeto
    - **platform**: Plataforma (github, gitlab, jenkins)
    """
    result = await devops_service.generate_ci_cd_pipeline(project_name, platform)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.get("/monitor/{deployment_id}")
async def monitor_deployment(deployment_id: str):
    """
    Monitorar deployment.
    
    - **deployment_id**: ID do deployment
    """
    result = await devops_service.monitor_deployment(deployment_id)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result
