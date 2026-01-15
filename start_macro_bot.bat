@echo off
TITLE Macro Bot Console
cd /d "%~dp0"

echo Starting Macro Bot...
echo ------------------------------------------

python main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] The program was unexpectedly shut down.
    pause
)