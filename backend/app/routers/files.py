"""
LocalAI Assistant - Files Router
API endpoints para processamento de arquivos
Author: Manus AI
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from ..services.file_processor import file_processor

router = APIRouter(prefix="/files", tags=["File Processing"])


class ProcessRequest(BaseModel):
    """Request model for file processing"""
    file_path: str


class ConvertRequest(BaseModel):
    """Request model for file conversion"""
    file_path: str
    target_format: str


class MergeRequest(BaseModel):
    """Request model for file merging"""
    file_paths: List[str]
    output_format: str = "pdf"


@router.post("/process/pdf")
async def process_pdf(
    file_path: str = Query(...),
    extract_text: bool = True,
    extract_images: bool = False,
    extract_tables: bool = True
):
    """
    Processar arquivo PDF.
    
    - **file_path**: Caminho do arquivo
    - **extract_text**: Extrair texto
    - **extract_images**: Extrair imagens
    - **extract_tables**: Extrair tabelas
    """
    result = await file_processor.process_pdf(
        file_path,
        extract_text,
        extract_images,
        extract_tables
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/process/excel")
async def process_excel(
    file_path: str = Query(...),
    sheet_name: Optional[str] = None
):
    """
    Processar arquivo Excel.
    
    - **file_path**: Caminho do arquivo
    - **sheet_name**: Nome da planilha
    """
    result = await file_processor.process_excel(file_path, sheet_name)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/process/csv")
async def process_csv(
    file_path: str = Query(...),
    delimiter: str = ",",
    encoding: str = "utf-8"
):
    """
    Processar arquivo CSV.
    
    - **file_path**: Caminho do arquivo
    - **delimiter**: Delimitador
    - **encoding**: Codificação
    """
    result = await file_processor.process_csv(file_path, delimiter, encoding)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/process/json")
async def process_json(
    file_path: str = Query(...),
    validate: bool = True
):
    """
    Processar arquivo JSON.
    
    - **file_path**: Caminho do arquivo
    - **validate**: Validar JSON
    """
    result = await file_processor.process_json(file_path, validate)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/process/xml")
async def process_xml(file_path: str = Query(...)):
    """
    Processar arquivo XML.
    
    - **file_path**: Caminho do arquivo
    """
    result = await file_processor.process_xml(file_path)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/process/text")
async def process_text(
    file_path: str = Query(...),
    encoding: str = "utf-8"
):
    """
    Processar arquivo de texto.
    
    - **file_path**: Caminho do arquivo
    - **encoding**: Codificação
    """
    result = await file_processor.process_text(file_path, encoding)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/convert")
async def convert_file(request: ConvertRequest):
    """
    Converter arquivo para outro formato.
    
    - **file_path**: Caminho do arquivo
    - **target_format**: Formato alvo
    """
    result = await file_processor.convert_file(request.file_path, request.target_format)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/merge")
async def merge_files(request: MergeRequest):
    """
    Mesclar múltiplos arquivos.
    
    - **file_paths**: Lista de caminhos
    - **output_format**: Formato de saída
    """
    if not request.file_paths:
        raise HTTPException(status_code=400, detail="At least one file required")
    
    result = await file_processor.merge_files(request.file_paths, request.output_format)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.get("/metadata")
async def extract_metadata(file_path: str = Query(...)):
    """
    Extrair metadados de arquivo.
    
    - **file_path**: Caminho do arquivo
    """
    result = await file_processor.extract_metadata(file_path)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result
