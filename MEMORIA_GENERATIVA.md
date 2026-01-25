# 🧠 Sistema de Memória Generativa - LocalAI Assistant

**Versão:** 1.0.0  
**Data:** Janeiro 2026  
**Autor:** Manus AI  
**Status:** ✅ Implementado e Funcional

---

## 📋 Visão Geral

O **Sistema de Memória Generativa** é um componente avançado que permite ao LocalAI Assistant **lembrar, aprender e personalizar** interações com o usuário. É como dar à IA a capacidade de ter memória de longo prazo e aprender com o tempo.

### O que o Sistema Faz?

✅ **Lembra conversas anteriores** - Armazena e recupera contexto de conversas passadas  
✅ **Gera resumos automáticos** - Comprime conversas longas em resumos concisos  
✅ **Aprende padrões** - Identifica preferências e comportamentos do usuário  
✅ **Personaliza respostas** - Adapta respostas baseado no perfil do usuário  
✅ **Otimiza tokens** - Gerencia contexto de forma eficiente  
✅ **Recuperação aumentada** - Usa RAG para melhorar qualidade das respostas  
✅ **Limpeza automática** - Remove memórias antigas e irrelevantes  

---

## 🏗️ Arquitetura

### Componentes Principais

```
┌─────────────────────────────────────────────────────────┐
│           LocalAI Assistant - Memória Generativa        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Frontend (React + TypeScript)            │  │
│  │  - Exibe histórico de conversas                  │  │
│  │  - Mostra padrões aprendidos                     │  │
│  └──────────────────────────────────────────────────┘  │
│                         ↓                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Backend (FastAPI)                        │  │
│  │  ┌────────────────────────────────────────────┐  │  │
│  │  │ Memory Service                             │  │  │
│  │  │ - Gerencia memórias                        │  │  │
│  │  │ - Gera resumos                             │  │  │
│  │  │ - Aprende padrões                          │  │  │
│  │  └────────────────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────────────────┐  │  │
│  │  │ RAG Service                                │  │  │
│  │  │ - Recupera contexto                        │  │  │
│  │  │ - Aumenta prompts                          │  │  │
│  │  │ - Personaliza respostas                    │  │  │
│  │  └────────────────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────────────────┐  │  │
│  │  │ LLM Service                                │  │  │
│  │  │ - Comunica com Ollama                      │  │  │
│  │  └────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
│                         ↓                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Database (SQLite)                        │  │
│  │  - Conversations                                 │  │
│  │  - Messages                                      │  │
│  │  - Memories                                      │  │
│  │  - MemorySummaries                               │  │
│  │  - UserPatterns                                  │  │
│  │  - ContextWindows                                │  │
│  └──────────────────────────────────────────────────┘  │
│                         ↓                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │         LLM Local (Ollama)                       │  │
│  │  - Gera respostas                                │  │
│  │  - Cria resumos                                  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Modelos de Dados

### 1. Memory (Memória)

Armazena lembranças individuais de conversas.

```python
{
    "id": 1,
    "uuid": "abc-123",
    "conversation_id": 1,
    "memory_type": "summary|pattern|preference|context",
    "content": "O usuário prefere respostas técnicas",
    "importance_score": 0.8,  # 0-1
    "relevance_score": 0.7,   # 0-1
    "access_count": 5,
    "is_active": true,
    "created_at": "2026-01-03T10:00:00",
    "last_accessed": "2026-01-03T15:30:00"
}
```

### 2. MemorySummary (Resumo de Conversa)

Armazena resumos comprimidos de conversas.

```python
{
    "id": 1,
    "uuid": "summary-123",
    "conversation_id": 1,
    "summary": "Usuário perguntou sobre Python...",
    "key_points": ["Python", "Algoritmos", "Performance"],
    "entities": {
        "topics": ["Python", "Programação"],
        "people": [],
        "places": [],
        "concepts": ["Algoritmos", "Performance"]
    },
    "original_message_count": 15,
    "compression_ratio": 3.5  # 3.5x compressão
}
```

### 3. UserPattern (Padrão do Usuário)

Armazena padrões aprendidos sobre o usuário.

```python
{
    "id": 1,
    "uuid": "pattern-123",
    "pattern_name": "prefers_technical_answers",
    "pattern_type": "preference",
    "description": "Usuário prefere explicações técnicas detalhadas",
    "pattern_data": {
        "technical_keyword_ratio": 0.65,
        "average_response_length": "long"
    },
    "confidence_score": 0.85,  # 0-1
    "frequency": 12,
    "created_at": "2026-01-03T10:00:00",
    "last_used": "2026-01-03T15:30:00"
}
```

### 4. ContextWindow (Janela de Contexto)

Gerencia contexto otimizado para cada conversa.

```python
{
    "id": 1,
    "uuid": "context-123",
    "conversation_id": 1,
    "context_content": "Resumo + Memórias + Padrões",
    "context_type": "summary|recent_messages|relevant_memories|user_profile",
    "token_count": 512,
    "relevance_score": 0.9,
    "created_at": "2026-01-03T10:00:00"
}
```

---

## 🔌 API de Memória

### Endpoints Disponíveis

#### Gerenciamento de Memórias

```bash
# Criar memória
POST /memory/memories
{
    "conversation_id": 1,
    "memory_type": "preference",
    "content": "Usuário prefere respostas breves",
    "importance_score": 0.8
}

