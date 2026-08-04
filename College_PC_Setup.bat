@echo off
setlocal enabledelayedexpansion
title AI Career Intelligence Platform - College PC Setup

echo =======================================================
echo AI Career Intelligence Platform - Automated Setup
echo =======================================================

:: 1. Check if running from a USB drive (typically not C:)
set current_drive=%~d0
if /I not "%current_drive%"=="C:" (
    echo [WARNING] You are running this project from drive %current_drive%.
    echo College PCs usually have AppLocker policies that block Python DLLs 
    echo from running on USB drives ^(E:, F:, etc.^).
    echo.
    echo If you encounter a "DLL load failed: An Application Control policy has blocked this file" error,
    echo PLEASE COPY THIS ENTIRE FOLDER TO YOUR DESKTOP OR C:\ DRIVE and run it from there.
    echo.
    pause
)

:: 2. Delete existing .venv if it was copied from another computer
echo [INFO] Checking for copied Virtual Environment...
if exist ".venv" (
    echo [INFO] Existing .venv found. Deleting it to avoid path and DLL conflict errors...
    rmdir /s /q ".venv"
    echo [INFO] Deleted old .venv.
)

:: 3. Create fresh .venv
echo [INFO] Creating a fresh Virtual Environment for this PC...
python -m venv .venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment. Ensure Python is installed and in your PATH.
    pause
    exit /b 1
)

:: 4. Activate and Install Dependencies
echo [INFO] Activating Virtual Environment and installing dependencies...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies. Check your internet connection.
    pause
    exit /b 1
)

:: 5. Download NLTK resources
echo [INFO] Downloading required NLTK NLP resources...
python -m nltk.downloader punkt punkt_tab stopwords wordnet

:: 6. Launch Application
echo [INFO] Setup complete! Launching the application...
streamlit run app/streamlit_app.py

pause
