@echo off
REM Phishing Detector Setup Script for Windows
REM This script sets up the environment with all dependencies and fixes

echo =========================================
echo Phishing Detector - Setup Script
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed. Please install Python 3 first.
    exit /b 1
)

echo Python version:
python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo.
echo =========================================
echo Setup completed successfully!
echo =========================================
echo.
echo To activate the virtual environment, run:
echo   venv\Scripts\activate
echo.
echo To run the application, use:
echo   python app.py
echo.
echo The application will run on http://localhost:5001
echo.

pause
