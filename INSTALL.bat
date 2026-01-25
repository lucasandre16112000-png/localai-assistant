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
if exist "%extractPath%" rmdir /s /q "%extractPath%"
mkdir "%extractPath%"
powershell -Command "try { Add-Type -AssemblyName System.IO.Compression.FileSystem; [System.IO.Compression.ZipFile]::ExtractToDirectory('%zipPath%', '%extractPath%'); Write-Host '[OK] Files extracted' } catch { Write-Host '[ERROR] Failed to extract'; exit 1 }"
if errorlevel 1 goto error_extract
echo.

REM Step 4: Copy files to permanent location
echo [4/8] Copying files to permanent location...
if exist "%installPath%\*" rmdir /s /q "%installPath%"
mkdir "%installPath%"
xcopy "%extractPath%\localai-assistant-main\*" "%installPath%\" /E /I /Y >nul
echo [OK] Files copied
echo.

REM Step 5: Clean up temporary files
echo [5/8] Cleaning up temporary files...
if exist "%zipPath%" del /f /q "%zipPath%"
if exist "%extractPath%" rmdir /s /q "%extractPath%"
echo [OK] Temporary files cleaned
echo.

REM Step 6: Install backend dependencies
echo [6/8] Installing backend dependencies...
cd /d "%installPath%\backend"
if exist "venv" rmdir /s /q venv
python -m venv venv >nul 2>&1
if errorlevel 1 goto error_python
call venv\Scripts\activate.bat
pip install --upgrade pip setuptools wheel >nul 2>&1
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 goto error_install
echo [OK] Backend dependencies installed
echo.

REM Step 7: Install frontend dependencies
echo [7/8] Installing frontend dependencies...
cd /d "%installPath%\frontend"
if exist "node_modules" rmdir /s /q node_modules
npm install --no-fund >nul 2>&1
if errorlevel 1 goto error_npm
echo [OK] Frontend dependencies installed
echo.

REM Step 8: Start servers
echo [8/8] Starting servers...
echo.
echo ================================================================================
echo.
echo                    STARTING LOCALAI ASSISTANT...
echo.
echo ================================================================================
echo.

timeout /t 2 /nobreak >nul

REM Start backend in separate window
cd /d "%installPath%\backend"
call venv\Scripts\activate.bat
start "LocalAI Backend" cmd /k "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to start
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

REM Start frontend in separate window
cd /d "%installPath%\frontend"
start "LocalAI Frontend" cmd /k "npm run dev"

REM Wait for frontend to start
echo Waiting for frontend to start...
timeout /t 5 /nobreak >nul

REM Open browser
echo.
echo ================================================================================
echo.
echo                    OPENING BROWSER...
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
echo.
echo Docs:     http://localhost:8000/docs
echo.
echo ================================================================================
echo.
echo IMPORTANT:
echo - Keep both terminal windows open
echo - Do NOT close them or the application will stop
echo - To stop: Close both terminal windows
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

:error_install
echo.
echo [ERROR] Failed to install backend dependencies
echo Make sure Python is installed correctly
echo.
pause
exit /b 1

:error_npm
echo.
echo [ERROR] Failed to install frontend dependencies
echo Make sure Node.js is installed
echo Download from: https://nodejs.org/
echo.
pause
exit /b 1
