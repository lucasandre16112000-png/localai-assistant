@echo off
setlocal enabledelayedexpansion

cls
color 0A

echo.
echo ================================================================================
echo.
echo                    LOCALAI ASSISTANT - AUTOMATIC INSTALLER
echo.
echo ================================================================================
echo.

REM Define installation paths
set "installPath=%USERPROFILE%\localai-assistant"
set "zipPath=%TEMP%\localai-assistant.zip"
set "extractPath=%TEMP%\localai-extract"

REM Step 1: Create installation folder
echo [1/8] Creating installation folder...
if not exist "%installPath%" mkdir "%installPath%"
echo [OK] Folder created at: %installPath%
echo.

REM Step 2: Download project from GitHub
echo [2/8] Downloading project from GitHub...
powershell -Command "try { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile('https://github.com/lucasandre16112000-png/localai-assistant/archive/refs/heads/main.zip', '%zipPath%'); Write-Host '[OK] Project downloaded' } catch { Write-Host '[ERROR] Failed to download'; exit 1 }"
if errorlevel 1 goto error_download
echo.

REM Step 3: Extract files
echo [3/8] Extracting files...
if exist "%extractPath%" rmdir /s /q "%extractPath%" >nul 2>&1
mkdir "%extractPath%"
powershell -Command "try { Add-Type -AssemblyName System.IO.Compression.FileSystem; [System.IO.Compression.ZipFile]::ExtractToDirectory('%zipPath%', '%extractPath%'); Write-Host '[OK] Files extracted' } catch { Write-Host '[ERROR] Failed to extract'; exit 1 }"
if errorlevel 1 goto error_extract
echo.

REM Step 4: Copy files to permanent location
echo [4/8] Copying files to permanent location...
if exist "%installPath%\*" rmdir /s /q "%installPath%" >nul 2>&1
mkdir "%installPath%"
xcopy "%extractPath%\localai-assistant-main\*" "%installPath%\" /E /I /Y >nul 2>&1
echo [OK] Files copied
echo.

REM Step 5: Clean up temporary files
echo [5/8] Cleaning up temporary files...
if exist "%zipPath%" del /f /q "%zipPath%" >nul 2>&1
if exist "%extractPath%" rmdir /s /q "%extractPath%" >nul 2>&1
echo [OK] Temporary files cleaned
echo.

REM Step 6: Check and start Ollama
echo [6/8] Checking Ollama installation...
ollama --version >nul 2>&1
if errorlevel 1 goto error_ollama

echo [OK] Ollama found
echo.
echo Starting Ollama service...

REM Kill any existing Ollama process
taskkill /F /IM ollama.exe >nul 2>&1

REM Start Ollama in background
start "" ollama serve

REM Wait for Ollama to start
echo Waiting for Ollama to start (this may take a moment)...
timeout /t 5 /nobreak >nul

REM Check if Ollama is responding
set "ollama_ready=0"
set "ollama_counter=0"
:check_ollama
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:11434/api/tags' -TimeoutSec 2 -ErrorAction Stop; exit 0 } catch { exit 1 }" >nul 2>&1
if errorlevel 0 (
    set "ollama_ready=1"
    goto ollama_ready
)

set /a ollama_counter=!ollama_counter!+1
if !ollama_counter! lss 30 (
    timeout /t 2 /nobreak >nul
    goto check_ollama
)

:ollama_ready
if !ollama_ready! equ 1 (
    echo [OK] Ollama is running
) else (
    echo [WARNING] Ollama may not be responding - continuing anyway
)
echo.

REM Check if model exists, if not download it
echo Checking for AI models...
ollama list | find "dolphin-mistral" >nul 2>&1
if errorlevel 1 (
    echo No models found. Downloading dolphin-mistral (this may take several minutes)...
    echo Please wait, this is a one-time download...
    echo.
    ollama pull dolphin-mistral
    if errorlevel 1 (
        echo [WARNING] Failed to download model, but continuing...
    ) else (
        echo [OK] Model downloaded successfully
    )
) else (
    echo [OK] Models found
)
echo.

REM Step 7: Install dependencies
echo [7/8] Installing dependencies...

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 goto error_python

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 goto error_node

echo [OK] Python and Node.js found
echo.

echo ================================================================================
echo.
echo                    STARTING LOCALAI ASSISTANT...
echo.
echo ================================================================================
echo.

timeout /t 2 /nobreak >nul

REM Step 8: Start backend and frontend
echo [8/8] Starting backend and frontend servers...
echo.

REM Start backend in separate window
cd /d "%installPath%\backend"
start "LocalAI Backend" cmd /k "python -m pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to start
echo Waiting for backend to start...
timeout /t 20 /nobreak >nul

REM Start frontend in separate window
cd /d "%installPath%\frontend"
start "LocalAI Frontend" cmd /k "npm install --no-fund && npm run dev"

REM Wait for frontend to start and be ready
echo Waiting for frontend to start and be ready...
timeout /t 20 /nobreak >nul

REM Check if frontend is ready by testing the port
echo Checking if frontend is ready...
set "counter=0"
:check_frontend
netstat -ano | find ":3000" >nul 2>&1
if errorlevel 1 (
    set /a counter=!counter!+1
    if !counter! lss 30 (
        timeout /t 2 /nobreak >nul
        goto check_frontend
    )
)

REM Open browser only when frontend is ready
echo.
echo ================================================================================
echo.
echo                    FRONTEND IS READY - OPENING BROWSER...
echo.
echo ================================================================================
echo.

start http://localhost:3000

echo.
echo ================================================================================
echo.
echo                    LOCALAI ASSISTANT IS RUNNING!
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo Ollama:   http://localhost:11434
echo.
echo Docs:     http://localhost:8000/docs
echo.
echo ================================================================================
echo.
echo IMPORTANT:
echo - Keep all terminal windows open
echo - Do NOT close them or the application will stop
echo - To stop: Close all terminal windows
echo.
echo ================================================================================
echo.

pause
exit /b 0

:error_download
echo.
echo [ERROR] Failed to download project
echo Check your internet connection and try again
echo.
pause
exit /b 1

:error_extract
echo.
echo [ERROR] Failed to extract files
echo.
pause
exit /b 1

:error_python
echo.
echo [ERROR] Python not found or not in PATH
echo Make sure Python 3.11+ is installed
echo Download from: https://www.python.org/downloads/
echo Important: Check "Add Python to PATH" during installation
echo.
pause
exit /b 1

:error_node
echo.
echo [ERROR] Node.js not found or not in PATH
echo Make sure Node.js 18+ is installed
echo Download from: https://nodejs.org/
echo.
pause
exit /b 1

:error_ollama
echo.
echo [ERROR] Ollama not found or not in PATH
echo Make sure Ollama is installed
echo Download from: https://ollama.ai/
echo Important: Install Ollama and add it to PATH
echo.
pause
exit /b 1
