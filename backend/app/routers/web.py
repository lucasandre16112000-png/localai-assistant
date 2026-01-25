"""
LocalAI Assistant - Web Router
API endpoints for web operations (scraping, searching, fetching)
Author: Manus AI
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..services.web_service import web_service

router = APIRouter(prefix="/web", tags=["Web Operations"])


@router.post("/search")
async def search_web(
    query: str = Query(..., min_length=1, max_length=500),
    num_results: int = Query(10, ge=1, le=50),
    use_cache: bool = Query(True)
):
    """
    Search the web for information.
    
    - **query**: Search query string
    - **num_results**: Number of results to return (1-50)
    - **use_cache**: Whether to use cached results
    """
    try:
        results = await web_service.search_web(query, num_results, use_cache)
        return {
            "query": query,
            "num_results": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scrape")
async def scrape_url(
    url: str = Query(..., min_length=5),
    selectors: Optional[List[str]] = Query(None),
    extract_text: bool = Query(True)
):
    """
    Scrape content from a URL.
    
    - **url**: URL to scrape
    - **selectors**: CSS selectors to extract specific elements
    - **extract_text**: Whether to extract all text content
    """
    try:
        result = await web_service.scrape_url(url, selectors, extract_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fetch-json")
async def fetch_json(url: str = Query(..., min_length=5)):
    """
    Fetch JSON data from an API endpoint.
    
    - **url**: API endpoint URL
    """
    try:
        data = await web_service.fetch_json(url)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fetch-text")
async def fetch_text(url: str = Query(..., min_length=5)):
    """
    Fetch plain text content from a URL.
    
    - **url**: URL to fetch
    """
    try:
        text = await web_service.fetch_text(url)
        return {"url": url, "content": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metadata")
async def get_metadata(url: str = Query(..., min_length=5)):
    """
    Extract metadata from a web page.
    
    - **url**: URL to analyze
    """
    try:
        metadata = await web_service.get_page_metadata(url)
        return metadata
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/check-url")
async def check_url(url: str = Query(..., min_length=5)):
    """
    Check if a URL is available.
    
    - **url**: URL to check
    """
    try:
        status = await web_service.check_url_availability(url)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clear-cache")
async def clear_cache():
    """Clear the web service cache"""
    web_service.clear_cache()
    return {"message": "Cache cleared successfully"}
