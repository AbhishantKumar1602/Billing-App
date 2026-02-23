@echo off
title Billing App - Setup & Launch
color 0B

echo.
echo  ============================================
echo   VIJAY HOMOEO BILLING APP
echo  ============================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found!
    echo  Please install Python 3.10+ from https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during install.
    pause
    exit /b
)

echo  [OK] Python found.

:: Install dependencies if not already installed
echo  Checking / installing dependencies...
pip install PyQt6 PyQt6-WebEngine --quiet --upgrade

echo  [OK] Dependencies ready.
echo.
echo  Launching Billing App...
echo.

python billing_app.py

pause
