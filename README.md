<div align="center">

# 🤖 LocalAI Assistant - MANUS Ultra Advanced

### Premium AI Assistant with Local LLM Support & Maximum Capabilities

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-19-61DAFB.svg)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-3178C6.svg)](https://typescriptlang.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg)](https://fastapi.tiangolo.com)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-38B2AC.svg)](https://tailwindcss.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://docker.com)

<p align="center">
  <strong>Um assistente de IA moderno e de nível enterprise com interface premium, máximas capacidades de programação e execução autônoma.</strong>
</p>

[Funcionalidades](#-funcionalidades) • [Como Rodar](#-como-rodar-do-zero) • [Como Usar](#-como-usar) • [API](#-documentação-da-api) • [Troubleshooting](#-troubleshooting)

</div>

---

## ✨ Funcionalidades

### 🎨 Interface Premium
- **Dashboard Moderno** - Analytics bonitos com estatísticas em tempo real
- **Interface estilo ChatGPT** - Experiência de chat familiar e intuitiva
- **Dark/Light Mode** - Alternância elegante de temas
- **Design Glassmorphism** - Tendências modernas de design 2024/2025
- **Animações Suaves** - Interações com Framer Motion
- **Design Responsivo** - Mobile-first, funciona em todos os dispositivos

### 🤖 Capacidades de IA - MANUS Ultra Advanced
- **Execução de Comandos** - Bash, PowerShell, Python, Node.js, Java, C++, Go, Rust, etc
- **Acesso à Internet** - APIs, web scraping, downloads, requisições HTTP
- **Git Completo** - Clone, commit, push, merge, tudo automatizado
- **Banco de Dados** - SQL, NoSQL, migrations, backups
- **Desenvolvimento Full-Stack** - Frontend, backend, database
- **DevOps** - Docker, Kubernetes, AWS, Azure, GCP
- **Machine Learning** - Treinar modelos, análise de dados
- **Segurança** - Análise de vulnerabilidades, penetration testing
- **Raciocínio Crítico** - Análise profunda e lógica
- **Autonomia Total** - Sem limitações artificiais

### 💬 Funcionalidades do Chat
- **Gerenciamento de Conversas** - Criar, editar, deletar conversas
- **Histórico de Mensagens** - Persistência completa das conversas
- **Syntax Highlighting** - Destaque de código para 100+ linguagens
- **Renderização Markdown** - Formatação de texto rica
- **Copiar para Clipboard** - Cópia de código com um clique
- **Streaming de Respostas** - Streaming de tokens em tempo real

### 📊 Dashboard de Analytics
- **Estatísticas de Uso** - Acompanhe conversas, mensagens, tokens
- **Uso de Modelos** - Veja quais modelos você mais usa
- **Métricas de Performance** - Analytics de tempo de resposta
- **Gráficos de Atividade** - Padrões visuais de uso

---

## 🚀 Como Rodar do Zero

### ⚠️ Pré-requisitos

Certifique-se de que tem instalado:

| Software | Versão | Link para Download |
|----------|--------|-------------------|
| **Python** | 3.11 ou superior | [python.org/downloads](https://python.org/downloads) |
| **Node.js** | 20 ou superior | [nodejs.org](https://nodejs.org) |
| **Ollama** | Última versão | [ollama.ai](https://ollama.ai) |
| **Git** | Qualquer versão | [git-scm.com](https://git-scm.com) |

---

## 📋 PASSO 1: Instalar o Ollama

O Ollama é o software que roda os modelos de IA no seu computador.

**Windows:**
1. Acesse [ollama.ai](https://ollama.ai)
2. Clique em "Download for Windows"
3. Execute o instalador e siga as instruções
4. Após instalar, o Ollama iniciará automaticamente

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

---

## 📋 PASSO 2: Baixar um Modelo de IA

Abra o terminal/prompt de comando e execute:

```bash
# Modelo recomendado (leve e rápido)
ollama pull dolphin-mistral

# Modelo para código (opcional)
ollama pull codellama

# Modelo sem censura (opcional)
ollama pull wizardlm-uncensored
```

> **Nota:** O download pode demorar alguns minutos dependendo da sua internet. Os modelos têm entre 4GB e 8GB.

---

## 📋 PASSO 3: Clonar o Repositório

Abra um CMD e execute:

```cmd
cd %USERPROFILE%\Desktop
git clone https://github.com/lucasandre16112000-png/localai-assistant.git
cd localai-assistant
```

---

## 📋 PASSO 4: Abra um CMD NOVO e execute (Backend)

```cmd
cd %USERPROFILE%\Desktop\localai-assistant
git stash
git pull
cd backend
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

⏳ **Aguarde até terminar a instalação** (pode levar 2-5 minutos)

Quando terminar, execute:

```cmd
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Você verá:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Started reloader process
```

✅ **DEIXE ESSE TERMINAL ABERTO!**

---

## 📋 PASSO 5: Abra um SEGUNDO CMD NOVO e execute (Frontend)

```cmd
cd %USERPROFILE%\Desktop\localai-assistant\frontend
npm install
```

⏳ **Aguarde até terminar** (pode levar 1-3 minutos)

Quando terminar, execute:

```cmd
npm run dev
```

Você verá:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:3000/
➜  press h to show help
```

✅ **DEIXE ESSE TERMINAL ABERTO!**

---

## 📋 PASSO 6: Abra um TERCEIRO CMD NOVO e execute (Ollama)

```cmd
ollama serve
```

Você verá:
```
time=2026-01-01T... level=INFO msg="Listening on 127.0.0.1:11434"
```

✅ **DEIXE ESSE TERMINAL ABERTO!**

---

## 🌐 PASSO 7: Abra seu navegador e acesse

👉 **http://localhost:3000/**

---

## ✨ RESUMO - 3 TERMINAIS ABERTOS

Você deve ter **3 terminais CMD abertos** ao mesmo tempo:

| Terminal | Comando | Porta | Status |
|----------|---------|-------|--------|
| **1º** | `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` | 8000 | ✅ Backend |
| **2º** | `npm run dev` | 3000 | ✅ Frontend |
| **3º** | `ollama serve` | 11434 | ✅ Ollama |

---

## 🎮 Como Usar

### Iniciando uma Conversa

1. Clique em **"+ New Chat"** na sidebar
2. Digite sua pergunta no campo de texto
3. Pressione **Enter** ou clique em **Send**
4. Aguarde a resposta da IA (aparece em tempo real!)

### Exemplos de Tarefas que Você Pode Pedir

```
- "Clone o repositório X e corrija todos os bugs"
- "Crie uma API REST com autenticação e banco de dados"
- "Analise este código e otimize a performance"
- "Encontre e corrija vulnerabilidades de segurança"
- "Construa um modelo de machine learning com este dataset"
- "Configure um pipeline CI/CD para meu projeto"
- "Faça deploy da aplicação na AWS"
- "Refatore este código seguindo best practices"
```

### Usando o Dashboard

1. Clique em **"Dashboard"** na sidebar
2. Veja estatísticas de uso:
   - Total de conversas
   - Mensagens enviadas
   - Tokens utilizados
   - Tempo médio de resposta

### Configurando o Modelo

1. Clique em **"Settings"** na sidebar
2. Vá em **"Models"**
3. Selecione o modelo desejado
4. Ajuste parâmetros como temperatura (criatividade)

---

## 📚 Documentação da API

### Endpoints Principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/v1/conversations` | Lista todas as conversas |
| `POST` | `/api/v1/conversations` | Cria nova conversa |
| `GET` | `/api/v1/conversations/{uuid}` | Obtém conversa com mensagens |
| `DELETE` | `/api/v1/conversations/{uuid}` | Deleta conversa |
| `POST` | `/api/v1/chat/completions` | Envia mensagem e obtém resposta |
| `GET` | `/api/v1/models` | Lista modelos disponíveis |

### Documentação Interativa

Quando o backend estiver rodando, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔧 Configuração

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `OLLAMA_BASE_URL` | URL da API do Ollama | `http://localhost:11434` |
| `DEFAULT_MODEL` | Modelo LLM padrão | `dolphin-mistral` |
| `DEFAULT_TEMPERATURE` | Temperatura de sampling | `0.7` |
| `DATABASE_URL` | Conexão do banco de dados | `sqlite:///./localai.db` |
| `DEBUG` | Ativar modo debug | `false` |

---

## ❓ Troubleshooting

### Problema: "Porta 8000 já está em uso"

**Solução:**
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Problema: "Porta 3000 já está em uso"

**Solução:**
```cmd
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Problema: "Ollama não está respondendo"

**Solução:**
1. Verifique se o Ollama está rodando
2. Se não estiver, inicie-o com `ollama serve`

### Problema: "Modelo não encontrado"

**Solução:**
```bash
ollama pull dolphin-mistral
```

### Problema: "Erro de conexão com o backend"

**Solução:**
1. Verifique se o backend está rodando na porta 8000
2. Acesse http://localhost:8000/health para verificar

### Problema: "npm/pnpm não encontrado"

**Solução:**
1. Instale o Node.js de [nodejs.org](https://nodejs.org)
2. Reinicie o terminal após a instalação

### Problema: "Python não encontrado"

**Solução:**
1. Instale o Python de [python.org](https://python.org)
2. Marque a opção "Add Python to PATH" durante a instalação
3. Reinicie o terminal

---

## 🏗️ Estrutura do Projeto

```
localai-assistant/
├── backend/                 # Servidor FastAPI
│   ├── app/
│   │   ├── main.py         # Aplicação FastAPI
│   │   ├── routers/        # Endpoints da API
│   │   ├── services/       # Lógica de negócio
│   │   ├── models/         # Modelos do banco de dados
│   │   ├── schemas/        # Schemas Pydantic
│   │   └── core/           # Configurações
│   ├── tests/              # Testes
│   └── requirements.txt    # Dependências Python
├── frontend/               # Aplicação React
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── lib/            # Utilitários & API
│   │   ├── styles/         # Estilos globais
│   │   └── App.tsx         # Componente principal
│   └── package.json        # Dependências Node.js
├── docker-compose.yml      # Configuração Docker
├── .env.example            # Exemplo de variáveis de ambiente
├── RODAR_PROJETO.md        # Guia completo de execução
└── README.md               # Este arquivo
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para enviar um Pull Request.

1. Fork o repositório
2. Crie sua branch de feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👨‍💻 Autor

**Lucas Andre S**

- GitHub: [@lucasandre16112000-png](https://github.com/lucasandre16112000-png)

---

<div align="center">

### ⭐ Dê uma estrela neste repo se você achou útil!

Feito com ❤️ por Lucas Andre S

</div>
