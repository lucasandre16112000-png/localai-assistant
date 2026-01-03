# 📖 Guia de Implementação - Sistema de Memória Generativa

**Versão:** 1.0.0  
**Data:** Janeiro 2026  
**Autor:** Manus AI  
**Status:** ✅ Pronto para Produção

---

## 🎯 Objetivo

Este guia fornece instruções passo-a-passo para **integrar e ativar** o Sistema de Memória Generativa no seu LocalAI Assistant.

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter:

- ✅ LocalAI Assistant clonado e funcional
- ✅ Python 3.11+
- ✅ Banco de dados SQLite criado
- ✅ Backend rodando na porta 8000
- ✅ Frontend rodando na porta 3000

---

## 🚀 Passo 1: Instalar Dependências

### 1.1 Atualizar requirements.txt

O arquivo `requirements.txt` já foi atualizado com as dependências necessárias:

```bash
langchain==0.1.0
langchain-community==0.0.10
numpy==1.24.3
scikit-learn==1.3.2
faiss-cpu==1.7.4
sentence-transformers==2.2.2
```

### 1.2 Instalar no seu ambiente

```bash
cd backend
pip install -r requirements.txt
```

**Tempo estimado:** 5-10 minutos (primeira vez)

---

## 🔧 Passo 2: Atualizar o Banco de Dados

### 2.1 Executar Migrações

O sistema de memória usa novas tabelas. Execute as migrações:

```bash
# No backend
python -m alembic upgrade head
```

**Ou manualmente (se não usar Alembic):**

```python
# No seu script de inicialização
from app.core.database import Base, engine
from app.models.memory import Memory, MemorySummary, UserPattern, ContextWindow

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Execute
asyncio.run(init_db())
```

---

## 📝 Passo 3: Registrar os Routers

### 3.1 Adicionar Routers ao Main

Edite `backend/app/main.py`:

```python
from fastapi import FastAPI
from app.routers import chat, conversations, memory

app = FastAPI()

# Registrar routers
app.include_router(chat.router)
app.include_router(conversations.router)
app.include_router(memory.router)  # ← ADICIONAR ESTA LINHA
```

### 3.2 Verificar Importação

Certifique-se de que o arquivo `backend/app/routers/memory.py` existe.

---

## 🧠 Passo 4: Integrar Serviços

### 4.1 Usar Memory Service no Chat

Edite `backend/app/routers/chat.py` para usar memória:

```python
from app.services.memory_service import MemoryService
from app.services.rag_service import RAGService
from app.services.auto_summary_service import AutoSummaryService, PatternLearningService

memory_service = MemoryService()
rag_service = RAGService(memory_service)
auto_summary_service = AutoSummaryService()
pattern_learning_service = PatternLearningService()

@router.post("/completions-stream")
async def chat_completion_stream(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    # ... código existente ...
    
    # ADICIONAR: Usar RAG para aumentar prompt
    augmented_prompt = await rag_service.augment_prompt(
        original_prompt=request.message,
        conversation_id=conv_uuid,
        db=db,
        include_context=True
    )
    
    # ADICIONAR: Usar prompt aumentado
    # ... gerar resposta ...
    
    # ADICIONAR: Extrair insights
    await rag_service.extract_and_store_insights(
        conversation_id=conv_id,
        user_message=request.message,
        assistant_response=full_response,
        db=db
    )
    
    # ADICIONAR: Auto-summarizar se necessário
    await auto_summary_service.auto_summarize_if_needed(db, conv_id)
    
    # ADICIONAR: Aprender padrões
    await pattern_learning_service.learn_from_conversation(db, conv_id)
```

---

## 🔌 Passo 5: Usar a API de Memória

### 5.1 Criar Memória

```bash
curl -X POST "http://localhost:8000/memory/memories" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": 1,
    "memory_type": "preference",
    "content": "Usuário prefere respostas técnicas",
    "importance_score": 0.8
  }'
```

### 5.2 Gerar Resumo

```bash
curl -X POST "http://localhost:8000/memory/conversations/1/summarize"
```

### 5.3 Detectar Preferências

```bash
curl -X POST "http://localhost:8000/memory/conversations/1/detect-preferences"
```

### 5.4 Obter Contexto Otimizado

```bash
curl -X GET "http://localhost:8000/memory/conversations/1/optimal-context?max_tokens=2048"
```

### 5.5 Obter Estado da Memória

```bash
curl -X GET "http://localhost:8000/memory/conversations/1/state"
```

---

## 🧪 Passo 6: Testar o Sistema

### 6.1 Teste Básico

