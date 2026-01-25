"""
LocalAI Assistant - Web Service
Service for web scraping, searching, and API integration
Author: Manus AI
"""

import httpx
import asyncio
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import json
from urllib.parse import urlencode
import logging

logger = logging.getLogger(__name__)


class WebService:
    """
    Service for web operations including scraping, searching, and API calls.
    Provides access to internet resources while maintaining performance through caching.
    """
    
    def __init__(self):
        self.timeout = httpx.Timeout(30.0, connect=10.0)
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour
        self.user_agent = "LocalAI-Assistant/1.0 (Compatible; Web Service)"
    
    async def search_web(
        self,
        query: str,
        num_results: int = 10,
        use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Search the web for information.
        
        Args:
            query: Search query string
            num_results: Number of results to return
            use_cache: Whether to use cached results
            
        Returns:
            List of search results with title, url, and snippet
        """
        cache_key = f"search:{query}:{num_results}"
        
        if use_cache and cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < timedelta(seconds=self.cache_ttl):
                logger.info(f"Returning cached search results for: {query}")
                return cached_data
        
        try:
            # Try using DuckDuckGo API (no key required)
            results = await self._search_duckduckgo(query, num_results)
            
            # Cache results
            self.cache[cache_key] = (results, datetime.now())
            return results
            
        except Exception as e:
            logger.error(f"Error searching web: {e}")
            return []
    
    async def _search_duckduckgo(
        self,
        query: str,
        num_results: int
    ) -> List[Dict[str, Any]]:
        """Search using DuckDuckGo API (no authentication required)"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # DuckDuckGo search
                url = "https://duckduckgo.com/api"
                params = {
                    "q": query,
                    "format": "json",
                    "no_redirect": 1,
                    "no_html": 1,
                    "skip_disambig": 1
                }
                
                response = await client.get(url, params=params)
                data = response.json()
                
                results = []
                
                # Process abstract result
                if data.get("AbstractText"):
                    results.append({
                        "title": data.get("Heading", "Result"),
                        "url": data.get("AbstractURL", ""),
                        "snippet": data.get("AbstractText", ""),
                        "source": "DuckDuckGo"
                    })
                
                # Process related topics
                for topic in data.get("RelatedTopics", [])[:num_results]:
                    if "Text" in topic:
                        results.append({
                            "title": topic.get("Text", "").split(" - ")[0],
                            "url": topic.get("FirstURL", ""),
                            "snippet": topic.get("Text", ""),
                            "source": "DuckDuckGo"
                        })
                
                return results[:num_results]
                
        except Exception as e:
            logger.error(f"DuckDuckGo search failed: {e}")
            return []
    
    async def scrape_url(
        self,
        url: str,
        selectors: Optional[List[str]] = None,
        extract_text: bool = True
    ) -> Dict[str, Any]:
        """
        Scrape content from a URL.
        
        Args:
            url: URL to scrape
            selectors: CSS selectors to extract specific elements
            extract_text: Whether to extract all text content
            
        Returns:
            Dictionary with scraped content
        """
        try:
            async with httpx.AsyncClient(
                timeout=self.timeout,
                headers={"User-Agent": self.user_agent}
            ) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                result = {
                    "url": url,
                    "status": response.status_code,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Extract title
                if soup.title:
                    result["title"] = soup.title.string
                
                # Extract specific selectors if provided
                if selectors:
                    result["selected_content"] = {}
                    for selector in selectors:
                        try:
                            elements = soup.select(selector)
                            result["selected_content"][selector] = [
                                elem.get_text(strip=True) for elem in elements
                            ]
                        except Exception as e:
                            logger.warning(f"Error extracting selector {selector}: {e}")
                
                # Extract all text if requested
                if extract_text:
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()
                    
                    text = soup.get_text(separator="\n", strip=True)
                    result["text"] = text[:5000]  # Limit to 5000 chars
                
                # Extract links
                result["links"] = [
                    {
                        "text": link.get_text(strip=True),
                        "href": link.get("href", "")
                    }
                    for link in soup.find_all("a")
                    if link.get("href")
                ][:20]  # Limit to 20 links
                
                return result
                
        except Exception as e:
            logger.error(f"Error scraping URL {url}: {e}")
            return {
                "url": url,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def fetch_json(self, url: str) -> Dict[str, Any]:
        """
        Fetch JSON data from an API endpoint.
        
        Args:
            url: API endpoint URL
            
        Returns:
            Parsed JSON data
        """
        try:
            async with httpx.AsyncClient(
                timeout=self.timeout,
                headers={"User-Agent": self.user_agent}
            ) as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Error fetching JSON from {url}: {e}")
            return {"error": str(e)}
    
    async def fetch_text(self, url: str) -> str:
        """
        Fetch plain text content from a URL.
        
        Args:
            url: URL to fetch
            
        Returns:
            Text content
        """
        try:
            async with httpx.AsyncClient(
                timeout=self.timeout,
                headers={"User-Agent": self.user_agent}
            ) as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.text
                
        except Exception as e:
            logger.error(f"Error fetching text from {url}: {e}")
            return f"Error: {str(e)}"
    
    async def get_page_metadata(self, url: str) -> Dict[str, Any]:
        """
        Extract metadata from a web page (title, description, keywords, etc).
        
        Args:
            url: URL to analyze
            
        Returns:
            Dictionary with page metadata
        """
        try:
            async with httpx.AsyncClient(
                timeout=self.timeout,
                headers={"User-Agent": self.user_agent}
            ) as client:
                response = await client.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                metadata = {
                    "url": url,
                    "title": soup.title.string if soup.title else None,
                    "description": None,
                    "keywords": None,
                    "author": None,
                    "og_image": None,
                    "og_title": None,
                    "og_description": None
                }
                
                # Extract meta tags
                for meta in soup.find_all("meta"):
                    name = meta.get("name", "").lower()
                    property_name = meta.get("property", "").lower()
                    content = meta.get("content", "")
                    
                    if name == "description":
                        metadata["description"] = content
                    elif name == "keywords":
                        metadata["keywords"] = content
                    elif name == "author":
                        metadata["author"] = content
                    elif property_name == "og:image":
                        metadata["og_image"] = content
                    elif property_name == "og:title":
                        metadata["og_title"] = content
                    elif property_name == "og:description":
                        metadata["og_description"] = content
                
                return metadata
                
        except Exception as e:
            logger.error(f"Error extracting metadata from {url}: {e}")
            return {"url": url, "error": str(e)}
    
    async def check_url_availability(self, url: str) -> Dict[str, Any]:
        """
        Check if a URL is available and get status information.
        
        Args:
            url: URL to check
            
        Returns:
            Dictionary with availability information
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.head(url, follow_redirects=True)
                
                return {
                    "url": url,
                    "available": response.status_code < 400,
                    "status_code": response.status_code,
                    "status_text": response.reason_phrase,
                    "content_type": response.headers.get("content-type", "unknown"),
                    "content_length": response.headers.get("content-length", "unknown")
                }
                
        except Exception as e:
            logger.error(f"Error checking URL {url}: {e}")
            return {
                "url": url,
                "available": False,
                "error": str(e)
            }
    
    def clear_cache(self):
        """Clear the cache"""
        self.cache.clear()
        logger.info("Web service cache cleared")


# Global instance
web_service = WebService()