# Obter memória
GET /memory/memories/{memory_uuid}

# Atualizar memória
PUT /memory/memories/{memory_uuid}
{
    "importance_score": 0.9,
    "is_active": true
}

# Deletar memória
DELETE /memory/memories/{memory_uuid}

# Listar memórias de uma conversa
GET /memory/conversations/{conversation_id}/memories?memory_type=preference&limit=10
```

#### Resumos

```bash
# Gerar resumo
POST /memory/conversations/{conversation_id}/summarize

# Obter último resumo
GET /memory/conversations/{conversation_id}/summary
```

#### Padrões de Usuário

```bash
# Aprender padrão
POST /memory/patterns
{
    "pattern_name": "prefers_technical_answers",
    "pattern_type": "preference",
    "description": "Usuário prefere respostas técnicas",
    "pattern_data": {"level": "advanced"},
    "confidence_score": 0.8
}

# Listar padrões
GET /memory/patterns?min_confidence=0.5&limit=10

# Detectar preferências de uma conversa
POST /memory/conversations/{conversation_id}/detect-preferences
```

#### Contexto

```bash
# Criar janela de contexto
POST /memory/context-windows
{
    "conversation_id": 1,
    "context_content": "...",
    "context_type": "summary",
    "token_count": 512
}

# Obter contexto otimizado
GET /memory/conversations/{conversation_id}/optimal-context?max_tokens=2048

# Obter estado da memória
GET /memory/conversations/{conversation_id}/state
```

#### Manutenção

```bash
# Limpar memórias antigas
POST /memory/cleanup?days_old=30
```

---

## 🚀 Como Usar

### 1. Habilitar Memória em uma Conversa

```python
# No backend, ao criar uma nova conversa:
from app.services.memory_service import MemoryService

memory_service = MemoryService()

# Criar memória inicial
memory_data = MemoryCreate(
    memory_type="context",
    content="Iniciando nova conversa",
    importance_score=0.5
)

memory = await memory_service.create_memory(db, conversation_id, memory_data)
```

### 2. Gerar Resumo Automático

```python
# Após 10+ mensagens, gerar resumo:
summary = await memory_service.generate_conversation_summary(db, conversation_id)

if summary:
    print(f"Resumo gerado: {summary.summary}")
    print(f"Pontos-chave: {summary.key_points}")
```

### 3. Detectar Preferências

```python
# Analisar conversa e detectar padrões:
patterns = await memory_service.detect_user_preferences(db, conversation_id)

for pattern in patterns:
    print(f"Padrão detectado: {pattern.pattern_name}")
    print(f"Confiança: {pattern.confidence_score}")
```

### 4. Usar RAG para Melhorar Respostas

```python
from app.services.rag_service import RAGService

rag_service = RAGService(memory_service)

# Aumentar prompt com contexto
augmented_prompt = await rag_service.augment_prompt(
    original_prompt="Como fazer X?",
    conversation_id=1,
    db=db,
    include_context=True
)

# Usar prompt aumentado para gerar resposta
response = await llm_service.generate(augmented_prompt)
```

### 5. Obter Contexto Otimizado

```python
# Obter melhor contexto dentro do limite de tokens:
context = await memory_service.get_optimal_context(
    db,
    conversation_id=1,
    max_tokens=2048
)

print(context)
```

---

## 📈 Fluxo de Funcionamento

### Fluxo Padrão de Conversa com Memória

```
1. Usuário envia mensagem
   ↓
2. Backend recebe mensagem
   ↓
3. Recuperar contexto relevante (RAG)
   ├─ Buscar memórias relacionadas
   ├─ Obter último resumo
   ├─ Recuperar padrões do usuário
   └─ Montar contexto otimizado
   ↓
4. Aumentar prompt com contexto
   ↓
5. Enviar para LLM (Ollama)
   ↓
6. LLM gera resposta
   ↓
7. Extrair insights da conversa
   ├─ Detectar preferências
   ├─ Identificar tópicos
   └─ Armazenar como memória
   ↓
8. Retornar resposta ao usuário
   ↓
9. Verificar se precisa gerar resumo
   └─ Se >10 mensagens, gerar resumo
   ↓
