@echo off
setlocal
TITLE Antigravity Skills App

echo ===================================================
echo      Antigravity Awesome Skills - Web App
echo ===================================================

:: Check for Node.js
WHERE node >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not installed. Please install it from https://nodejs.org/
    pause
    exit /b 1
)

:: ===== Auto-Update Skills from GitHub =====
WHERE git >nul 2>nul
IF %ERRORLEVEL% NEQ 0 goto :NO_GIT
goto :HAS_GIT

:NO_GIT
echo [WARN] Git is not installed. Skipping auto-update.
goto :SKIP_UPDATE

:HAS_GIT
:: Add upstream remote if not already set
git remote get-url upstream >nul 2>nul
IF %ERRORLEVEL% EQU 0 goto :DO_FETCH
echo [INFO] Adding upstream remote...
git remote add upstream https://github.com/sickn33/antigravity-awesome-skills.git

:DO_FETCH
echo [INFO] Checking for skill updates from original repo...
git fetch upstream >nul 2>nul
IF %ERRORLEVEL% NEQ 0 goto :FETCH_FAIL
goto :DO_MERGE

:FETCH_FAIL
echo [WARN] Could not fetch updates. Continuing with local version...
goto :SKIP_UPDATE

:DO_MERGE
git merge upstream/main --ff-only >nul 2>nul
IF %ERRORLEVEL% NEQ 0 goto :MERGE_FAIL
echo [INFO] Skills updated successfully from original repo!
goto :SKIP_UPDATE

:MERGE_FAIL
echo [WARN] Could not merge updates. Continuing with local version...

:SKIP_UPDATE

:: Check/Install dependencies
cd web-app

:CHECK_DEPS
if not exist "node_modules\" (
    echo [INFO] Dependencies not found. Installing...
    goto :INSTALL_DEPS
)

:: Verify dependencies aren't corrupted (e.g. esbuild arch mismatch after update)
echo [INFO] Verifying app dependencies...
call npx -y vite --version >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [WARN] Dependencies appear corrupted or outdated.
    echo [INFO] Cleaning up and reinstalling fresh dependencies...
    rmdir /s /q "node_modules" >nul 2>nul
    goto :INSTALL_DEPS
)
goto :DEPS_OK

:INSTALL_DEPS
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install dependencies. Please check your internet connection.
    pause
    exit /b 1
)

:DEPS_OK
cd ..

:: Run setup script
echo [INFO] Updating skills data...
call npm run app:setup

:: Start App
echo [INFO] Starting Web App...
echo [INFO] Opening default browser...
cd web-app
call npx -y vite --open

endlocal