```python
# test_memory.py
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.services.memory_service import MemoryService
from app.schemas.memory import MemoryCreate

async def test_memory():
    # Criar engine
    engine = create_async_engine("sqlite+aiosqlite:///test.db")
    
    # Criar tabelas
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Criar sessão
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as db:
        # Testar serviço
        memory_service = MemoryService()
        
        # Criar memória
        memory_data = MemoryCreate(
            memory_type="test",
            content="Teste de memória",
            importance_score=0.8
        )
        
        memory = await memory_service.create_memory(db, 1, memory_data)
        print(f"✅ Memória criada: {memory.uuid}")
        
        # Recuperar memória
        retrieved = await memory_service.get_memory(db, memory.uuid)
        print(f"✅ Memória recuperada: {retrieved.content}")

# Executar teste
asyncio.run(test_memory())
```

### 6.2 Teste de Conversa Completa

1. Abra o frontend em `http://localhost:3000`
2. Crie uma nova conversa
3. Envie 10+ mensagens
4. Observe o resumo automático ser gerado
5. Verifique as preferências detectadas via API

---

## 📊 Passo 7: Monitorar e Ajustar

### 7.1 Verificar Logs

```bash
# Ver logs do backend
tail -f backend/logs/app.log | grep memory
```

### 7.2 Ajustar Parâmetros

Edite `backend/app/services/memory_service.py`:

```python
class MemoryService:
    max_context_tokens = 2048      # Aumentar para mais contexto
    summary_threshold = 10          # Reduzir para resumir mais frequentemente
```

### 7.3 Limpar Memórias Antigas

```bash
curl -X POST "http://localhost:8000/memory/cleanup?days_old=30"
```

---

## 🎯 Passo 8: Integração no Frontend (Opcional)

### 8.1 Exibir Padrões Aprendidos

Adicione no `frontend/src/components/Chat/Chat.tsx`:

```typescript
const [userPatterns, setUserPatterns] = useState([]);

useEffect(() => {
  // Buscar padrões do usuário
  fetch(`/api/memory/patterns`)
    .then(res => res.json())
    .then(data => setUserPatterns(data.patterns));
}, []);

// Exibir padrões
<div className="user-patterns">
  <h3>Padrões Aprendidos</h3>
  {userPatterns.map(pattern => (
    <div key={pattern.uuid}>
      <p>{pattern.description}</p>
      <p>Confiança: {(pattern.confidence_score * 100).toFixed(0)}%</p>
    </div>
  ))}
</div>
```

### 8.2 Exibir Resumo

```typescript
const [summary, setSummary] = useState(null);

useEffect(() => {
  // Buscar resumo
  fetch(`/api/memory/conversations/${conversationId}/summary`)
    .then(res => res.json())
    .then(data => setSummary(data));
}, [conversationId]);

// Exibir resumo
{summary && (
  <div className="conversation-summary">
    <h3>Resumo da Conversa</h3>
    <p>{summary.summary}</p>
    <ul>
      {summary.key_points.map((point, idx) => (
        <li key={idx}>{point}</li>
      ))}
    </ul>
  </div>
)}
```

---

## 🔍 Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'langchain'"

**Solução:**
```bash
pip install langchain langchain-community
```

### Problema: "FAISS not installed"

**Solução:**
```bash
pip install faiss-cpu
# Ou para GPU:
pip install faiss-gpu
```

### Problema: Memórias não estão sendo criadas

**Verificar:**
1. Banco de dados está criado? `SELECT * FROM memories;`
2. Routers estão registrados? Verificar `main.py`
3. Logs de erro? `tail -f backend/logs/app.log`

### Problema: Resumos muito longos

**Solução:**
```python
# Reduzir max_tokens no prompt
summary_prompt = f"Summarize in 2 sentences: {text}"
```

---

## 📈 Próximos Passos

Após implementar o sistema básico, você pode:

1. **Adicionar Persistência de Embeddings** - Salvar vetores FAISS em banco de dados
2. **Implementar Feedback Loop** - Usuário avalia qualidade de resumos
3. **Adicionar Múltiplos Usuários** - Isolar memórias por usuário
4. **Integrar com APIs Externas** - Enriquecer contexto com dados externos
5. **Adicionar Visualizações** - Dashboard de padrões e insights

---

## 📚 Referências

- [LangChain Documentation](https://python.langchain.com/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Sentence Transformers](https://www.sbert.net/)
- [RAG Papers](https://arxiv.org/abs/2005.11401)

---

## ✅ Checklist de Implementação

- [ ] Dependências instaladas
- [ ] Banco de dados atualizado
- [ ] Routers registrados
- [ ] Serviços integrados no chat
- [ ] Testes passando
- [ ] API funcionando
- [ ] Logs monitorados
- [ ] Frontend atualizado (opcional)
- [ ] Parâmetros ajustados
- [ ] Documentação revisada

---

## 🎉 Conclusão

Parabéns! Você agora tem um **Sistema de Memória Generativa completo** rodando no seu LocalAI Assistant!

**Próxima conversa será muito mais inteligente e personalizada!** 🚀

---

**Desenvolvido com ❤️ por Manus AI**