10. Atualizar estado da memória
```

---

## 🎯 Casos de Uso

### 1. Personalização de Respostas

**Antes (sem memória):**
```
Usuário: "Como fazer um loop em Python?"
IA: "Um loop em Python pode ser feito com for ou while..."
```

**Depois (com memória):**
```
Usuário: "Como fazer um loop em Python?"
IA: [Detecta que usuário prefere respostas técnicas]
IA: "Um loop em Python pode ser feito com:
    1. for loop com iteração
    2. while loop com condição
    3. List comprehension para casos simples
    
    Exemplo avançado com generators:
    def my_generator():
        for i in range(10):
            yield i
    ..."
```

### 2. Contexto Persistente

**Conversa 1:**
```
Usuário: "Estou aprendendo Python"
IA: "Ótimo! Você é iniciante ou tem experiência?"
Usuário: "Sou iniciante"
```

**Conversa 2 (dias depois):**
```
Usuário: "Como fazer uma função?"
IA: [Recupera que usuário é iniciante em Python]
IA: "Como você é iniciante, vou explicar de forma simples..."
```

### 3. Resumos Automáticos

**Conversa longa (30 mensagens) sobre Python:**
```
Resumo gerado:
"Usuário aprendeu sobre:
- Variáveis e tipos de dados
- Loops (for e while)
- Funções e escopo
- Tratamento de erros

Próximos tópicos sugeridos:
- Módulos e pacotes
- Programação orientada a objetos
- Trabalhando com arquivos"
```

---

## ⚙️ Configuração

### Variáveis de Ambiente

```bash
# .env
MEMORY_MAX_CONTEXT_TOKENS=2048
MEMORY_SUMMARY_THRESHOLD=10
MEMORY_CLEANUP_DAYS=30
MEMORY_MIN_IMPORTANCE=0.3
```

### Parâmetros de Tuning

```python
# backend/app/services/memory_service.py
class MemoryService:
    max_context_tokens = 2048      # Máximo de tokens no contexto
    summary_threshold = 10          # Gerar resumo após N mensagens
    
# backend/app/services/rag_service.py
class RAGService:
    max_retrieved_documents = 5     # Máximo de documentos recuperados
    similarity_threshold = 0.3      # Limiar de similaridade
```

---

## 📊 Métricas e Monitoramento

### Métricas Importantes

```python
# Obter estado da memória
GET /memory/conversations/{conversation_id}/state

Retorna:
{
    "conversation_id": 1,
    "total_memories": 25,
    "active_memories": 20,
    "summaries": [...],
    "user_patterns": [...],
    "context_windows": [...],
    "last_updated": "2026-01-03T15:30:00"
}
```

### Qualidade da Resposta

```python
# Avaliar qualidade
evaluation = await rag_service.evaluate_response_quality(
    user_query="Como fazer X?",
    assistant_response="Resposta...",
    retrieved_context="Contexto..."
)

# Retorna:
{
    "query_length": 15,
    "response_length": 250,
    "context_used": true,
    "context_length": 500,
    "quality_score": 0.85
}
```

---

## 🔒 Privacidade e Segurança

- ✅ **Dados locais:** Tudo é armazenado localmente, não é enviado para nenhum servidor
- ✅ **Sem rastreamento:** Nenhum rastreamento de usuário
- ✅ **Controle total:** Você controla o que é memorizado
- ✅ **Limpeza automática:** Memórias antigas são removidas automaticamente

---

## 🐛 Troubleshooting

### Problema: Memórias não estão sendo criadas

**Solução:**
```python
# Verificar se o serviço está inicializado
memory_service = MemoryService()

# Verificar se a conversa existe
conversation = await db.get(Conversation, conversation_id)
assert conversation is not None
```

### Problema: Resumos muito longos

**Solução:**
```python
# Ajustar threshold
memory_service.summary_threshold = 5  # Resumir após 5 mensagens
```

### Problema: Contexto muito grande

**Solução:**
```python
# Reduzir max_tokens
context = await memory_service.get_optimal_context(
    db,
    conversation_id=1,
    max_tokens=1024  # Reduzido de 2048
)
```

---

## 📚 Referências

- [LangChain Documentation](https://python.langchain.com/)
- [RAG (Retrieval Augmented Generation)](https://arxiv.org/abs/2005.11401)
- [Memory in LLMs](https://arxiv.org/abs/2308.01399)

---

## 🎉 Conclusão

O Sistema de Memória Generativa transforma o LocalAI Assistant de uma IA sem memória para uma IA que **aprende, lembra e personaliza**. Isso resulta em:

✅ Conversas mais naturais e contextualizadas  
✅ Respostas personalizadas baseadas no perfil do usuário  
✅ Melhor compreensão do contexto  
✅ Uso mais eficiente de tokens  
✅ Experiência de usuário superior  

**Desenvolvido com ❤️ por Manus AI**
