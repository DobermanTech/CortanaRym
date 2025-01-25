@echo off
REM Check if Python is installed
python --version
IF %ERRORLEVEL% NEQ 0 (
    echo Python not found. Installing Python...
    REM Add command to install Python (e.g., using a pre-downloaded installer)
    REM For example, assuming the installer is in the same directory:
    REM start /wait python-3.9.1-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
    REM You need to adjust the command based on your Python installer

    REM Verify the installation
    python --version
    IF %ERRORLEVEL% NEQ 0 (
        echo Python installation failed.
        pause
        exit /b
    )
)

REM Check if Pygame is installed
python -c "import pygame" 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Pygame not found. Installing Pygame...
    pip install pygame
    REM Verify the installation
    python -c "import pygame" 2>nul
    IF %ERRORLEVEL% NEQ 0 (
        echo Pygame installation failed.
        pause
        exit /b
    )
)

REM Run the Python script
cd /d "C:\Data\Custom Programs\CortanaRym\Version 0.4"
python main.py
pause
