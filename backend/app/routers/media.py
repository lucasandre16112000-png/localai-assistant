"""
LocalAI Assistant - Media Router
API endpoints for image and audio generation/processing
Author: Manus AI
"""

from fastapi import APIRouter, HTTPException, Query, File, UploadFile
from pydantic import BaseModel
from typing import Optional, List
from ..services.image_service import image_service
from ..services.audio_service import audio_service

router = APIRouter(prefix="/media", tags=["Media Generation"])


class ImageGenerationRequest(BaseModel):
    """Request model for image generation"""
    prompt: str
    model: str = "stable-diffusion"
    size: str = "512x512"
    num_images: int = 1
    quality: str = "standard"


class ImageEditRequest(BaseModel):
    """Request model for image editing"""
    image_path: str
    prompt: str
    mask_path: Optional[str] = None


class TextToSpeechRequest(BaseModel):
    """Request model for text-to-speech"""
    text: str
    voice: str = "default"
    language: str = "en"
    speed: float = 1.0


class SpeechToTextRequest(BaseModel):
    """Request model for speech-to-text"""
    audio_path: str
    language: Optional[str] = None


# Image Endpoints
@router.post("/image/generate")
async def generate_image(request: ImageGenerationRequest):
    """
    Generate images from text prompts.
    
    - **prompt**: Text description
    - **model**: Model to use (stable-diffusion, dall-e)
    - **size**: Image size
    - **num_images**: Number of images
    - **quality**: Quality level
    """
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    result = await image_service.generate_image(
        request.prompt,
        request.model,
        request.size,
        request.num_images,
        request.quality
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/image/edit")
async def edit_image(request: ImageEditRequest):
    """
    Edit an existing image.
    
    - **image_path**: Path to image
    - **prompt**: Edit description
    - **mask_path**: Optional mask
    """
    result = await image_service.edit_image(
        request.image_path,
        request.prompt,
        request.mask_path
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/image/upscale")
async def upscale_image(image_path: str = Query(...), scale: int = Query(2, ge=2, le=4)):
    """
    Upscale an image.
    
    - **image_path**: Path to image
    - **scale**: Upscale factor (2, 4)
    """
    result = await image_service.upscale_image(image_path, scale)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/image/remove-background")
async def remove_background(image_path: str = Query(...)):
    """
    Remove background from image.
    
    - **image_path**: Path to image
    """
    result = await image_service.remove_background(image_path)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/image/analyze")
async def analyze_image(image_path: str = Query(...)):
    """
    Analyze an image (OCR, objects, etc).
    
    - **image_path**: Path to image
    """
    result = await image_service.analyze_image(image_path)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


# Audio Endpoints
@router.post("/audio/text-to-speech")
async def text_to_speech(request: TextToSpeechRequest):
    """
    Convert text to speech.
    
    - **text**: Text to convert
    - **voice**: Voice to use
    - **language**: Language code
    - **speed**: Speech speed
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    result = await audio_service.text_to_speech(
        request.text,
        request.voice,
        request.language,
        request.speed
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/audio/speech-to-text")
async def speech_to_text(request: SpeechToTextRequest):
    """
    Convert speech to text (transcription).
    
    - **audio_path**: Path to audio file
    - **language**: Language code (optional)
    """
    result = await audio_service.speech_to_text(
        request.audio_path,
        request.language
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/audio/generate-music")
async def generate_music(
    prompt: str = Query(...),
    duration: int = Query(30, ge=10, le=300),
    style: str = Query("ambient")
):
    """
    Generate music from description.
    
    - **prompt**: Music description
    - **duration**: Duration in seconds
    - **style**: Music style
    """
    result = await audio_service.generate_music(prompt, duration, style)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/audio/voice-clone")
async def voice_clone(
    audio_sample_path: str = Query(...),
    text: str = Query(...)
):
    """
    Clone a voice and generate speech.
    
    - **audio_sample_path**: Path to voice sample
    - **text**: Text to speak
    """
    result = await audio_service.voice_clone(audio_sample_path, text)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/audio/enhance")
async def enhance_audio(
    audio_path: str = Query(...),
    enhancement_type: str = Query("denoise")
):
    """
    Enhance audio quality.
    
    - **audio_path**: Path to audio
    - **enhancement_type**: Type of enhancement
    """
    result = await audio_service.audio_enhancement(audio_path, enhancement_type)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result
