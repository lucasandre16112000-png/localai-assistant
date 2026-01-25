# 🤖 LocalAI Assistant

**A Premium and Modern AI Assistant** that runs completely locally on your computer, without depending on cloud servers. It's like having a **personal, private, and free ChatGPT** running on your Windows.

![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Node.js](https://img.shields.io/badge/Node.js-18%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

1. [Quick Start (For Everyone)](#quick-start-for-everyone)
2. [Prerequisites - What to Install First](#prerequisites---what-to-install-first)
3. [Step-by-Step Installation Guide](#step-by-step-installation-guide)
4. [How to Use](#how-to-use)
5. [Features](#features)
6. [Technology Stack](#technology-stack)
7. [Project Structure](#project-structure)
8. [Troubleshooting](#troubleshooting)
9. [API Documentation](#api-documentation)

---

## 🚀 Quick Start (For Everyone)

### The Easiest Way - Just 2 Clicks! ⚡

If you just want to run the application without any technical knowledge:

1. **Install Prerequisites** (Python, Node.js, Ollama) - See section below
2. **Download** the project from GitHub
3. **Double-click** `INSTALL.bat`
4. **Wait** for everything to install automatically (~3-4 minutes)
5. **Done!** The application opens automatically in your browser

**That's it!** No terminal commands needed. Everything is automatic.

### What Happens When You Click INSTALL.bat:

```
[1/7] Creating installation folder...
[2/7] Downloading project from GitHub...
[3/7] Extracting files...
[4/7] Copying files to permanent location...
[5/7] Cleaning up temporary files...
[6/7] Checking prerequisites and starting services...
      ✓ Ollama starts (20 seconds)
      ✓ Backend starts (60 seconds)
      ✓ Frontend starts (90 seconds)
[7/7] Opening browser automatically

✓ Backend running on http://localhost:8000
✓ Frontend running on http://localhost:3000
✓ Browser opens automatically
✓ Application is ready to use!
```

---

## ⚙️ Prerequisites - What to Install First

**IMPORTANT:** You MUST install these programs BEFORE running INSTALL.bat. Without them, the installer will fail.

### 1. **Python 3.11+** (Required) 🐍

**What is it?** A programming language that powers the backend AI engine.

**Why do you need it?** LocalAI Assistant backend is built with Python.

**How to install:**

1. Go to https://www.python.org/downloads/
2. Click **"Download Python 3.11"** (or the latest 3.x version)
3. Run the installer (.exe file)
4. **IMPORTANT:** At the bottom of the installer, CHECK the box that says **"Add Python to PATH"** ✓
5. Click **"Install Now"**
6. Wait for installation to complete
7. Click **"Close"**

**Verify it worked:**
- Open Command Prompt (search for "cmd" in Windows Start menu)
- Type: `python --version`
- You should see: `Python 3.11.x` or higher
- If you see an error, restart your computer and try again

---

### 2. **Node.js 18+** (Required) 📦

**What is it?** A JavaScript runtime environment.

**Why do you need it?** LocalAI Assistant frontend is built with Node.js and React.

**How to install:**

1. Go to https://nodejs.org/
2. Click the **LTS** button (Long Term Support - recommended for stability)
3. Download the Windows installer (.msi file)
4. Run the installer
5. Click **"Next"** for each step (accept all defaults)
6. Click **"Install"**
7. Wait for installation to complete
8. Click **"Finish"**

**Verify it worked:**
- Open Command Prompt (search for "cmd")
- Type: `node --version`
- You should see: `v18.x.x` or higher
- Type: `npm --version`
- You should see: `9.x.x` or higher

---

### 3. **Ollama** (Required for AI Models) 🤖

**What is it?** A local AI model runner that allows you to run AI models on your computer.

**Why do you need it?** To run AI models locally without internet connection.

**How to install:**

1. Go to https://ollama.ai/
2. Click **"Download"** and select **Windows**
3. Run the installer (.exe file)
4. Follow the installation steps (accept all defaults)
5. Ollama will start automatically
6. **IMPORTANT:** The INSTALL.bat will automatically download the AI model for you

**Verify it worked:**
- Open Command Prompt (search for "cmd")
- Type: `ollama --version`
- You should see a version number

---

### 4. **Git** (Optional but Recommended) 📚

**What is it?** A version control system.

**Why do you need it?** To easily download and update the project from GitHub.

**How to install:**

1. Go to https://git-scm.com/
2. Download the Windows installer
3. Run the installer
4. Click **"Next"** for each step (accept all defaults)
5. Click **"Install"**
6. Click **"Finish"**

---

## 📝 Step-by-Step Installation Guide

### For Complete Beginners

Follow these steps in order. Don't skip any!

#### Step 1: Install Python (5 minutes)

1. Go to https://www.python.org/downloads/
2. Click **"Download Python 3.11"** (or latest 3.x)
3. Run the downloaded .exe file
4. **CRITICAL:** Check the box **"Add Python to PATH"** ✓
5. Click **"Install Now"**
6. Wait for installation
7. Click **"Close"**

**Verify:**
- Open Command Prompt (search "cmd")
- Type: `python --version`
- Should show: `Python 3.11.x` or higher

---

#### Step 2: Install Node.js (5 minutes)

1. Go to https://nodejs.org/
2. Click **LTS** (Long Term Support)
3. Download and run the installer
4. Click **"Next"** → **"Install"** → **"Finish"**

**Verify:**
- Open Command Prompt
- Type: `node --version`
- Should show: `v18.x.x` or higher

---

#### Step 3: Install Ollama (5 minutes)

1. Go to https://ollama.ai/
2. Download and run the Windows installer
3. Follow the installation steps
4. Ollama will start automatically

**Verify:**
- Open Command Prompt
- Type: `ollama --version`
- Should show a version number

---

#### Step 4: Download LocalAI Assistant (2 minutes)

**Option A: Download as ZIP (Easiest for Beginners)**

1. Go to https://github.com/lucasandre16112000-png/localai-assistant
2. Click the green **Code** button
3. Click **Download ZIP**
4. Extract the ZIP file to your Desktop or Documents folder
5. You should now have a folder called `localai-assistant-main`

**Option B: Using Git (For Advanced Users)**

1. Open Command Prompt
2. Navigate to where you want to install:
   ```
   cd Desktop
   ```
3. Clone the repository:
   ```
   git clone https://github.com/lucasandre16112000-png/localai-assistant.git
   ```

---

#### Step 5: Run INSTALL.bat (3-4 minutes)

1. Open the `localai-assistant` (or `localai-assistant-main`) folder
2. Find the file named **`INSTALL.bat`**
3. **Double-click** it
4. A command window will open and start the installation
5. **DO NOT CLOSE** the command window - let it run!

**What you'll see:**

```
[1/7] Creating installation folder...
[2/7] Downloading project from GitHub...
[3/7] Extracting files...
[4/7] Copying files to permanent location...
[5/7] Cleaning up temporary files...
[6/7] Checking prerequisites and starting services...
      Starting Ollama service...
      [OK] Ollama started
      Waiting 20 seconds for Ollama to initialize...
      
      Starting backend server...
      Installing dependencies (this may take 2-3 minutes)...
      Waiting for backend to initialize (60 seconds)...
      [OK] Backend should be ready
      
      Starting frontend server...
      Installing dependencies (this may take 1-2 minutes)...
      Waiting for frontend to initialize (90 seconds)...
      [OK] Frontend should be ready
      
[7/7] Opening browser...
      Everything is ready! Opening browser in 5 seconds...

LOCALAI ASSISTANT IS READY!
Frontend: http://localhost:3000
Backend:  http://localhost:8000
Ollama:   http://localhost:11434
```

6. Your browser will automatically open to http://localhost:3000
7. **Done!** The application is running!

**IMPORTANT:** Keep all the command windows open while using the application. If you close them, the application will stop.

---

## 🎮 How to Use the Application

### 1. Access the Dashboard

Your browser should automatically open to http://localhost:3000

If not, manually open: http://localhost:3000

### 2. Send Your First Message

1. Type your question or message in the chat box at the bottom
2. Press **Enter** or click the **Send** button
3. Wait for the AI to respond
4. The response will stream in real-time (you'll see it appearing word by word)

### 3. Stop a Response

- Click the **STOP** button if you want to stop the AI from responding
- Useful for long responses

### 4. View Conversation History

- All conversations are saved automatically
- Click on previous conversations in the left sidebar
- View all your chat history
- Search through conversations

### 5. Change AI Model

1. Click the **Settings** (⚙️) button in the top right
2. Select a different model from the dropdown
3. Click "Save"
4. Your next messages will use the new model

### 6. Adjust AI Settings

In **Settings**, you can adjust:

- **Temperature**: Creativity level
  - 0.0 = Deterministic (same answer every time)
  - 0.7 = Balanced (default)
  - 2.0 = Very creative (random answers)

- **Top P**: Diversity of responses (0.0 - 1.0)
- **Top K**: Number of tokens to consider (1 - 100)
- **Max Tokens**: Maximum length of response (1 - 4096)

---

## ✨ Features

### 📅 Real-Time Chat
- Instant responses with streaming
- Type and get answers immediately
- See AI thinking in real-time

### 💾 Conversation History
- All conversations are saved
- Access previous chats anytime
- Search through conversation history

### ⏹️ Stop Button
- Stop the AI from responding anytime
- Useful for long responses
- Full control over responses

### 🎨 Modern Interface
- ChatGPT-style design
- Dark theme for comfortable viewing
- Responsive and intuitive UI

### 🤖 Multiple Models
- Support for different AI models
- Switch models anytime
- Optimized for local performance

### 🔒 100% Local
- Your data never leaves your computer
- No cloud servers needed
- Complete privacy

### 💰 Free and Open Source
- No costs, no subscriptions
- Open source code
- Community-driven development

---

## 🌐 Access URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:3000 | Chat interface |
| **Backend API** | http://localhost:8000 | API server |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| **Ollama** | http://localhost:11434 | Local AI model runner |

---

## 🛠️ Technology Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Axios** - HTTP client

### Backend
- **FastAPI** - Web framework
- **Python 3.11+** - Programming language
- **Uvicorn** - ASGI server
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation

### AI
- **Ollama** - Local model runner
- **Dolphin-Mistral** - Default AI model
- **LLaMA** - Alternative models

---

## 📁 Project Structure

```
localai-assistant/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── main.py         # Application entry point
│   │   ├── routers/        # API endpoints
│   │   │   ├── chat.py     # Chat completions
│   │   │   ├── conversations.py  # Conversation management
│   │   │   ├── models.py   # Available models
│   │   │   └── prompts.py  # System prompts
│   │   ├── services/       # Business logic
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Data validation
│   │   └── core/          # Configuration
│   └── requirements.txt    # Python dependencies
│
├── frontend/               # React + TypeScript Frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── lib/          # Utilities and API client
│   │   ├── App.tsx       # Main app component
│   │   └── main.tsx      # Entry point
│   ├── package.json      # Node.js dependencies
│   ├── vite.config.ts    # Vite configuration
│   └── .env.local        # Environment variables
│
├── INSTALL.bat            # Automatic installer (ONE-CLICK!)
├── README.md             # This file
└── .gitignore           # Git configuration
```

---

## 🐛 Troubleshooting

### Problem: "Python not found" or "Python is not recognized"

**Solution:**
1. Make sure Python 3.11+ is installed
2. **CRITICAL:** When installing Python, check "Add Python to PATH"
3. Restart your computer
4. Open Command Prompt and type: `python --version`
5. If it still doesn't work, uninstall Python and reinstall it
6. Make sure to check "Add Python to PATH" during installation

---

### Problem: "Node.js not found" or "npm is not recognized"

**Solution:**
1. Make sure Node.js 18+ is installed
2. Restart your computer
3. Open Command Prompt and type: `node --version`
4. If it still doesn't work, uninstall Node.js and reinstall it

---

### Problem: "Ollama not found"

**Solution:**
1. Make sure Ollama is installed from https://ollama.ai/
2. Restart your computer
3. Open Command Prompt and type: `ollama --version`
4. If it still doesn't work, uninstall Ollama and reinstall it

---

### Problem: Browser shows "ERR_CONNECTION_REFUSED"

**Solution:**
1. This means the frontend is still loading
2. Wait a few more seconds
3. Refresh the page (press F5)
4. If it still doesn't work, close the browser and wait 30 seconds
5. Open http://localhost:3000 again

---

### Problem: "Failed to send message" in the chat

**Solution:**
1. Make sure all command windows are still open
2. Check that the backend is running (you should see a command window with "Uvicorn running")
3. Check that Ollama is running (you should see a command window with "Ollama")
4. Wait a few seconds and try again
5. If it still doesn't work, close all windows and run INSTALL.bat again

---

### Problem: Installation takes too long

**Solution:**
1. This is normal! First installation takes 3-4 minutes because:
   - npm installs 476 packages (~200MB)
   - pip installs 50+ Python packages (~100MB)
   - Vite compiles React + TypeScript
   - Ollama loads the AI model
2. Next time you run it, it will be much faster (1-2 minutes)
3. Don't close any windows while it's installing

---

### Problem: Application is very slow

**Solution:**
1. Make sure you have at least 8GB of RAM
2. Close other applications to free up memory
3. Make sure your hard drive has at least 10GB free space
4. Restart your computer
5. Run INSTALL.bat again

---

### Problem: Can't find INSTALL.bat

**Solution:**
1. Make sure you extracted the ZIP file completely
2. Open the `localai-assistant` folder
3. You should see: INSTALL.bat, README.md, backend folder, frontend folder
4. If you don't see INSTALL.bat, you didn't extract the ZIP correctly
5. Try downloading and extracting again

---

## 📚 API Documentation

The backend provides a REST API for chat completions and conversation management.

### Interactive API Docs

Once the application is running, visit: http://localhost:8000/docs

This provides an interactive Swagger UI where you can test all API endpoints.

### Main Endpoints

#### Chat Completions

**Endpoint:** `POST /api/v1/chat/completions`

**Description:** Send a message and get a response

**Request:**
```json
{
  "message": "Hello, how are you?",
  "model": "dolphin-mistral",
  "temperature": 0.7,
  "max_tokens": 2048
}
```

**Response:**
```json
{
  "content": "Hello! I'm doing well, thank you for asking...",
  "conversation_id": "uuid",
  "model": "dolphin-mistral",
  "tokens": 150
}
```

#### Chat Completions (Streaming)

**Endpoint:** `POST /api/v1/chat/completions/stream`

**Description:** Send a message and get a streaming response

**Response:** Server-Sent Events (SSE) stream

---

## 📞 Support

If you have issues:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Check that all prerequisites are installed correctly
3. Make sure all command windows are open and running
4. Restart your computer
5. Run INSTALL.bat again

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Contributing

Contributions are welcome! Feel free to:

1. Report bugs
2. Suggest features
3. Submit pull requests
4. Improve documentation

---

## 🌟 Acknowledgments

- Built with FastAPI, React, and Ollama
- Inspired by ChatGPT
- Community-driven development

---

**Enjoy your local AI assistant!** 🚀
