# 🤖 LocalAI Assistant

Um **assistente de IA premium e moderno** que roda completamente localmente no seu computador, sem depender de servidores na nuvem. É como ter um **ChatGPT pessoal, privado e gratuito** rodando no seu Windows.

![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Node.js](https://img.shields.io/badge/Node.js-18%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Funcionalidades Principais

✅ **Chat em Tempo Real** - Respostas instantâneas com streaming  
✅ **Histórico de Conversas** - Salva e recupera todas as conversas  
✅ **Botão STOP Funcional** - Para a IA de responder quando quiser  
✅ **Interface Moderna** - Design estilo ChatGPT com tema escuro  
✅ **Múltiplos Modelos** - Suporte a diferentes modelos de IA  
✅ **Configurações Avançadas** - Controle total sobre parâmetros  
✅ **Dashboard com Analytics** - Visualize estatísticas de uso  
✅ **100% Local** - Seus dados nunca saem do seu computador  
✅ **Gratuito e Open Source** - Sem custos, sem assinaturas  

---

## 🚀 Como Rodar (Guia Completo para Iniciantes)

### **Pré-requisitos**

Antes de começar, você precisa ter instalado no seu Windows:

1. **Python 3.11+** - [Baixe aqui](https://www.python.org/downloads/)
2. **Node.js 18+** - [Baixe aqui](https://nodejs.org/)
3. **Git** - [Baixe aqui](https://git-scm.com/)
4. **Ollama** - [Baixe aqui](https://ollama.ai/)

> **Dica:** Durante a instalação do Python, **marque a opção "Add Python to PATH"**

---

## 📋 Passo-a-Passo Completo

### **PASSO 1: Preparar o Projeto**

Abra um **CMD (Prompt de Comando)** e execute:

```cmd
cd %USERPROFILE%\Desktop
git clone https://github.com/lucasandre16112000-png/localai-assistant.git
cd localai-assistant
```

**Pressione ENTER uma única vez após colar**

---

### **PASSO 2: Rodar o Backend (Primeiro Terminal)**

Abra um **NOVO CMD** e copie/cole TUDO isso de uma vez:

```cmd
cd %USERPROFILE%\Desktop\localai-assistant
cd backend
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Pressione ENTER uma única vez após colar**

**Você verá algo assim quando funcionar:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

✅ **DEIXE ESTE TERMINAL ABERTO!**

---

### **PASSO 3: Rodar o Frontend (Segundo Terminal)**

Abra um **NOVO CMD** e copie/cole TUDO isso de uma vez:

```cmd
cd %USERPROFILE%\Desktop\localai-assistant\frontend
npm install
npm run dev
```

**Pressione ENTER uma única vez após colar**

**Você verá algo assim quando funcionar:**
```
VITE v4.x.x  ready in xxx ms

➜  Local:   http://localhost:3000/
```

✅ **DEIXE ESTE TERMINAL ABERTO!**

---

### **PASSO 4: Rodar o Ollama (Terceiro Terminal)**

Abra um **NOVO CMD** e copie/cole:

```cmd
ollama serve
```

**Pressione ENTER uma única vez após colar**

**Você verá algo assim quando funcionar:**
```
time=2024-01-03T10:00:00.000Z level=INFO msg="Listening on 127.0.0.1:11434"
```

✅ **DEIXE ESTE TERMINAL ABERTO!**

---

### **PASSO 5: Acessar no Navegador**

Abra seu navegador (Chrome, Firefox, Edge, etc.) e acesse:

```
http://localhost:3000/
```

🎉 **Pronto! O LocalAI Assistant está rodando!**

---

## 🧪 Testando as Funcionalidades

### **Teste 1: Enviar uma Mensagem**
1. Digite uma pergunta no campo de chat
2. Clique em "Send" ou pressione Enter
3. A IA deve responder em tempo real

### **Teste 2: Botão STOP**
1. Envie uma mensagem longa
2. Enquanto a IA está respondendo, clique no botão "Stop"
3. A resposta deve parar imediatamente
4. A resposta parcial deve ser salva

### **Teste 3: Histórico de Conversas**
1. Crie uma nova conversa (clique em "New Chat")
2. Envie algumas mensagens
3. Observe na barra lateral esquerda - as conversas devem aparecer
4. Recarregue a página - as conversas devem continuar lá

### **Teste 4: Múltiplas Conversas**
1. Crie 2 conversas diferentes
2. Envie mensagens diferentes em cada uma
3. Clique entre elas - cada uma deve manter seu histórico

---

## 🐛 Troubleshooting (Soluções para Problemas)

### **Problema: "Python não encontrado"**
**Solução:** Python não foi adicionado ao PATH. Reinstale marcando "Add Python to PATH"

### **Problema: "npm não encontrado"**
**Solução:** Node.js não foi instalado. Baixe em https://nodejs.org/

### **Problema: "Porta 8000 em uso"**
**Solução:** Feche outro programa usando a porta 8000 ou execute:
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### **Problema: "Porta 3000 em uso"**
**Solução:** Feche outro programa usando a porta 3000 ou execute:
```cmd
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### **Problema: "Ollama não responde"**
**Solução:** Certifique-se de que o Ollama está rodando no terceiro terminal

### **Problema: "Conversas não aparecem na sidebar"**
**Solução:** 
1. Abra o Console do navegador (F12)
2. Verifique se há erros
3. Recarregue a página (Ctrl+R)

### **Problema: "Botão STOP não funciona"**
**Solução:**
1. Verifique se o backend está rodando
2. Abra o Console (F12) e procure por erros
3. Reinicie o backend

---

## 📁 Estrutura do Projeto

```
localai-assistant/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── main.py         # Aplicação principal
│   │   ├── routers/        # Endpoints da API
│   │   ├── services/       # Lógica de negócio
│   │   ├── models/         # Modelos do banco de dados
│   │   └── schemas/        # Schemas de validação
│   ├── requirements.txt    # Dependências Python
│   └── venv/              # Ambiente virtual (criado automaticamente)
│
├── frontend/               # React + TypeScript Frontend
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── lib/          # Utilitários e API client
│   │   ├── App.tsx       # Componente principal
│   │   └── main.tsx      # Entrada da aplicação
│   ├── package.json      # Dependências Node.js
│   └── vite.config.ts    # Configuração do Vite
│
└── README.md             # Este arquivo
```

---

## 🔧 Configuração Avançada

### **Mudar o Modelo de IA**

1. Vá em **Settings** (⚙️) no canto superior direito
2. Selecione um modelo diferente na lista
3. Clique em "Save"

### **Ajustar Parâmetros de Resposta**

Em **Settings**, você pode ajustar:
- **Temperature**: Criatividade da IA (0.0 = determinístico, 2.0 = criativo)
- **Top P**: Diversidade de tokens
- **Top K**: Número de tokens considerados
- **Max Tokens**: Comprimento máximo da resposta

---

## 📊 API REST

O backend fornece uma API REST completa. Exemplos:

### **Listar Conversas**
```bash
curl http://localhost:8000/api/v1/conversations/
```

### **Enviar Mensagem**
```bash
curl -X POST http://localhost:8000/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Olá!",
    "model": "dolphin-mistral",
    "temperature": 0.7
  }'
```

### **Documentação Interativa**
Acesse http://localhost:8000/docs para ver a documentação Swagger completa

---

## 🧠 Sistema de Memória Generativa (Avançado)

O LocalAI Assistant inclui um sistema de memória generativa que:
- Lembra de conversas anteriores
- Aprende suas preferências
- Faz resumos automáticos
- Personaliza respostas

Veja `MEMORIA_GENERATIVA.md` para mais detalhes.

---

## 📝 Logs e Debug

### **Ver Logs do Backend**
Os logs são salvos em `backend/logs/app.log`

### **Ver Logs do Frontend**
Abra o Console do navegador (F12) e procure por mensagens com ✅ ou ❌

---

## 🤝 Contribuindo

Encontrou um bug? Quer adicionar uma feature? Abra uma issue ou pull request!

---

## 📄 Licença

Este projeto é licenciado sob a MIT License - veja o arquivo LICENSE para detalhes.

---

## 🙋 Suporte

Tem dúvidas? Verifique:
1. Este README
2. A seção de Troubleshooting
3. Os arquivos de documentação (MEMORIA_GENERATIVA.md, etc.)
4. Abra uma issue no GitHub

---

## 🎯 Roadmap

- [ ] Suporte a múltiplos usuários
- [ ] Integração com APIs externas
- [ ] Exportar conversas em PDF
- [ ] Temas customizáveis
- [ ] Suporte a voice input/output
- [ ] Mobile app

---

## 🙏 Agradecimentos

Desenvolvido com ❤️ por **Lucas Andre S** e **Manus AI**

Powered by:
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [Ollama](https://ollama.ai/)
- [LangChain](https://python.langchain.com/)

---

**Versão:** 1.0.0  
**Última atualização:** Janeiro 2026  
**Status:** ✅ Pronto para Produção

---

## 🚀 Comece Agora!

Pronto para começar? Siga o **Passo-a-Passo Completo** acima e aproveite seu assistente de IA local!

**Dúvidas? Verifique a seção de Troubleshooting ou abra uma issue!**
