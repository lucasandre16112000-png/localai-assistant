"""
LocalAI Assistant - Analysis Router
API endpoints para análise de imagens, vídeos e dados
Author: Manus AI
"""

from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from ..services.image_analysis import image_analysis
from ..services.video_processor import video_processor
from ..services.advanced_data_analysis import advanced_data_analysis

router = APIRouter(prefix="/analysis", tags=["Analysis"])


class OCRRequest(BaseModel):
    """Request model for OCR"""
    image_path: str
    language: str = "por"


class ObjectDetectionRequest(BaseModel):
    """Request model for object detection"""
    image_path: str
    confidence_threshold: float = 0.5


class VideoConvertRequest(BaseModel):
    """Request model for video conversion"""
    video_path: str
    output_format: str
    quality: str = "high"


class DataAnalysisRequest(BaseModel):
    """Request model for data analysis"""
    data: List[float]
    include_percentiles: bool = True


# Image Analysis Endpoints
@router.post("/image/ocr")
async def ocr_extract_text(request: OCRRequest):
    """
    Extrair texto de imagem (OCR).
    
    - **image_path**: Caminho da imagem
    - **language**: Idioma para OCR
    """
    result = await image_analysis.ocr_extract_text(request.image_path, request.language)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/image/detect-objects")
async def detect_objects(request: ObjectDetectionRequest):
    """
    Detectar objetos em imagem.
    
    - **image_path**: Caminho da imagem
    - **confidence_threshold**: Limiar de confiança
    """
    result = await image_analysis.detect_objects(
        request.image_path,
        request.confidence_threshold
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/image/detect-faces")
async def detect_faces(image_path: str = Body(...)):
    """
    Detectar rostos em imagem.
    
    - **image_path**: Caminho da imagem
    """
    result = await image_analysis.detect_faces(image_path)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/image/analyze")
async def analyze_image(image_path: str = Body(...)):
    """
    Análise completa de imagem.
    
    - **image_path**: Caminho da imagem
    """
    result = await image_analysis.analyze_image(image_path)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/image/compare")
async def compare_images(
    image1_path: str = Body(...),
    image2_path: str = Body(...)
):
    """
    Comparar duas imagens.
    
    - **image1_path**: Caminho da primeira imagem
    - **image2_path**: Caminho da segunda imagem
    """
    result = await image_analysis.compare_images(image1_path, image2_path)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/image/extract-colors")
async def extract_colors(
    image_path: str = Body(...),
    num_colors: int = Body(5, ge=1, le=20)
):
    """
    Extrair cores dominantes de imagem.
    
    - **image_path**: Caminho da imagem
    - **num_colors**: Número de cores
    """
    result = await image_analysis.extract_colors(image_path, num_colors)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


# Video Processing Endpoints
@router.post("/video/convert")
async def convert_video(request: VideoConvertRequest):
    """
    Converter vídeo para outro formato.
    
    - **video_path**: Caminho do vídeo
    - **output_format**: Formato de saída
    - **quality**: Qualidade
    """
    result = await video_processor.convert_video(
        request.video_path,
        request.output_format,
        request.quality
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/video/extract-frames")
async def extract_frames(
    video_path: str = Body(...),
    interval: int = Body(1, ge=1)
):
    """
    Extrair frames de vídeo.
    
    - **video_path**: Caminho do vídeo
    - **interval**: Intervalo em segundos
    """
    result = await video_processor.extract_frames(video_path, interval)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/video/extract-audio")
async def extract_audio(
    video_path: str = Body(...),
    audio_format: str = Body("mp3")
):
    """
    Extrair áudio de vídeo.
    
    - **video_path**: Caminho do vídeo
    - **audio_format**: Formato de áudio
    """
    result = await video_processor.extract_audio(video_path, audio_format)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/video/trim")
async def trim_video(
    video_path: str = Body(...),
    start_time: str = Body(...),
    end_time: str = Body(...)
):
    """
    Cortar vídeo.
    
    - **video_path**: Caminho do vídeo
    - **start_time**: Tempo inicial (HH:MM:SS)
    - **end_time**: Tempo final (HH:MM:SS)
    """
    result = await video_processor.trim_video(video_path, start_time, end_time)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/video/analyze")
async def analyze_video(video_path: str = Body(...)):
    """
    Analisar vídeo.
    
    - **video_path**: Caminho do vídeo
    """
    result = await video_processor.analyze_video(video_path)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


# Data Analysis Endpoints
@router.post("/data/statistics")
async def statistical_analysis(request: DataAnalysisRequest):
    """
    Análise estatística de dados.
    
    - **data**: Lista de dados numéricos
    - **include_percentiles**: Incluir percentis
    """
    result = await advanced_data_analysis.statistical_analysis(
        request.data,
        request.include_percentiles
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/data/anomalies")
async def detect_anomalies(
    data: List[float] = Body(...),
    method: str = Body("zscore")
):
    """
    Detectar anomalias em dados.
    
    - **data**: Lista de dados
    - **method**: Método de detecção
    """
    result = await advanced_data_analysis.anomaly_detection(data, method)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/data/clustering")
async def clustering_analysis(
    data: List[List[float]] = Body(...),
    num_clusters: int = Query(3, ge=2, le=20)
):
    """
    Análise de clustering.
    
    - **data**: Dados multidimensionais
    - **num_clusters**: Número de clusters
    """
    result = await advanced_data_analysis.clustering_analysis(data, num_clusters)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result
