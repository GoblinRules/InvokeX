@echo off
title InvokeX - Application & Tweak Installer
echo.
echo ========================================
echo           InvokeX Installer
echo ========================================
echo.
echo Starting InvokeX...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Please install Python 3.6+ first.
    echo Download from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Run the InvokeX application
python "%~dp0app_installer.py"

if %errorlevel% neq 0 (
    echo.
    echo An error occurred while running InvokeX.
    echo Check the error messages above for details.
    echo.
    pause
)
