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
    prompts_router,
)
from .routers.web import router as web_router
from .routers.code import router as code_router
from .routers.tasks import router as tasks_router
from .routers.data import router as data_router
from .routers.media import router as media_router
from .routers.execute import router as execute_router
from .routers.llm import router as llm_router
from .routers.docs import router as docs_router
from .routers.projects import router as projects_router
from .routers.files import router as files_router
from .routers.analysis import router as analysis_router
from .routers.security import router as security_router
from .routers.database import router as database_router
from .routers.devops import router as devops_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("🚀 Starting LocalAI Assistant...")
    await init_db()
    logger.info("✅ Database initialized")
    logger.info(f"📡 Ollama endpoint: {settings.OLLAMA_BASE_URL}")
    logger.info(f"🤖 Default model: {settings.DEFAULT_MODEL}")
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down LocalAI Assistant...")
    await close_db()
    logger.info("✅ Database connections closed")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="""
## LocalAI Assistant API

A premium, enterprise-grade AI assistant with local LLM support.

### Features

- 🤖 **Chat Completions** - Real-time chat with streaming support
- 💬 **Conversations** - Full conversation management with history
- 🎛️ **Models** - List and manage available LLM models
- 📝 **System Prompts** - Customizable prompt templates
- 📊 **Analytics** - Usage statistics and metrics

### Authentication

Currently, the API is open for local development. In production, 
configure API key authentication via the `X-API-Key` header.

### Rate Limiting

Default rate limit: 100 requests per minute per IP.

---

**Developer:** Lucas Andre S  
**GitHub:** [lucasandre16112000-png](https://github.com/lucasandre16112000-png)
    """,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS + ["*"],  # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time * 1000, 2)) + "ms"
    return response


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An unexpected error occurred",
        }
    )


# Include routers
app.include_router(chat_router, prefix="/api/v1")
app.include_router(conversations_router, prefix="/api/v1")
app.include_router(models_router, prefix="/api/v1")
app.include_router(prompts_router, prefix="/api/v1")
app.include_router(web_router, prefix="/api/v1")
app.include_router(code_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")
app.include_router(data_router, prefix="/api/v1")
app.include_router(media_router, prefix="/api/v1")
app.include_router(execute_router, prefix="/api/v1")
app.include_router(llm_router, prefix="/api/v1")
app.include_router(docs_router, prefix="/api/v1")
app.include_router(projects_router, prefix="/api/v1")
app.include_router(files_router, prefix="/api/v1")
app.include_router(analysis_router, prefix="/api/v1")
app.include_router(security_router, prefix="/api/v1")
app.include_router(database_router, prefix="/api/v1")
app.include_router(devops_router, prefix="/api/v1")


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "api": "/api/v1",
    }


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "ollama_url": settings.OLLAMA_BASE_URL,
        "default_model": settings.DEFAULT_MODEL,
    }


# API info endpoint
@app.get("/api/v1", tags=["API"])
async def api_info():
    """
    API version information.
    """
    return {
        "version": "v1",
        "endpoints": {
            "chat": "/api/v1/chat",
            "conversations": "/api/v1/conversations",
            "models": "/api/v1/models",
            "prompts": "/api/v1/prompts",
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json",
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else settings.WORKERS,
    )
