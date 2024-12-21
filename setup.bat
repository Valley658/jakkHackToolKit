@echo off
chcp 65001 >nul 2>&1

python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Thank you USER, Python is installed!
    timeout /t 1 /nobreak >nul
) else (
    echo Python is not installed. Attempting to download and install Python...
    if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
        start chrome https://www.python.org/downloads/
    ) else (
        echo Please download Python manually from https://www.python.org/downloads
    )
    pause
    exit /b
)

echo Attempting to upgrade pip...
python -m pip install --upgrade pip
if %errorlevel% equ 0 (
    echo pip has been successfully upgraded.
) else (
    echo Failed to upgrade pip. Check your configuration.
    pause
    exit /b
)

if exist requirements.txt (
    echo Installing requirements from requirements.txt...
    python -m pip install -r requirements.txt
    if %errorlevel% equ 0 (
        echo Requirements have been successfully installed.
    ) else (
        echo Failed to install requirements. Check your configuration.
        pause
        exit /b
    )
) else (
    echo requirements.txt not found. Please ensure it exists in the directory.
    pause
    exit /b
)

echo Upgrading Scapy and Cryptography...
python -m pip install --upgrade scapy cryptography
if %errorlevel% equ 0 (
    echo Scapy and Cryptography have been successfully upgraded.
) else (
    echo Failed to upgrade Scapy or Cryptography. Check your configuration.
    pause
    exit /b
)

echo Checking for Npcap...
sc query npcap >nul 2>&1
if %errorlevel% neq 0 (
    echo Npcap is not installed. Attempting to download and install Npcap...
    if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
        start chrome https://nmap.org/npcap/
    ) else (
        echo Please download and install Npcap manually from https://nmap.org/npcap/
    )
    pause
    exit /b
) else (
    echo Npcap is already installed.
)

echo All tasks completed successfully!
pause