"""
LocalAI Assistant - API Tests
Comprehensive test suite for API endpoints
Author: Lucas Andre S
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_root_endpoint():
    """Test root endpoint returns API info."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert data["name"] == "LocalAI Assistant"


@pytest.mark.anyio
async def test_health_endpoint():
    """Test health check endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.anyio
async def test_api_info_endpoint():
    """Test API info endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1")
    
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert "endpoints" in data


@pytest.mark.anyio
async def test_list_models():
    """Test listing available models."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/models/")
    
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert isinstance(data["models"], list)


@pytest.mark.anyio
async def test_list_prompts():
    """Test listing system prompts."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/prompts/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.anyio
async def test_create_conversation():
    """Test creating a new conversation."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/conversations/",
            json={
                "title": "Test Conversation",
                "model": "dolphin-mistral"
            }
        )
    
    assert response.status_code == 201
    data = response.json()
    assert "uuid" in data
    assert data["title"] == "Test Conversation"


@pytest.mark.anyio
async def test_list_conversations():
    """Test listing conversations."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/conversations/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.anyio
async def test_chat_completion():
    """Test chat completion endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/chat/completions",
            json={
                "message": "Hello, how are you?"
            }
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    assert "message" in data


@pytest.mark.anyio
async def test_dashboard_stats():
    """Test dashboard statistics endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/conversations/stats")
    
    assert response.status_code == 200
    data = response.json()
    assert "total_conversations" in data
    assert "total_messages" in data


@pytest.mark.anyio
async def test_openapi_docs():
    """Test OpenAPI documentation is accessible."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/openapi.json")
    
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data
