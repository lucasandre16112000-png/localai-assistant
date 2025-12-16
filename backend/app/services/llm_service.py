"""
LocalAI Assistant - LLM Service
Service for interacting with Ollama and local LLM models
Author: Lucas Andre S
"""

import asyncio
import httpx
import json
from typing import AsyncGenerator, Optional, Dict, Any, List
from datetime import datetime

from ..core.config import settings


class LLMService:
    """
    Service class for LLM operations.
    Handles communication with Ollama API for local model inference.
    """
    
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.default_model = settings.DEFAULT_MODEL
        self.timeout = httpx.Timeout(120.0, connect=10.0)
    
    async def list_models(self) -> List[Dict[str, Any]]:
        """
        List all available models from Ollama.
        Returns a list of model information dictionaries.
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    data = response.json()
                    return data.get("models", [])
                return []
        except Exception as e:
            # Return mock models for demo when Ollama is not available
            return [
                {
                    "name": "dolphin-mistral",
                    "modified_at": datetime.utcnow().isoformat(),
                    "size": 4_100_000_000,
                    "details": {"family": "mistral", "parameter_size": "7B"}
                },
                {
                    "name": "wizardlm-uncensored",
                    "modified_at": datetime.utcnow().isoformat(),
                    "size": 7_400_000_000,
                    "details": {"family": "llama", "parameter_size": "13B"}
                },
                {
                    "name": "codellama",
                    "modified_at": datetime.utcnow().isoformat(),
                    "size": 3_800_000_000,
                    "details": {"family": "llama", "parameter_size": "7B"}
                },
                {
                    "name": "nous-hermes",
                    "modified_at": datetime.utcnow().isoformat(),
                    "size": 4_000_000_000,
                    "details": {"family": "llama", "parameter_size": "7B"}
                }
            ]
    
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 40,
        max_tokens: int = 2048,
        context: Optional[List[int]] = None,
    ) -> Dict[str, Any]:
        """
        Generate a completion from the LLM.
        Returns the full response with metadata.
        """
        model = model or self.default_model
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "num_predict": max_tokens,
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        if context:
            payload["context"] = context
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                start_time = datetime.utcnow()
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                )
                end_time = datetime.utcnow()
                
                if response.status_code == 200:
                    data = response.json()
                    data["generation_time"] = (end_time - start_time).total_seconds()
                    return data
                else:
                    raise Exception(f"LLM API error: {response.status_code}")
        except httpx.ConnectError:
            # Demo mode response when Ollama is not available
            return self._generate_demo_response(prompt, model)
    
    async def generate_stream(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 40,
        max_tokens: int = 2048,
        context: Optional[List[int]] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Generate a streaming completion from the LLM.
        Yields chunks of the response as they are generated.
        """
        model = model or self.default_model
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "num_predict": max_tokens,
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        if context:
            payload["context"] = context
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/api/generate",
                    json=payload
                ) as response:
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                chunk = json.loads(line)
                                yield chunk
                            except json.JSONDecodeError:
                                continue
        except httpx.ConnectError:
            # Demo mode streaming when Ollama is not available
            async for chunk in self._generate_demo_stream(prompt, model):
                yield chunk
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 40,
        max_tokens: int = 2048,
    ) -> Dict[str, Any]:
        """
        Chat completion with message history.
        Uses the Ollama chat API for multi-turn conversations.
        """
        model = model or self.default_model
        
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "num_predict": max_tokens,
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                start_time = datetime.utcnow()
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload
                )
                end_time = datetime.utcnow()
                
                if response.status_code == 200:
                    data = response.json()
                    data["generation_time"] = (end_time - start_time).total_seconds()
                    return data
                else:
                    raise Exception(f"LLM API error: {response.status_code}")
        except httpx.ConnectError:
            # Demo mode response
            last_message = messages[-1]["content"] if messages else ""
            return self._generate_demo_response(last_message, model)
    
    async def chat_stream(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 40,
        max_tokens: int = 2048,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Streaming chat completion with message history.
        """
        model = model or self.default_model
        
        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "num_predict": max_tokens,
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/api/chat",
                    json=payload
                ) as response:
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                chunk = json.loads(line)
                                yield chunk
                            except json.JSONDecodeError:
                                continue
        except httpx.ConnectError:
            last_message = messages[-1]["content"] if messages else ""
            async for chunk in self._generate_demo_stream(last_message, model):
                yield chunk
    
    def _generate_demo_response(self, prompt: str, model: str) -> Dict[str, Any]:
        """Generate a demo response when Ollama is not available."""
        demo_responses = {
            "hello": "Hello! I'm LocalAI Assistant, your premium AI companion. How can I help you today?",
            "help": "I'm here to assist you with coding, analysis, writing, and much more. Just ask me anything!",
            "code": "```python\n# Here's a sample Python code\ndef greet(name: str) -> str:\n    return f'Hello, {name}!'\n\nprint(greet('World'))\n```",
        }
        
        response_text = demo_responses.get(
            prompt.lower().split()[0] if prompt else "hello",
            f"I received your message: '{prompt[:50]}...'. This is a demo response since Ollama is not currently running. In production, I would provide a comprehensive AI-generated response using the {model} model."
        )
        
        return {
            "model": model,
            "response": response_text,
            "done": True,
            "total_duration": 1500000000,
            "eval_count": len(response_text.split()),
            "generation_time": 1.5
        }
    
    async def _generate_demo_stream(
        self, 
        prompt: str, 
        model: str
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Generate demo streaming response."""
        response = self._generate_demo_response(prompt, model)
        words = response["response"].split()
        
        for i, word in enumerate(words):
            yield {
                "model": model,
                "response": word + " ",
                "done": i == len(words) - 1
            }
            await asyncio.sleep(0.05)  # Simulate typing delay


# Singleton instance
llm_service = LLMService()
