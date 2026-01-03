# 🎯 GUIA COMPLETO DO ZERO - LocalAI Assistant

**Para Iniciantes - Sem Exceção de Nada**

**Versão:** 2.0.0 (Super Completo)  
**Autor:** Manus AI  
**Data:** Janeiro 2026  
**Nível:** 🟢 Iniciante (Qualquer pessoa consegue)

---

## 📌 ÍNDICE

1. [Instalação de Pré-requisitos](#instalação-de-pré-requisitos)
2. [Verificação de Instalação](#verificação-de-instalação)
3. [Download do Projeto](#download-do-projeto)
4. [Rodar o Projeto](#rodar-o-projeto)
5. [Acessar no Navegador](#acessar-no-navegador)
6. [Testes de Funcionalidade](#testes-de-funcionalidade)
7. [Troubleshooting](#troubleshooting)

---

# 1️⃣ INSTALAÇÃO DE PRÉ-REQUISITOS

Você precisa instalar 4 programas. Se já tem todos, pule para a seção [Verificação de Instalação](#verificação-de-instalação).

## 1.1 - Instalar Python 3.11+

### Passo 1: Baixar Python

1. Acesse: **https://www.python.org/downloads/**
2. Clique em **"Download Python 3.12.x"** (ou versão mais recente)
3. Salve o arquivo na sua Área de Trabalho

### Passo 2: Executar o Instalador

1. **Abra o arquivo** `python-3.12.x.exe` que você baixou
2. **IMPORTANTE:** Marque a caixa **"Add Python to PATH"** ⭐
3. Clique em **"Install Now"**
4. Aguarde a instalação terminar
5. Clique em **"Close"**

✅ **Python instalado!**

---

## 1.2 - Instalar Node.js 20+

### Passo 1: Baixar Node.js

1. Acesse: **https://nodejs.org/**
2. Clique em **"Download LTS"** (versão recomendada)
3. Salve o arquivo na sua Área de Trabalho

### Passo 2: Executar o Instalador

1. **Abra o arquivo** `node-v20.x.x.msi` que você baixou
2. Clique em **"Next"** várias vezes
3. Clique em **"Install"**
4. Aguarde a instalação terminar
5. Clique em **"Finish"**

✅ **Node.js instalado!**

---

## 1.3 - Instalar Git

### Passo 1: Baixar Git

1. Acesse: **https://git-scm.com/download/win**
2. Clique em **"Download"** (versão 64-bit)
3. Salve o arquivo na sua Área de Trabalho

### Passo 2: Executar o Instalador

1. **Abra o arquivo** `Git-2.x.x-64-bit.exe` que você baixou
2. Clique em **"Next"** várias vezes
3. Mantenha as opções padrão e clique em **"Install"**
4. Aguarde a instalação terminar
5. Clique em **"Finish"**

✅ **Git instalado!**

---

## 1.4 - Instalar Ollama

### Passo 1: Baixar Ollama

1. Acesse: **https://ollama.ai/**
2. Clique em **"Download for Windows"**
3. Salve o arquivo na sua Área de Trabalho

### Passo 2: Executar o Instalador

1. **Abra o arquivo** `OllamaSetup.exe` que você baixou
2. Clique em **"Install"**
3. Aguarde a instalação terminar
4. O Ollama vai iniciar automaticamente

✅ **Ollama instalado!**

### Passo 3: Baixar um Modelo de IA

1. **Pressione** `Win + R` (abre a janela "Executar")
2. Digite: `cmd` e pressione **Enter**
3. Uma janela preta (Prompt de Comando) vai abrir
4. Digite este comando e pressione **Enter**:
   ```cmd
   ollama pull dolphin-mistral
   ```
5. ⏳ **Aguarde o download terminar** (pode levar 10-20 minutos, dependendo da sua internet)
6. Você verá uma mensagem como: `success`

✅ **Modelo de IA baixado!**

---

# 2️⃣ VERIFICAÇÃO DE INSTALAÇÃO

Vamos verificar se tudo foi instalado corretamente.

## Verificar Python

1. **Pressione** `Win + R`
2. Digite: `cmd` e pressione **Enter**
3. Digite este comando:
   ```cmd
   python --version
   ```
4. Você deve ver: `Python 3.11.x` (ou versão mais recente)

✅ **Python OK!**

---

## Verificar Node.js

1. Na mesma janela do CMD, digite:
   ```cmd
   node --version
   ```
2. Você deve ver: `v20.x.x` (ou versão mais recente)

✅ **Node.js OK!**

---

## Verificar Git

1. Na mesma janela do CMD, digite:
   ```cmd
   git --version
   ```
2. Você deve ver: `git version 2.x.x`

✅ **Git OK!**

---

## Verificar npm

1. Na mesma janela do CMD, digite:
   ```cmd
   npm --version
   ```
2. Você deve ver: `10.x.x` (ou versão mais recente)

✅ **npm OK!**

---

# 3️⃣ DOWNLOAD DO PROJETO

Agora vamos baixar o projeto do GitHub.

## Passo 1: Abrir o Prompt de Comando

1. **Pressione** `Win + R`
2. Digite: `cmd` e pressione **Enter**

## Passo 2: Navegar até a Área de Trabalho

Digite este comando e pressione **Enter**:
```cmd
cd %USERPROFILE%\Desktop
```

## Passo 3: Clonar o Projeto

Digite este comando e pressione **Enter**:
```cmd
git clone https://github.com/lucasandre16112000-png/localai-assistant.git
```

⏳ **Aguarde o download terminar** (pode levar 1-2 minutos)

Você verá uma mensagem como: `Cloning into 'localai-assistant'...`

## Passo 4: Entrar na Pasta do Projeto

Digite este comando e pressione **Enter**:
```cmd
cd localai-assistant
```

✅ **Projeto baixado!**

---

# 4️⃣ RODAR O PROJETO

Agora vamos rodar os 3 componentes do projeto. **Você precisa de 3 janelas de CMD abertas ao mesmo tempo!**

---

## TERMINAL 1: Rodar o Backend (Servidor)

### Passo 1: Abrir um NOVO CMD

1. **Pressione** `Win + R`
2. Digite: `cmd` e pressione **Enter**

### Passo 2: Navegar até a Pasta do Backend

Digite estes comandos (um por um, pressionando Enter após cada um):

```cmd
cd %USERPROFILE%\Desktop\localai-assistant
cd backend
```

### Passo 3: Criar um Ambiente Virtual Python

Digite este comando e pressione **Enter**:
```cmd
python -m venv venv
```

⏳ **Aguarde alguns segundos**

### Passo 4: Ativar o Ambiente Virtual

Digite este comando e pressione **Enter**:
```cmd
venv\Scripts\activate
```

Você verá `(venv)` no início da linha. Isso significa que o ambiente virtual está ativo.

### Passo 5: Instalar as Dependências

Digite este comando e pressione **Enter**:
```cmd
pip install -r requirements.txt
```

⏳ **Aguarde a instalação terminar** (pode levar 3-5 minutos)

Você verá mensagens como: `Collecting fastapi`, `Installing collected packages`, etc.

Quando terminar, você verá: `Successfully installed ...`

### Passo 6: Rodar o Backend

Digite este comando e pressione **Enter**:
```cmd
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Você verá mensagens como:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Started reloader process
```

✅ **DEIXE ESTE TERMINAL ABERTO!** Não feche!

---

## TERMINAL 2: Rodar o Frontend (Interface)

### Passo 1: Abrir um NOVO CMD (diferente do anterior)

1. **Pressione** `Win + R`
2. Digite: `cmd` e pressione **Enter**

### Passo 2: Navegar até a Pasta do Frontend

Digite estes comandos (um por um, pressionando Enter após cada um):

```cmd
cd %USERPROFILE%\Desktop\localai-assistant\frontend
```

### Passo 3: Instalar as Dependências

Digite este comando e pressione **Enter**:
```cmd
npm install
```

⏳ **Aguarde a instalação terminar** (pode levar 2-3 minutos)

Você verá mensagens como: `npm notice`, `added X packages`, etc.

### Passo 4: Rodar o Frontend

Digite este comando e pressione **Enter**:
```cmd
npm run dev
```

Você verá mensagens como:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:3000/
```

✅ **DEIXE ESTE TERMINAL ABERTO!** Não feche!

---

## TERMINAL 3: Rodar o Ollama (IA)

### Passo 1: Abrir um NOVO CMD (diferente dos anteriores)

1. **Pressione** `Win + R`
2. Digite: `cmd` e pressione **Enter**

### Passo 2: Rodar o Ollama

Digite este comando e pressione **Enter**:
```cmd
ollama serve
```

Você verá uma mensagem como:
```
time=2026-01-03T... level=INFO msg="Listening on 127.0.0.1:11434"
```

✅ **DEIXE ESTE TERMINAL ABERTO!** Não feche!

---

# 5️⃣ ACESSAR NO NAVEGADOR

Agora que tudo está rodando, abra seu navegador (Chrome, Edge, Firefox, etc.) e acesse:

👉 **http://localhost:3000/**

Você verá a interface do LocalAI Assistant!

---

# 6️⃣ TESTES DE FUNCIONALIDADE

Vamos testar se tudo está funcionando corretamente.

## Teste 1: Criar uma Conversa

1. Clique em **"New Chat"** (botão azul)
2. Digite uma pergunta simples, por exemplo: `Olá, como você está?`
3. Clique em **"Send"** (ou pressione Enter)
4. ⏳ Aguarde a resposta da IA
5. ✅ A resposta deve aparecer na tela

---

## Teste 2: Conversa Aparece na Sidebar

1. Após enviar a mensagem, olhe para a **barra lateral esquerda**
2. ✅ Você deve ver a conversa listada com o título da pergunta

---

## Teste 3: Botão STOP Funciona

1. Clique em **"New Chat"**
2. Digite uma pergunta longa: `Explique a história da computação em detalhes com exemplos`
3. Clique em **"Send"**
4. Enquanto a IA está respondendo, clique em **"Stop"** (o botão muda de "Send" para "Stop")
5. ✅ A resposta deve parar imediatamente

---

## Teste 4: Histórico Persiste

1. Recarregue a página (pressione F5)
2. ✅ As conversas anteriores devem continuar na barra lateral
3. ✅ Você deve conseguir clicar nelas e ver o histórico

---

# 7️⃣ TROUBLESHOOTING

Se algo não funcionar, siga as soluções abaixo.

## ❌ Problema: "Porta 8000 já está em uso"

**Solução:**

1. Abra um novo CMD
2. Digite este comando:
   ```cmd
   netstat -ano | findstr :8000
   ```
3. Você verá um número (PID) na última coluna
4. Digite este comando (substitua XXXX pelo número):
   ```cmd
   taskkill /PID XXXX /F
   ```
5. Feche o terminal do backend e abra um novo
6. Execute novamente: `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

---

## ❌ Problema: "Porta 3000 já está em uso"

**Solução:**

1. Abra um novo CMD
2. Digite este comando:
   ```cmd
   netstat -ano | findstr :3000
   ```
3. Você verá um número (PID) na última coluna
4. Digite este comando (substitua XXXX pelo número):
   ```cmd
   taskkill /PID XXXX /F
   ```
5. Feche o terminal do frontend e abra um novo
6. Execute novamente: `npm run dev`

---

## ❌ Problema: "Ollama não está respondendo"

**Solução:**

1. Verifique se o Ollama está rodando (você deve ver o ícone na bandeja do sistema, perto do relógio)
2. Se não estiver, abra um novo CMD e execute: `ollama serve`
3. Se ainda não funcionar, reinicie o computador

---

## ❌ Problema: "npm: command not found"

**Solução:**

1. Você não instalou o Node.js corretamente
2. Desinstale o Node.js e instale novamente seguindo a seção [1.2 - Instalar Node.js 20+](#12---instalar-nodejs-20)
3. **Reinicie o computador** após a instalação
4. Abra um novo CMD e tente novamente

---

## ❌ Problema: "python: command not found"

**Solução:**

1. Você não instalou o Python corretamente ou não marcou "Add Python to PATH"
2. Desinstale o Python e instale novamente seguindo a seção [1.1 - Instalar Python 3.11+](#11---instalar-python-311)
3. **Importante:** Marque a caixa "Add Python to PATH" durante a instalação
4. **Reinicie o computador** após a instalação
5. Abra um novo CMD e tente novamente

---

## ❌ Problema: "Conversas não aparecem na sidebar"

**Solução:**

1. Certifique-se de que o backend está rodando (você deve ver mensagens no terminal 1)
2. Recarregue a página (pressione F5)
3. Se ainda não funcionar, feche todos os 3 terminais
4. Abra um novo CMD e navegue até: `cd %USERPROFILE%\Desktop\localai-assistant\backend`
5. Delete a pasta `venv` e o arquivo `localai.db`:
   ```cmd
   rmdir /s /q venv
   del localai.db
   ```
6. Comece do zero seguindo a seção [TERMINAL 1: Rodar o Backend](#terminal-1-rodar-o-backend-servidor)

---

## ❌ Problema: "Botão STOP não funciona"

**Solução:**

1. Certifique-se de que está usando a versão mais recente do projeto
2. Abra um CMD e execute:
   ```cmd
   cd %USERPROFILE%\Desktop\localai-assistant
   git pull
   ```
3. Recarregue a página no navegador (pressione F5)
4. Se ainda não funcionar, limpe o cache do navegador (Ctrl+Shift+Del)

---

# ✅ RESUMO FINAL

Se você seguiu todos os passos acima, você deve ter:

✅ Python instalado e funcionando  
✅ Node.js instalado e funcionando  
✅ Git instalado e funcionando  
✅ Ollama instalado e funcionando  
✅ Projeto baixado da GitHub  
✅ Backend rodando na porta 8000  
✅ Frontend rodando na porta 3000  
✅ Ollama rodando na porta 11434  
✅ Interface acessível em http://localhost:3000/  
✅ Conversas sendo salvas  
✅ Botão STOP funcionando  

---

# 🎉 PARABÉNS!

Você conseguiu rodar o LocalAI Assistant com sucesso! Agora você tem um assistente de IA rodando **100% localmente no seu computador**, sem depender de nenhum servidor na nuvem.

**Aproveite e explore todas as funcionalidades!**

---

**Desenvolvido com ❤️ por Manus AI**

Versão: 2.0.0 | Data: Janeiro 2026 | Status: ✅ 100% Completo
