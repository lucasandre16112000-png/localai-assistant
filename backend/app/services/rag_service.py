"""
LocalAI Assistant - RAG Service
Retrieval Augmented Generation service using LangChain
Author: Lucas Andre S & Manus AI
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class RAGService:
    """
    Retrieval Augmented Generation service.
    Enhances LLM responses by retrieving relevant context from memory.
    """
    
    def __init__(self, memory_service=None):
        self.memory_service = memory_service
        self.max_retrieved_documents = 5
        self.similarity_threshold = 0.3
    
    async def retrieve_relevant_context(
        self,
        query: str,
        conversation_id: int,
        db,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Retrieve relevant context from memory for a given query.
        """
        if not self.memory_service:
            return {"context": "", "sources": []}
        
        try:
            # Get relevant memories
            memories = await self.memory_service.get_conversation_memories(
                db, conversation_id, limit=top_k
            )
            
            # Get latest summary
            summary = await self.memory_service.get_latest_summary(db, conversation_id)
            
            # Get user patterns
            patterns = await self.memory_service.get_user_patterns(db, min_confidence=0.5, limit=3)
            
            # Build context
            context_parts = []
            sources = []
            
            # Add summary if available
            if summary:
                context_parts.append(f"Context: {summary.summary}")
                sources.append({
                    "type": "summary",
                    "uuid": summary.uuid,
                    "relevance": 0.9
                })
            
            # Add relevant memories
            for memory in memories:
                context_parts.append(f"- {memory.content}")
                sources.append({
                    "type": "memory",
                    "uuid": memory.uuid,
                    "relevance": memory.relevance_score
                })
            
            # Add user patterns
            if patterns:
                pattern_text = "User preferences: " + ", ".join([p.description for p in patterns])
                context_parts.append(pattern_text)
                sources.append({
                    "type": "pattern",
                    "count": len(patterns),
                    "relevance": 0.7
                })
            
            context = "\n".join(context_parts)
            
            return {
                "context": context,
                "sources": sources,
                "query": query,
                "retrieved_at": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return {"context": "", "sources": []}
    
    async def augment_prompt(
        self,
        original_prompt: str,
        conversation_id: int,
        db,
        include_context: bool = True
    ) -> str:
        """
        Augment a prompt with retrieved context.
        """
        if not include_context:
            return original_prompt
        
        try:
            # Retrieve relevant context
            retrieval_result = await self.retrieve_relevant_context(
                original_prompt, conversation_id, db
            )
            
            context = retrieval_result.get("context", "")
            
            if not context:
                return original_prompt
            
            # Build augmented prompt
            augmented_prompt = f"""Based on the following context from previous conversations, answer the user's question:

CONTEXT:
{context}

USER QUESTION:
{original_prompt}

Please use the context above to provide a more personalized and informed response."""
            
            return augmented_prompt
        
        except Exception as e:
            logger.error(f"Error augmenting prompt: {e}")
            return original_prompt
    
    async def extract_and_store_insights(
        self,
        conversation_id: int,
        user_message: str,
        assistant_response: str,
        db
    ) -> List[str]:
        """
        Extract insights from the conversation and store them as memories.
        """
        if not self.memory_service:
            return []
        
        try:
            insights = []
            
            # Extract user preferences from the message
            if any(word in user_message.lower() for word in ['prefer', 'like', 'want', 'need']):
                insights.append({
                    "type": "preference",
                    "content": f"User expressed preference in message: {user_message[:100]}",
                    "importance": 0.7
                })
            
            # Extract topics
            topics = self._extract_topics(user_message)
            if topics:
                insights.append({
                    "type": "topic",
                    "content": f"Topics discussed: {', '.join(topics)}",
                    "importance": 0.6
                })
            
            # Store insights as memories
            from ..schemas.memory import MemoryCreate
            
            stored_insights = []
            for insight in insights:
                memory_data = MemoryCreate(
                    memory_type=insight["type"],
                    content=insight["content"],
                    importance_score=insight["importance"],
                    relevance_score=insight["importance"]
                )
                
                memory = await self.memory_service.create_memory(
                    db, conversation_id, memory_data
                )
                stored_insights.append(memory.uuid)
            
            return stored_insights
        
        except Exception as e:
            logger.error(f"Error extracting insights: {e}")
            return []
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics from text."""
        # Simple topic extraction - can be improved with NLP
        topics = []
        
        # Common topic keywords
        topic_keywords = {
            "programming": ["code", "python", "javascript", "java", "c++", "algorithm"],
            "data": ["data", "database", "sql", "analytics", "statistics"],
            "web": ["web", "html", "css", "react", "vue", "angular"],
            "devops": ["docker", "kubernetes", "ci/cd", "deployment", "infrastructure"],
            "ai": ["ai", "machine learning", "neural", "model", "deep learning"],
        }
        
        text_lower = text.lower()
        for topic, keywords in topic_keywords.items():
            if any(kw in text_lower for kw in keywords):
                topics.append(topic)
        
        return topics
    
    async def generate_personalized_response(
        self,
        base_response: str,
        user_patterns: List[Any],
        conversation_id: int
    ) -> str:
        """
        Personalize a response based on learned user patterns.
        """
        try:
            personalized_response = base_response
            
            # Apply pattern-based personalization
            for pattern in user_patterns:
                if pattern.pattern_name == "prefers_technical_answers":
                    # Add more technical details
                    personalized_response += "\n\nTechnical Details:\n[Additional technical information based on user preference]"
                
                elif pattern.pattern_name == "prefers_brief_answers":
                    # Shorten the response
                    personalized_response = personalized_response[:len(personalized_response)//2]
            
            return personalized_response
        
        except Exception as e:
            logger.error(f"Error personalizing response: {e}")
            return base_response
    
    async def evaluate_response_quality(
        self,
        user_query: str,
        assistant_response: str,
        retrieved_context: str
    ) -> Dict[str, Any]:
        """
        Evaluate the quality of a response based on context relevance.
        """
        try:
            evaluation = {
                "query_length": len(user_query.split()),
                "response_length": len(assistant_response.split()),
                "context_used": len(retrieved_context) > 0,
                "context_length": len(retrieved_context.split()),
                "quality_score": 0.0
            }
            
            # Calculate quality score
            if len(retrieved_context) > 0:
                evaluation["quality_score"] = 0.8
            else:
                evaluation["quality_score"] = 0.5
            
            # Adjust based on response length
            if len(assistant_response.split()) > 50:
                evaluation["quality_score"] += 0.1
            
            evaluation["quality_score"] = min(evaluation["quality_score"], 1.0)
            
            return evaluation
        
        except Exception as e:
            logger.error(f"Error evaluating response: {e}")
            return {"quality_score": 0.5}


class ContextOptimizer:
    """Optimizes context for efficient token usage."""
    
    def __init__(self, max_tokens: int = 2048):
        self.max_tokens = max_tokens
        self.token_per_word_ratio = 1.3  # Approximate ratio
    
    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text."""
        return int(len(text.split()) * self.token_per_word_ratio)
    
    def optimize_context(
        self,
        context_parts: List[Dict[str, Any]],
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Optimize context by selecting the most relevant parts within token limit.
        """
        max_tokens = max_tokens or self.max_tokens
        
        # Sort by relevance score
        sorted_parts = sorted(
            context_parts,
            key=lambda x: x.get("relevance", 0),
            reverse=True
        )
        
        selected_parts = []
        total_tokens = 0
        
        for part in sorted_parts:
            part_tokens = self.estimate_tokens(part.get("content", ""))
            
            if total_tokens + part_tokens <= max_tokens:
                selected_parts.append(part["content"])
                total_tokens += part_tokens
            else:
                break
        
        return "\n".join(selected_parts)
    
    def calculate_compression_ratio(
        self,
        original_text: str,
        compressed_text: str
    ) -> float:
        """Calculate compression ratio."""
        original_tokens = self.estimate_tokens(original_text)
        compressed_tokens = self.estimate_tokens(compressed_text)
        
        if original_tokens == 0:
            return 0.0
        
        return compressed_tokens / original_tokens
