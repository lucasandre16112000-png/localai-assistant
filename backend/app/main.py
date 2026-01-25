"""
LocalAI Assistant - Main Application
Premium AI Assistant with Local LLM Support
Author: Lucas Andre S
GitHub: lucasandre16112000-png

A modern, enterprise-grade AI assistant application featuring:
- Real-time chat with streaming responses
- Multiple conversation management
- Customizable system prompts
- Analytics dashboard
- Full REST API with OpenAPI documentation
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time

from .core.config import settings
from .core.database import init_db, close_db
from .routers import (
    conversations_router,
    chat_router,
    models_router,
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info("🚀 Starting LocalAI Assistant...")
    init_db()
    logger.info("✅ Database initialized")
    yield
    # Shutdown
    logger.info("🛑 Shutting down LocalAI Assistant...")
    close_db()
    logger.info("✅ Cleanup complete")


# Initialize FastAPI app
app = FastAPI(
    title="LocalAI Assistant API",
    description="A powerful local AI assistant with streaming responses",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests and responses"""
    start_time = time.time()
    
    # Log request
    logger.debug(f"📨 {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.debug(f"✅ {request.method} {request.url.path} - {response.status_code} ({process_time:.2f}s)")
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"❌ {request.method} {request.url.path} - Error: {str(e)} ({process_time:.2f}s)")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )


# Include routers
app.include_router(chat_router, prefix="/api/v1")
app.include_router(conversations_router, prefix="/api/v1")
app.include_router(models_router, prefix="/api/v1")


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "LocalAI Assistant",
        "version": "1.0.0"
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to LocalAI Assistant API",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
