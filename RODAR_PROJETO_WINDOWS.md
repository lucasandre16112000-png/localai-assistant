> [!IMPORTANT]
> **GUIA ATUALIZADO E CORRIGIDO (Janeiro 2026)**
> Este guia foi revisado e corrigido pela Manus AI para garantir que o projeto funcione 100% no Windows.

# 🚀 Como Rodar o LocalAI Assistant no Windows (Guia Completo)

**Autor:** Lucas Andre S & Manus AI
**Versão Corrigida:** 1.1.0

---

## ⚠️ PASSO 1: Pré-requisitos Essenciais

Antes de começar, **garanta que você tem os seguintes programas instalados** no seu Windows. Se já tiver, pode pular para o próximo passo.

| Software | Versão Mínima | Link para Download |
| :--- | :--- | :--- |
| **Python** | 3.11 ou superior | [python.org/downloads](https://python.org/downloads) |
| **Node.js** | 20 ou superior | [nodejs.org](https://nodejs.org) |
| **Ollama** | Última versão | [ollama.ai](https://ollama.ai) |
| **Git** | Qualquer versão | [git-scm.com/download/win](https://git-scm.com/download/win) |

> [!TIP]
> Durante a instalação do Python, marque a caixa **"Add Python to PATH"**.
> Após instalar tudo, **reinicie o seu computador** para garantir que os programas sejam reconhecidos no sistema.

---

## 📥 PASSO 2: Baixar o Projeto Corrigido

Eu já realizei todas as correções no seu repositório. Agora você precisa baixar a versão mais recente.

1.  **Abra o Prompt de Comando (CMD)**:
    - Pressione `Win + R`, digite `cmd` e pressione Enter.

2.  **Navegue até a Área de Trabalho** e clone o projeto:
    ```cmd
    cd %USERPROFILE%\Desktop
    git clone https://github.com/lucasandre16112000-png/localai-assistant.git
    cd localai-assistant
    ```

> [!NOTE]
> Se você já tinha o projeto, delete a pasta antiga ou use o comando `git pull` dentro da pasta para baixar as atualizações que eu fiz.

---

## 🤖 PASSO 3: Instalar e Rodar o Ollama (Servidor de IA)

O Ollama é o programa que vai rodar os modelos de inteligência artificial no seu PC.

1.  **Instale o Ollama**:
    - Acesse [ollama.ai](https://ollama.ai) e baixe o instalador para Windows.
    - Execute o instalador. Ele vai rodar em segundo plano.

2.  **Baixe um Modelo de IA**:
    - Abra um **novo CMD** e execute o comando abaixo para baixar o modelo recomendado (leve e rápido).
    ```cmd
    ollama pull dolphin-mistral
    ```
    - O download pode demorar alguns minutos (o modelo tem cerca de 4GB).

3.  **Deixe o Ollama Rodando**:
    - O Ollama já deve estar rodando. Você verá um ícone dele na bandeja do sistema (perto do relógio).

---

## ⚙️ PASSO 4: Rodar o Backend (O Cérebro da Aplicação)

O backend é o servidor que conecta a interface com a IA.

1.  **Abra um NOVO Prompt de Comando (CMD)**.

2.  **Navegue até a pasta do backend** e instale as dependências:
    ```cmd
    cd %USERPROFILE%\Desktop\localai-assistant\backend
    
    rem Cria um ambiente virtual para o Python
    python -m venv venv
    
    rem Ativa o ambiente virtual
    venv\Scripts\activate
    
    rem Instala as bibliotecas necessárias
    pip install --upgrade pip
    pip install -r requirements.txt
    ```
    - ⏳ **Aguarde a instalação terminar** (pode levar de 2 a 5 minutos).

3.  **Inicie o servidor do backend**:
    ```cmd
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

4.  Você verá uma mensagem de sucesso. **DEIXE ESTE TERMINAL ABERTO!**
    ```
    INFO:     Uvicorn running on http://0.0.0.0:8000
    ```

---

## 🎨 PASSO 5: Rodar o Frontend (A Interface Gráfica)

O frontend é a interface bonita que você vê no navegador.

1.  **Abra um SEGUNDO Prompt de Comando (CMD)**.

2.  **Navegue até a pasta do frontend** e instale as dependências:
    ```cmd
    cd %USERPROFILE%\Desktop\localai-assistant\frontend
    
    rem Instala as bibliotecas necessárias
    npm install
    ```
    - ⏳ **Aguarde a instalação terminar** (pode levar de 1 a 3 minutos).

3.  **Inicie o servidor do frontend**:
    ```cmd
    npm run dev
    ```

4.  Você verá uma mensagem de sucesso. **DEIXE ESTE SEGUNDO TERMINAL ABERTO!**
    ```
    VITE v5.x.x  ready in xxx ms
    
    ➜  Local:   http://localhost:3000/
    ```

---

## ✅ PASSO 6: Acesse a Aplicação!

Agora que tudo está rodando, abra seu navegador (Chrome, Edge, etc.) e acesse o link:

👉 **http://localhost:3000/**

---

## 📊 Resumo dos Terminais

Você precisa manter **2 terminais CMD abertos** o tempo todo para a aplicação funcionar:

| Terminal | Aplicação | Comando Rodando |
| :--- | :--- | :--- |
| **1º CMD** | ✅ **Backend** | `python -m uvicorn app.main:app --reload ...` |
| **2º CMD** | ✅ **Frontend** | `npm run dev` |

O **Ollama** roda em segundo plano e não precisa de um terminal aberto.

---

## 🔧 Solução de Problemas Comuns

- **"Porta 8000 já está em uso"**: Feche o terminal do backend, abra um novo e rode os comandos do PASSO 4 novamente.
- **"Porta 3000 já está em uso"**: Feche o terminal do frontend, abra um novo e rode os comandos do PASSO 5 novamente.
- **"Ollama não responde"**: Verifique se o ícone do Ollama está na bandeja do sistema. Se não, procure por "Ollama" no menu Iniciar e abra-o.

Se encontrar qualquer outro problema, pode me perguntar!
