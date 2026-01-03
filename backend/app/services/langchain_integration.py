"""
LocalAI Assistant - LangChain Integration
Advanced context management and RAG using LangChain
Author: Lucas Andre S & Manus AI
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.schema import Document
    from langchain.vectorstores import FAISS
    from langchain.embeddings import HuggingFaceEmbeddings
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("LangChain not installed. Install with: pip install langchain langchain-community")

logger = logging.getLogger(__name__)


class LangChainContextManager:
    """
    Advanced context management using LangChain.
    Provides semantic search and intelligent context retrieval.
    """
    
    def __init__(self):
        if not LANGCHAIN_AVAILABLE:
            raise ImportError("LangChain is not installed. Please install it with: pip install langchain")
        
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", " ", ""]
        )
        self.vector_stores: Dict[int, FAISS] = {}  # conversation_id -> FAISS
    
    async def initialize_vector_store(
        self,
        conversation_id: int,
        documents: List[str]
    ) -> None:
        """Initialize or update vector store for a conversation."""
        try:
            # Split documents into chunks
            docs = [Document(page_content=doc) for doc in documents]
            split_docs = self.text_splitter.split_documents(docs)
            
            if not split_docs:
                logger.warning(f"No documents to split for conversation {conversation_id}")
                return
            
            # Create or update FAISS vector store
            if conversation_id in self.vector_stores:
                # Add new documents to existing store
                texts = [doc.page_content for doc in split_docs]
                self.vector_stores[conversation_id].add_texts(texts)
            else:
                # Create new vector store
                texts = [doc.page_content for doc in split_docs]
                self.vector_stores[conversation_id] = FAISS.from_texts(
                    texts,
                    self.embeddings
                )
            
            logger.info(f"Vector store initialized for conversation {conversation_id} with {len(split_docs)} chunks")
        
        except Exception as e:
            logger.error(f"Error initializing vector store: {e}")
            raise
    
    async def semantic_search(
        self,
        query: str,
        conversation_id: int,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Perform semantic search on conversation documents."""
        try:
            if conversation_id not in self.vector_stores:
                logger.warning(f"No vector store for conversation {conversation_id}")
                return []
            
            # Search similar documents
            results = self.vector_stores[conversation_id].similarity_search_with_score(
                query,
                k=top_k
            )
            
            # Format results
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "relevance_score": 1 - score,  # Convert distance to similarity
                    "retrieved_at": datetime.utcnow().isoformat()
                })
            
            return formatted_results
        
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            return []
    
    async def build_context_chain(
        self,
        query: str,
        conversation_id: int,
        max_results: int = 5
    ) -> str:
        """Build a context chain for the query."""
        try:
            results = await self.semantic_search(query, conversation_id, max_results)
            
            if not results:
                return ""
            
            # Build context string
            context_parts = [
                f"Relevant context from previous conversations:\n"
            ]
            
            for i, result in enumerate(results, 1):
                relevance = result["relevance_score"]
                content = result["content"]
                context_parts.append(
                    f"\n[{i}] (Relevance: {relevance:.2%})\n{content}"
                )
            
            return "\n".join(context_parts)
        
        except Exception as e:
            logger.error(f"Error building context chain: {e}")
            return ""
    
    async def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities from text."""
        try:
            # Simple entity extraction
            # Can be enhanced with more sophisticated NLP
            entities = {
                "topics": [],
                "people": [],
                "places": [],
                "concepts": [],
                "technologies": []
            }
            
            # Technology keywords
            tech_keywords = {
                "technologies": [
                    "python", "javascript", "java", "c++", "rust",
                    "react", "vue", "angular", "django", "flask",
                    "docker", "kubernetes", "aws", "gcp", "azure",
                    "sql", "mongodb", "postgresql", "redis"
                ]
            }
            
            text_lower = text.lower()
            for entity_type, keywords in tech_keywords.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        entities[entity_type].append(keyword)
            
            return entities
        
        except Exception as e:
            logger.error(f"Error extracting entities: {e}")
            return {}
    
    async def summarize_documents(
        self,
        documents: List[str],
        max_length: int = 200
    ) -> str:
        """Summarize a list of documents."""
        try:
            # Combine documents
            combined_text = "\n\n".join(documents)
            
            # Simple extractive summarization
            sentences = combined_text.split(".")
            
            # Score sentences by relevance
            scored_sentences = []
            for sentence in sentences:
                words = sentence.split()
                score = len(words)  # Simple scoring
                scored_sentences.append((sentence.strip(), score))
            
            # Select top sentences
            sorted_sentences = sorted(scored_sentences, key=lambda x: x[1], reverse=True)
            summary_sentences = [s[0] for s in sorted_sentences[:3]]
            
            summary = ". ".join(summary_sentences)
            
            # Truncate if too long
            if len(summary) > max_length:
                summary = summary[:max_length] + "..."
            
            return summary
        
        except Exception as e:
            logger.error(f"Error summarizing documents: {e}")
            return ""
    
    async def get_conversation_summary(
        self,
        conversation_id: int,
        max_length: int = 300
    ) -> Optional[str]:
        """Get a summary of the entire conversation."""
        try:
            if conversation_id not in self.vector_stores:
                return None
            
            # Retrieve all documents
            all_docs = self.vector_stores[conversation_id].docstore._dict.values()
            documents = [doc.page_content for doc in all_docs]
            
            if not documents:
                return None
            
            # Summarize
            summary = await self.summarize_documents(documents, max_length)
            return summary
        
        except Exception as e:
            logger.error(f"Error getting conversation summary: {e}")
            return None
    
    def clear_vector_store(self, conversation_id: int) -> bool:
        """Clear vector store for a conversation."""
        try:
            if conversation_id in self.vector_stores:
                del self.vector_stores[conversation_id]
                logger.info(f"Vector store cleared for conversation {conversation_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error clearing vector store: {e}")
            return False


class ContextChainBuilder:
    """Build sophisticated context chains for improved responses."""
    
    def __init__(self, langchain_manager: LangChainContextManager):
        self.langchain_manager = langchain_manager
    
    async def build_full_context(
        self,
        query: str,
        conversation_id: int,
        user_patterns: List[Any],
        recent_messages: List[str],
        max_tokens: int = 2048
    ) -> Dict[str, Any]:
        """Build a comprehensive context for the query."""
        try:
            context_parts = []
            token_count = 0
            
            # 1. Add user patterns
            if user_patterns:
                patterns_text = "User Preferences:\n" + "\n".join([
                    f"- {p.description}" for p in user_patterns
                ])
                context_parts.append(patterns_text)
                token_count += len(patterns_text.split())
            
            # 2. Add recent messages
            if recent_messages and token_count < max_tokens * 0.7:
                recent_text = "Recent Context:\n" + "\n".join(recent_messages[-3:])
                context_parts.append(recent_text)
                token_count += len(recent_text.split())
            
            # 3. Add semantic search results
            if token_count < max_tokens * 0.8:
                semantic_context = await self.langchain_manager.build_context_chain(
                    query, conversation_id, max_results=3
                )
                if semantic_context:
                    context_parts.append(semantic_context)
                    token_count += len(semantic_context.split())
            
            # 4. Add conversation summary
            if token_count < max_tokens * 0.9:
                summary = await self.langchain_manager.get_conversation_summary(
                    conversation_id, max_length=200
                )
                if summary:
                    context_parts.append(f"Conversation Summary:\n{summary}")
                    token_count += len(summary.split())
            
            # Build final context
            full_context = "\n\n".join(context_parts)
            
            return {
                "context": full_context,
                "token_count": token_count,
                "max_tokens": max_tokens,
                "utilization_ratio": token_count / max_tokens,
                "components": len(context_parts),
                "built_at": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error building full context: {e}")
            return {
                "context": "",
                "token_count": 0,
                "error": str(e)
            }


class AdaptiveContextSelector:
    """Intelligently select the most relevant context based on query and history."""
    
    def __init__(self):
        self.query_history = []
    
    async def select_optimal_context(
        self,
        query: str,
        available_contexts: List[Dict[str, Any]],
        max_tokens: int = 2048
    ) -> List[Dict[str, Any]]:
        """Select the most relevant contexts within token limit."""
        try:
            # Score contexts by relevance to query
            scored_contexts = []
            
            for context in available_contexts:
                score = self._calculate_relevance_score(query, context)
                scored_contexts.append((context, score))
            
            # Sort by score
            sorted_contexts = sorted(scored_contexts, key=lambda x: x[1], reverse=True)
            
            # Select contexts within token limit
            selected = []
            total_tokens = 0
            
            for context, score in sorted_contexts:
                context_tokens = context.get("token_count", 100)
                
                if total_tokens + context_tokens <= max_tokens:
                    selected.append(context)
                    total_tokens += context_tokens
                else:
                    break
            
            return selected
        
        except Exception as e:
            logger.error(f"Error selecting optimal context: {e}")
            return []
    
    def _calculate_relevance_score(
        self,
        query: str,
        context: Dict[str, Any]
    ) -> float:
        """Calculate relevance score between query and context."""
        try:
            query_words = set(query.lower().split())
            context_text = context.get("content", "").lower()
            
            # Count matching words
            matches = sum(1 for word in query_words if word in context_text)
            
            # Calculate score
            score = matches / max(len(query_words), 1)
            
            # Factor in explicit relevance score if available
            if "relevance_score" in context:
                score = (score + context["relevance_score"]) / 2
            
            return min(score, 1.0)
        
        except Exception as e:
            logger.error(f"Error calculating relevance score: {e}")
            return 0.0
