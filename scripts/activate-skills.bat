@echo off
setlocal EnableDelayedExpansion

:: --- CONFIGURATION ---
set "BASE_DIR=%USERPROFILE%\.gemini\antigravity"
set "SKILLS_DIR=%BASE_DIR%\skills"
set "LIBRARY_DIR=%BASE_DIR%\skills_library"
set "ARCHIVE_DIR=%BASE_DIR%\skills_archive"
set "REPO_SKILLS=%~dp0..\skills"

echo Activating Antigravity skills...

:: --- ARGUMENT HANDLING ---
set "DO_CLEAR=0"
set "EXTRA_ARGS="

for %%a in (%*) do (
    if /I "%%a"=="--clear" (
        set "DO_CLEAR=1"
    ) else (
        if "!EXTRA_ARGS!"=="" (set "EXTRA_ARGS=%%a") else (set "EXTRA_ARGS=!EXTRA_ARGS! %%a")
    )
)

:: --- LIBRARY SYNC ---
:: If running from the repo, ensure the library is synced with the 1,200+ skills source.
if exist "%REPO_SKILLS%" (
    echo Syncing library with repository source...
    if not exist "%LIBRARY_DIR%" mkdir "%LIBRARY_DIR%" 2>nul
    robocopy "%REPO_SKILLS%" "%LIBRARY_DIR%" /E /NFL /NDL /NJH /NJS /XO >nul 2>&1
)

:: If still no library, try to create one from current skills or archives.
if not exist "%LIBRARY_DIR%" (
    echo Initializing skills library from local state...
    mkdir "%LIBRARY_DIR%" 2>nul
    
    :: 1. Migrate from current skills folder
    if exist "%SKILLS_DIR%" (
        echo   + Moving current skills to library...
        robocopy "%SKILLS_DIR%" "%LIBRARY_DIR%" /E /MOVE /NFL /NDL /NJH /NJS >nul 2>&1
    )
    
    :: 2. Merge from all archives
    for /f "delims=" %%i in ('dir /b /ad "%BASE_DIR%\skills_archive*" 2^>nul') do (
        echo   + Merging skills from %%i...
        robocopy "%BASE_DIR%\%%i" "%LIBRARY_DIR%" /E /NFL /NDL /NJH /NJS >nul 2>&1
    )
)

:: --- PREPARE ACTIVE FOLDER ---
if "!DO_CLEAR!"=="1" (
    echo [RESET] Archiving and clearing existing skills...
    if exist "%SKILLS_DIR%" (
        set "ts=%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
        set "ts=!ts: =0!"
        robocopy "%SKILLS_DIR%" "%ARCHIVE_DIR%_!ts!" /E /MOVE /NFL /NDL /NJH /NJH >nul 2>&1
    )
) else (
    echo [APPEND] Layering new skills onto existing folder...
)
mkdir "%SKILLS_DIR%" 2>nul


:: --- BUNDLE EXPANSION ---
set "ESSENTIALS="
echo Expanding bundles...

python --version >nul 2>&1
if not errorlevel 1 (
    :: Safely pass all arguments to Python (filtering out --clear)
    python "%~dp0..\tools\scripts\get-bundle-skills.py" !EXTRA_ARGS! > "%TEMP%\skills_list.txt" 2>nul
    
    :: If no other arguments, expand Essentials
    if "!EXTRA_ARGS!"=="" python "%~dp0..\tools\scripts\get-bundle-skills.py" Essentials > "%TEMP%\skills_list.txt" 2>nul
    
    if exist "%TEMP%\skills_list.txt" (
        set /p ESSENTIALS=<"%TEMP%\skills_list.txt"
        del "%TEMP%\skills_list.txt"
    )
)

:: Fallback if Python fails or returned empty
if "!ESSENTIALS!"=="" (
    if "!EXTRA_ARGS!"=="" (
        echo Using default essentials...
        set "ESSENTIALS=api-security-best-practices auth-implementation-patterns backend-security-coder frontend-security-coder cc-skill-security-review pci-compliance frontend-design react-best-practices react-patterns nextjs-best-practices tailwind-patterns form-cro seo-audit ui-ux-pro-max 3d-web-experience canvas-design mobile-design scroll-experience senior-fullstack frontend-developer backend-dev-guidelines api-patterns database-design stripe-integration agent-evaluation langgraph mcp-builder prompt-engineering ai-agents-architect rag-engineer llm-app-patterns rag-implementation prompt-caching context-window-management langfuse"
    ) else (
        :: Just use the literal arguments
        set "ESSENTIALS=!EXTRA_ARGS!"
    )
)

:: --- RESTORATION ---
echo Restoring selected skills...
for %%s in (!ESSENTIALS!) do (
    if exist "%SKILLS_DIR%\%%s" (
        echo   . %%s ^(already active^)
    ) else if exist "%LIBRARY_DIR%\%%s" (
        echo   + %%s
        robocopy "%LIBRARY_DIR%\%%s" "%SKILLS_DIR%\%%s" /E /NFL /NDL /NJH /NJS >nul 2>&1
    ) else (
        echo   - %%s ^(not found in library^)
    )
)

echo.
echo Done! Antigravity skills are now activated.
pause
