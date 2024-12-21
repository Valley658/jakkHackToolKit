@echo off
chcp 65001 >nul 2>&1

python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Thank you USER, Python is installed!
    timeout /t 1 /nobreak >nul
) else (
    echo Not installed, what a disappointment!
    echo Python is not installed. Attempting to download and install Python...
    
    if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
        start chrome https://www.python.org/downloads/
    ) else (
        echo Please download Python manually from https://www.python.org/downloads
    )
    pause
    exit /b
)

python -m pip install --upgrade pip
if %errorlevel% equ 0 (
    echo "pip has been successfully upgraded."
    pip install -r requirements.txt
    if %errorlevel% equ 0 (
        echo "Requirements have been successfully installed."
    ) else (
        echo "Failed to install requirements. Check your configuration."
    )
) else (
    echo "Failed to upgrade pip. Check your configuration."
)
pause