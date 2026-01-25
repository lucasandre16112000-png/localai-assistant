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
echo [1/7] Creating installation folder...
if not exist "%installPath%" mkdir "%installPath%"
echo [OK] Folder created at: %installPath%
echo.

REM Step 2: Download project from GitHub
echo [2/7] Downloading project from GitHub...
powershell -Command "try { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile('https://github.com/lucasandre16112000-png/localai-assistant/archive/refs/heads/main.zip', '%zipPath%'); Write-Host '[OK] Project downloaded' } catch { Write-Host '[ERROR] Failed to download'; exit 1 }"
if errorlevel 1 goto error_download
echo.

REM Step 3: Extract files
echo [3/7] Extracting files...
if exist "%extractPath%" (
    rmdir /s /q "%extractPath%" >nul 2>&1
)
mkdir "%extractPath%"
powershell -Command "try { Add-Type -AssemblyName System.IO.Compression.FileSystem; [System.IO.Compression.ZipFile]::ExtractToDirectory('%zipPath%', '%extractPath%'); Write-Host '[OK] Files extracted' } catch { Write-Host '[ERROR] Failed to extract'; exit 1 }"
if errorlevel 1 goto error_extract
echo.

REM Step 4: Copy files to permanent location
echo [4/7] Copying files to permanent location...
if exist "%installPath%" (
    rmdir /s /q "%installPath%" >nul 2>&1
)
mkdir "%installPath%"
xcopy "%extractPath%\localai-assistant-main\*" "%installPath%\" /E /I /Y >nul 2>&1
if errorlevel 1 goto error_copy
echo [OK] Files copied
echo.

REM Step 5: Clean up temporary files
echo [5/7] Cleaning up temporary files...
if exist "%zipPath%" del /f /q "%zipPath%" >nul 2>&1
if exist "%extractPath%" rmdir /s /q "%extractPath%" >nul 2>&1
echo [OK] Temporary files cleaned
echo.

REM Step 6: Check prerequisites
echo [6/7] Checking prerequisites and starting services...

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 goto error_python

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 goto error_node

REM Check if Ollama is available
ollama --version >nul 2>&1
if errorlevel 1 goto error_ollama

echo [OK] Python, Node.js, and Ollama found
echo.

REM Start Ollama in background
echo Starting Ollama service...
taskkill /F /IM ollama.exe >nul 2>&1
timeout /t 1 /nobreak >nul
start "" ollama serve
echo [OK] Ollama started
echo Waiting 10 seconds for Ollama to initialize...
timeout /t 10 /nobreak >nul
echo.

REM Check if model exists, if not download it
echo Checking for AI models...
for /f "tokens=*" %%i in ('ollama list 2^>nul') do (
    if "%%i"=="NAME" goto model_check_done
    if "%%i"=="dolphin-mistral" goto model_exists
)

echo No models found. Downloading dolphin-mistral (this may take 5-15 minutes)...
echo Please wait, this is a one-time download...
echo.
call ollama pull dolphin-mistral
if errorlevel 1 (
    echo [WARNING] Failed to download model, but continuing anyway...
    echo You can manually download it later with: ollama pull dolphin-mistral
)
echo.

:model_exists
:model_check_done
echo [OK] Model check complete
echo.

echo ================================================================================
echo.
echo                    STARTING LOCALAI ASSISTANT...
echo.
echo ================================================================================
echo.

timeout /t 2 /nobreak >nul

REM Step 7: Start backend and frontend
echo [7/7] Starting backend and frontend...
echo.

REM Start backend in separate window
cd /d "%installPath%\backend"
if errorlevel 1 goto error_backend_dir

echo Starting backend server...
start "LocalAI Backend" cmd /k "python -m pip install --upgrade pip setuptools wheel >nul 2>&1 && pip install -r requirements.txt >nul 2>&1 && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to start
echo Waiting for backend to start (20 seconds)...
timeout /t 20 /nobreak >nul
echo.

REM Start frontend in separate window
cd /d "%installPath%\frontend"
if errorlevel 1 goto error_frontend_dir

echo Starting frontend server...
start "LocalAI Frontend" cmd /k "npm install --no-fund >nul 2>&1 && npm run dev"

REM Wait for frontend to start
echo Waiting for frontend to start (10 seconds)...
timeout /t 10 /nobreak >nul
echo.

REM Open browser
echo.
echo ================================================================================
echo.
echo                    OPENING BROWSER...
echo.
echo ================================================================================
echo.

echo Waiting 5 more seconds to ensure everything is ready...
timeout /t 5 /nobreak >nul
start http://localhost:3000

echo.
echo ================================================================================
echo.
echo                    LOCALAI ASSISTANT IS READY!
echo.
echo ================================================================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo Ollama:   http://localhost:11434
echo.
echo API Docs: http://localhost:8000/docs
echo.
echo ================================================================================
echo.
echo You can now start chatting with the AI!
echo.
echo IMPORTANT - KEEP RUNNING:
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
echo [ERROR] Failed to download project from GitHub
echo Check your internet connection and try again
echo.
pause
exit /b 1

:error_extract
echo.
echo [ERROR] Failed to extract files
echo Make sure you have enough disk space
echo.
pause
exit /b 1

:error_copy
echo.
echo [ERROR] Failed to copy files
echo Make sure you have enough disk space
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

:error_backend_dir
echo.
echo [ERROR] Failed to access backend directory
echo Make sure the installation completed successfully
echo.
pause
exit /b 1

:error_frontend_dir
echo.
echo [ERROR] Failed to access frontend directory
echo Make sure the installation completed successfully
echo.
pause
exit /b 1
