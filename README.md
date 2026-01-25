# 🤖 LocalAI Assistant

**A Premium and Modern AI Assistant** that runs completely locally on your computer, without depending on cloud servers. It's like having a **personal, private, and free ChatGPT** running on your Windows.

![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Node.js](https://img.shields.io/badge/Node.js-18%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

1. [Quick Start (For Everyone)](#quick-start-for-everyone)
2. [What You Need to Install](#what-you-need-to-install)
3. [Step-by-Step Installation Guide](#step-by-step-installation-guide)
4. [Features](#features)
5. [How to Use](#how-to-use)
6. [Technology Stack](#technology-stack)
7. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start (For Everyone)

### The Easiest Way - 2 Clicks! ⚡

If you just want to run the application without any technical knowledge:

1. **Download** the project from GitHub
2. **Double-click** `INSTALL.bat`
3. **Wait** for everything to install automatically (10-15 minutes)
4. **Done!** The application opens automatically in your browser

**That's it!** No terminal, no commands needed. Everything is automatic.

### What Happens When You Click INSTALL.bat:

```
[1/8] Creating installation folder...
[2/8] Downloading project from GitHub...
[3/8] Extracting files...
[4/8] Copying files to permanent location...
[5/8] Cleaning up temporary files...
[6/8] Installing backend dependencies...
[7/8] Installing frontend dependencies...
[8/8] Starting servers...

✓ Backend starts (port 8000)
✓ Frontend starts (port 3000)
✓ Browser opens automatically
✓ Application is running!
```

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

### ⚙️ Advanced Settings
- Temperature control (creativity)
- Top P and Top K parameters
- Max tokens configuration
- Full control over AI behavior

### 📊 Analytics Dashboard
- View usage statistics
- Track conversation metrics
- Visual charts and reports

### 🔒 100% Local
- Your data never leaves your computer
- No cloud servers needed
- Complete privacy

### 💰 Free and Open Source
- No costs, no subscriptions
- Open source code
- Community-driven development

---

## 📦 What You Need to Install

Before running LocalAI Assistant, you need to have these programs installed on your Windows computer:

### 1. **Python** (Required)
- **What is it?** A programming language runtime
- **Why do you need it?** LocalAI Assistant backend is built with Python
- **Download:** https://www.python.org/downloads/
- **Version:** 3.11 or higher
- **Installation Steps:**
  1. Go to https://www.python.org/downloads/
  2. Click "Download Python 3.11" (or latest 3.x version)
  3. Run the installer (.exe file)
  4. **IMPORTANT:** Check the box "Add Python to PATH" ✓
  5. Click "Install Now"
  6. Wait for completion
  7. Click "Close"

**Verify Installation:**
- Open Command Prompt (search for "cmd")
- Type: `python --version`
- You should see: `Python 3.11.x` or higher

### 2. **Node.js** (Required)
- **What is it?** A JavaScript runtime environment
- **Why do you need it?** LocalAI Assistant frontend is built with Node.js
- **Download:** https://nodejs.org/
- **Version:** 18 or higher (LTS recommended)
- **Installation Steps:**
  1. Go to https://nodejs.org/
  2. Click the **LTS** button (Long Term Support)
  3. Download the Windows installer
  4. Run the installer (.msi file)
  5. Click "Next" through all steps
  6. Click "Install"
  7. Wait for completion
  8. Click "Finish"

**Verify Installation:**
- Open Command Prompt (search for "cmd")
- Type: `node --version`
- You should see: `v18.x.x` or higher

### 3. **Git** (Optional but Recommended)
- **What is it?** A version control system
- **Why do you need it?** To download the project from GitHub
- **Download:** https://git-scm.com/
- **Installation:** Click "Next" through all steps

### 4. **Ollama** (Required for AI Models)
- **What is it?** Local AI model runner
- **Why do you need it?** To run AI models locally
- **Download:** https://ollama.ai/
- **Installation:** Run the installer and follow steps
- **After Installation:** Open Ollama and download a model (e.g., `ollama pull mistral`)

---

## 📝 Step-by-Step Installation Guide

### For Complete Beginners

#### Step 1: Install Python

1. Go to https://www.python.org/downloads/
2. Click "Download Python 3.11" (or latest 3.x version)
3. Run the installer (.exe file)
4. **IMPORTANT:** Check the box "Add Python to PATH" ✓
5. Click "Install Now"
6. Wait for installation to complete
7. Click "Close"

**Verify it worked:**
- Open Command Prompt (search for "cmd" in Windows)
- Type: `python --version`
- You should see a version number like `Python 3.11.x`

#### Step 2: Install Node.js

1. Go to https://nodejs.org/
2. Click the **LTS** button (Long Term Support - recommended)
3. Download the Windows installer
4. Run the installer (.msi file)
5. Click "Next" for each step
6. Click "Install"
7. Wait for installation to complete
8. Click "Finish"

**Verify it worked:**
- Open Command Prompt (search for "cmd")
- Type: `node --version`
- You should see a version number like `v18.x.x`

#### Step 3: Install Ollama

1. Go to https://ollama.ai/
2. Download the Windows version
3. Run the installer
4. Follow the installation steps
5. After installation, open Ollama
6. Download a model (e.g., type `ollama pull mistral` in terminal)

#### Step 4: Download LocalAI Assistant

**Option A: Download as ZIP (Easiest)**
1. Go to https://github.com/lucasandre16112000-png/localai-assistant
2. Click the green **Code** button
3. Click **Download ZIP**
4. Extract the ZIP file to a folder (e.g., Desktop or Documents)

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

#### Step 5: Run INSTALL.bat

1. Open the `localai-assistant` folder
2. Find the file named `INSTALL.bat`
3. **Double-click** it
4. A command window will open
5. Wait for the installation to complete (this may take 10-15 minutes)
6. You'll see messages like:
   - `[OK] Backend dependencies installed`
   - `[OK] Frontend dependencies installed`
   - `STARTING LOCALAI ASSISTANT...`
7. Your browser will automatically open to http://localhost:3000
8. **Done!** The application is running!

---

## 🎮 How to Use the Application

### 1. Access the Dashboard
- Your browser should automatically open to http://localhost:3000
- If not, manually open: http://localhost:3000

### 2. Send Your First Message
1. Type your question or message in the chat box
2. Press Enter or click "Send"
3. Wait for the AI to respond
4. The response will stream in real-time

### 3. Stop a Response
- Click the **STOP** button if you want to stop the AI from responding
- Useful for long responses

### 4. View Conversation History
- All conversations are saved automatically
- Click on previous conversations in the sidebar
- View all your chat history

### 5. Change AI Model
1. Click the **Settings** (⚙️) button in the top right
2. Select a different model from the dropdown
3. Click "Save"
4. Your next messages will use the new model

### 6. Adjust AI Settings
In **Settings**, you can adjust:
- **Temperature**: Creativity level (0.0 = deterministic, 2.0 = creative)
- **Top P**: Diversity of responses
- **Top K**: Number of tokens to consider
- **Max Tokens**: Maximum length of response

### 7. View Analytics
- Click the **Analytics** tab to see statistics
- View conversation metrics
- See usage patterns

---

## 🌐 Access URLs

| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:3000 |
| **Backend API** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |
| **Ollama** | http://localhost:11434 |

---

## 🛠️ Technology Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Recharts** - Data visualization
- **Radix UI** - Component library

### Backend
- **FastAPI** - Web framework
- **Python 3.11+** - Programming language
- **Uvicorn** - ASGI server
- **LangChain** - AI integration
- **SQLAlchemy** - Database ORM

### AI
- **Ollama** - Local model runner
- **Mistral** - Default AI model
- **LLaMA** - Alternative models

---

## 📁 Project Structure

```
localai-assistant/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── main.py         # Application entry point
│   │   ├── routers/        # API endpoints
│   │   ├── services/       # Business logic
│   │   ├── models/         # Database models
│   │   └── schemas/        # Data validation
│   ├── requirements.txt    # Python dependencies
│   └── venv/              # Virtual environment (created by INSTALL.bat)
│
├── frontend/               # React + TypeScript Frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── lib/          # Utilities and API client
│   │   ├── App.tsx       # Main app component
│   │   └── main.tsx      # Entry point
│   ├── package.json      # Node.js dependencies
│   └── vite.config.ts    # Vite configuration
│
├── INSTALL.bat            # Automatic installer (FINAL VERSION)
├── README.md             # This file
└── docker-compose.yml    # Docker configuration (optional)
```

---

## 🐛 Troubleshooting

### Problem: "Python not found"
**Solution:**
1. Make sure Python 3.11+ is installed
2. Restart your computer
3. Open Command Prompt and type: `python --version`
4. If it still doesn't work, reinstall Python
5. Make sure you checked "Add Python to PATH" during installation

### Problem: "Node.js not found"
**Solution:**
1. Make sure Node.js 18+ is installed
2. Restart your computer
3. Open Command Prompt and type: `node --version`
4. If it still doesn't work, reinstall Node.js

### Problem: "INSTALL.bat closes immediately"
**Solution:**
1. Make sure Python and Node.js are installed
2. Check your internet connection
3. Try running as Administrator
4. Read the error messages carefully

### Problem: "Port 3000 is already in use"
**Solution:**
1. Close any other applications using port 3000
2. Or change the PORT in the frontend configuration
3. Restart INSTALL.bat

### Problem: "Port 8000 is already in use"
**Solution:**
1. Close any other applications using port 8000
2. Or change the PORT in the backend configuration
3. Restart INSTALL.bat

### Problem: "Ollama not responding"
**Solution:**
1. Make sure Ollama is installed and running
2. Download a model: `ollama pull mistral`
3. Check http://localhost:11434 in your browser
4. Restart Ollama if needed

### Problem: "Cannot find module"
**Solution:**
1. Delete the `node_modules` folder in frontend
2. Delete the `venv` folder in backend
3. Run INSTALL.bat again
4. Wait for all dependencies to install

### Problem: "Browser shows error when opening"
**Solution:**
1. Wait a bit longer - servers may still be starting
2. Refresh the page (F5)
3. Close and restart INSTALL.bat
4. Make sure ports 3000 and 8000 are not in use

### Problem: "Chat doesn't work"
**Solution:**
1. Make sure Ollama is running with a model loaded
2. Check the browser console (F12) for errors
3. Restart both the backend and frontend
4. Check http://localhost:8000/docs to test the API

---

## 📊 API Documentation

The backend provides a complete REST API. Access the interactive documentation at:

```
http://localhost:8000/docs
```

### Example API Calls

**Get Conversations:**
```bash
curl http://localhost:8000/api/v1/conversations/
```

**Send Message:**
```bash
curl -X POST http://localhost:8000/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello!",
    "model": "mistral",
    "temperature": 0.7
  }'
```

---

## 🔧 Development Commands

### Backend Commands
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Commands
```bash
cd frontend
npm install
npm run dev
npm run build
npm run preview
```

---

## 🚀 Next Steps

After successful installation:

1. **Explore the Chat** - Send your first message
2. **Try Different Models** - Switch between AI models
3. **Adjust Settings** - Customize AI behavior
4. **View History** - Check your conversation history
5. **Check Analytics** - See usage statistics

---

## 📞 Support

If you encounter any issues:

1. Check the Troubleshooting section above
2. Make sure all prerequisites are installed
3. Try running INSTALL.bat again
4. Check your internet connection
5. Restart your computer if something doesn't work

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🎯 Getting Started Now

### The Fastest Way:
1. Download `INSTALL.bat`
2. Double-click it
3. Done! ✅

### Questions?
- Check the Troubleshooting section
- Make sure Python, Node.js, and Ollama are installed
- Restart your computer if something doesn't work

---

**Enjoy your local AI assistant! 🤖**

For more information, visit: https://github.com/lucasandre16112000-png/localai-assistant
