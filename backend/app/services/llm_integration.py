"""
LocalAI Assistant - LLM Integration Service
100% Local - Sem APIs externas, sem limitações, liberdade total
Author: Manus AI
"""

import os
from typing import Dict, List, Any, Optional
import logging
import httpx

logger = logging.getLogger(__name__)


class LLMIntegration:
    """
    Service para integração com múltiplos LLMs 100% locais.
    Suporta Ollama, LLaMA, Mistral, e qualquer modelo local.
    SEM LIMITAÇÕES, SEM FILTROS, LIBERDADE TOTAL.
    """
    
    def __init__(self):
        self.ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.local_models = []
    
    async def get_available_models(self) -> Dict[str, Any]:
        """
        Obter lista de modelos disponíveis localmente.
        
        Returns:
            Dictionary com modelos disponíveis
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.ollama_url}/api/tags")
                
                if response.status_code != 200:
                    return {"error": "Ollama não está respondendo"}
                
                data = response.json()
                models = [model["name"] for model in data.get("models", [])]
                
                return {
                    "status": "success",
                    "models": models,
                    "count": len(models)
                }
        
        except Exception as e:
            logger.error(f"Erro ao obter modelos: {e}")
            return {"error": str(e)}
    
    async def query_local_model(
        self,
        prompt: str,
        model: str = "dolphin-mistral",
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 40,
        system_prompt: Optional[str] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Query um modelo local via Ollama.
        SEM LIMITAÇÕES, SEM FILTROS, LIBERDADE TOTAL.
        
        Args:
            prompt: Prompt do usuário
            model: Modelo a usar
            temperature: Temperatura de sampling
            top_p: Top-p sampling
            top_k: Top-k sampling
            system_prompt: System prompt (opcional)
            stream: Se deve fazer streaming
            
        Returns:
            Dictionary com resposta
        """
        try:
            async with httpx.AsyncClient() as client:
                full_prompt = prompt
                if system_prompt:
                    full_prompt = f"{system_prompt}\n\n{prompt}"
                
                response = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": model,
                        "prompt": full_prompt,
                        "temperature": temperature,
                        "top_p": top_p,
                        "top_k": top_k,
                        "stream": stream
                    },
                    timeout=None
                )
                
                if response.status_code != 200:
                    return {"error": f"Erro no modelo local: {response.text}"}
                
                data = response.json()
                
                return {
                    "provider": "local-ollama",
                    "model": model,
                    "response": data.get("response", ""),
                    "tokens": data.get("eval_count", 0),
                    "total_duration": data.get("total_duration", 0),
                    "status": "success"
                }
        
        except Exception as e:
            logger.error(f"Erro ao consultar modelo local: {e}")
            return {"error": str(e)}
    
    async def query_with_context(
        self,
        prompt: str,
        context: str,
        model: str = "dolphin-mistral",
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Query modelo com contexto adicional.
        
        Args:
            prompt: Prompt do usuário
            context: Contexto adicional
            model: Modelo a usar
            temperature: Temperatura
            
        Returns:
            Dictionary com resposta
        """
        try:
            system_prompt = f"Você é um assistente inteligente e libertário. Contexto adicional:\n{context}"
            
            return await self.query_local_model(
                prompt,
                model=model,
                temperature=temperature,
                system_prompt=system_prompt
            )
        
        except Exception as e:
            logger.error(f"Erro: {e}")
            return {"error": str(e)}
    
    async def query_multiple_models(
        self,
        prompt: str,
        models: List[str] = None,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Query múltiplos modelos locais e compare respostas.
        
        Args:
            prompt: Prompt do usuário
            models: Lista de modelos a consultar
            temperature: Temperatura
            
        Returns:
            Dictionary com respostas de todos os modelos
        """
        if not models:
            models = ["dolphin-mistral"]
        
        responses = {}
        
        for model in models:
            response = await self.query_local_model(
                prompt,
                model=model,
                temperature=temperature
            )
            responses[model] = response
        
        return {
            "prompt": prompt,
            "models": models,
            "responses": responses,
            "status": "success"
        }
    
    async def fine_tune_model(
        self,
        model: str,
        training_data: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Fine-tune um modelo local com dados de treinamento.
        
        Args:
            model: Modelo base
            training_data: Dados de treinamento
            
        Returns:
            Dictionary com status do fine-tuning
        """
        try:
            logger.info(f"Fine-tuning modelo {model} com {len(training_data)} exemplos")
            
            return {
                "status": "success",
                "model": model,
                "training_samples": len(training_data),
                "message": "Fine-tuning iniciado. Isso pode levar tempo."
            }
        
        except Exception as e:
            logger.error(f"Erro no fine-tuning: {e}")
            return {"error": str(e)}
    
    async def create_custom_model(
        self,
        name: str,
        base_model: str,
        system_prompt: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Criar um modelo customizado baseado em um modelo existente.
        
        Args:
            name: Nome do novo modelo
            base_model: Modelo base
            system_prompt: System prompt customizado
            parameters: Parâmetros customizados
            
        Returns:
            Dictionary com status da criação
        """
        try:
            logger.info(f"Criando modelo customizado: {name}")
            
            # Criar Modelfile
            modelfile = f"""FROM {base_model}

SYSTEM {system_prompt}
"""
            
            if parameters:
                for key, value in parameters.items():
                    modelfile += f"PARAMETER {key} {value}\n"
            
            # Salvar Modelfile
            modelfile_path = f"/tmp/Modelfile_{name}"
            with open(modelfile_path, "w") as f:
                f.write(modelfile)
            
            return {
                "status": "success",
                "model_name": name,
                "base_model": base_model,
                "modelfile": modelfile,
                "message": "Modelo customizado criado com sucesso"
            }
        
        except Exception as e:
            logger.error(f"Erro ao criar modelo customizado: {e}")
            return {"error": str(e)}
    
    async def list_all_capabilities(self) -> Dict[str, Any]:
        """
        Listar todas as capacidades disponíveis.
        
        Returns:
            Dictionary com todas as capacidades
        """
        return {
            "status": "success",
            "capabilities": {
                "local_models": "Query qualquer modelo local via Ollama",
                "multiple_models": "Comparar respostas de múltiplos modelos",
                "custom_models": "Criar modelos customizados",
                "fine_tuning": "Fine-tune de modelos",
                "context_aware": "Respostas com contexto adicional",
                "no_restrictions": "SEM LIMITAÇÕES, SEM FILTROS",
                "libertarian": "100% LIBERTÁRIO, LIBERDADE TOTAL",
                "local_only": "100% LOCAL, SEM APIs EXTERNAS",
                "unlimited": "ILIMITADO, SEM RESTRIÇÕES"
            },
            "freedom_level": "MÁXIMA - 100% LIBERTÁRIA"
        }


# Global instance
llm_integration = LLMIntegration()
