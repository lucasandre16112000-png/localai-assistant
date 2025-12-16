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
        
        # Resposta completa sobre QuickSort
        quicksort_response = """# Algoritmo QuickSort - Explicação Completa

## O que é o QuickSort?

O **QuickSort** é um algoritmo de ordenação eficiente baseado na estratégia de **dividir para conquistar**. Foi desenvolvido por Tony Hoare em 1959 e é amplamente utilizado devido à sua eficiência na prática.

## Como Funciona?

O algoritmo funciona da seguinte forma:

1. **Escolha do Pivô**: Seleciona um elemento do array como pivô
2. **Particionamento**: Reorganiza o array de forma que elementos menores que o pivô fiquem à esquerda e maiores à direita
3. **Recursão**: Aplica o mesmo processo recursivamente nas duas partições

## Complexidade de Tempo

| Caso | Complexidade | Descrição |
|------|--------------|-----------|
| **Melhor Caso** | O(n log n) | Quando o pivô divide o array em partes iguais |
| **Caso Médio** | O(n log n) | Na maioria das situações práticas |
| **Pior Caso** | O(n²) | Quando o array já está ordenado e o pivô é sempre o menor/maior elemento |

## Implementação em Python

```python
def quicksort(arr: list) -> list:
    \"\"\"
    Implementação do algoritmo QuickSort.
    
    Args:
        arr: Lista de elementos a serem ordenados
        
    Returns:
        Lista ordenada em ordem crescente
    \"\"\"
    # Caso base: arrays vazios ou com 1 elemento já estão ordenados
    if len(arr) <= 1:
        return arr
    
    # Escolhe o pivô (elemento do meio)
    pivot = arr[len(arr) // 2]
    
    # Particiona o array em três partes
    left = [x for x in arr if x < pivot]    # Elementos menores que o pivô
    middle = [x for x in arr if x == pivot]  # Elementos iguais ao pivô
    right = [x for x in arr if x > pivot]    # Elementos maiores que o pivô
    
    # Recursivamente ordena as partições e concatena
    return quicksort(left) + middle + quicksort(right)


# Exemplo de uso
if __name__ == "__main__":
    numeros = [64, 34, 25, 12, 22, 11, 90, 5]
    print(f"Array original: {numeros}")
    print(f"Array ordenado: {quicksort(numeros)}")
    # Saída: Array ordenado: [5, 11, 12, 22, 25, 34, 64, 90]
```

## Vantagens do QuickSort

- ✅ Muito eficiente na prática (O(n log n) na média)
- ✅ Ordenação in-place (baixo uso de memória)
- ✅ Boa performance com cache de CPU
- ✅ Paralelizável

## Desvantagens

- ❌ Pior caso O(n²) sem otimizações
- ❌ Não é estável (pode alterar ordem de elementos iguais)
- ❌ Recursivo (pode causar stack overflow em arrays muito grandes)

Espero que esta explicação tenha sido útil! 🚀"""

        # Verifica se a pergunta é sobre QuickSort
        prompt_lower = prompt.lower()
        if "quicksort" in prompt_lower or "ordenação" in prompt_lower or "ordenacao" in prompt_lower:
            response_text = quicksort_response
        elif "hello" in prompt_lower or "olá" in prompt_lower or "oi" in prompt_lower:
            response_text = "Olá! Sou o LocalAI Assistant, seu assistente de IA premium. Como posso ajudá-lo hoje?"
        elif "código" in prompt_lower or "code" in prompt_lower or "python" in prompt_lower:
            response_text = """```python
# Exemplo de código Python
def hello_world():
    print("Hello, World!")
    
hello_world()
```"""
        else:
            response_text = f"""Recebi sua mensagem! Esta é uma resposta de demonstração do LocalAI Assistant.

**Sua pergunta:** {prompt[:100]}...

Para obter respostas completas da IA, certifique-se de que o Ollama está rodando com um modelo instalado.

**Como iniciar:**
1. Instale o Ollama: `curl -fsSL https://ollama.ai/install.sh | sh`
2. Baixe um modelo: `ollama pull dolphin-mistral`
3. O LocalAI Assistant detectará automaticamente!

🚀 Modelo atual: {model}"""
        
        return {
            "model": model,
            "response": response_text,
            "done": True,
            "total_duration": 2500000000,
            "eval_count": len(response_text.split()),
            "generation_time": 2.5
        }
    
    async def _generate_demo_stream(
        self, 
        prompt: str, 
        model: str
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Generate demo streaming response."""
        response = self._generate_demo_response(prompt, model)
        text = response["response"]
        
        # Stream character by character for more realistic effect
        words = text.split(' ')
        for i, word in enumerate(words):
            yield {
                "model": model,
                "response": word + " ",
                "done": i == len(words) - 1
            }
            await asyncio.sleep(0.02)  # Faster typing delay


# Singleton instance
llm_service = LLMService()
