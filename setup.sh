#!/bin/bash

exit_with_message() {
    echo "$1"
    exit 1
}

# Check if Python3 is installed
if python3 --version > /dev/null 2>&1; then
    echo "Thank you USER, Python is installed!"
    sleep 0.5
else
    echo "Python is not installed. Attempting to download and install Python..."

    # Check for default browser and open the Python download page
    if command -v xdg-open > /dev/null; then
        xdg-open https://www.python.org/downloads/
    elif command -v gnome-open > /dev/null; then
        gnome-open https://www.python.org/downloads/
    elif command -v open > /dev/null; then
        open https://www.python.org/downloads/
    else
        echo "Please download Python manually from https://www.python.org/downloads"
    fi

    exit_with_message "Python installation required. Exiting..."
fi

# Attempt to upgrade pip
echo "Attempting to upgrade pip..."
python3 -m pip install --upgrade pip --break-system-packages
if [ $? -eq 0 ]; then
    echo "pip has been successfully upgraded."
else
    exit_with_message "Failed to upgrade pip. Check your configuration."
fi

# Check if requirements.txt exists
if [ -f requirements.txt ]; then
    echo "Installing requirements from requirements.txt..."
    python3 -m pip install -r requirements.txt --break-system-packages
    if [ $? -eq 0 ]; then
        echo "Requirements have been successfully installed."
    else
        exit_with_message "Failed to install requirements. Check your configuration."
    fi
else
    exit_with_message "requirements.txt not found. Please ensure it exists in the directory."
fi

# Upgrade Scapy and Cryptography manually
echo "Upgrading Scapy and Cryptography..."
python3 -m pip install --upgrade scapy cryptography
if [ $? -eq 0 ]; then
    echo "Scapy and Cryptography have been successfully upgraded."
else
    exit_with_message "Failed to upgrade Scapy or Cryptography. Check your configuration."
fi

# Check if Npcap is installed (for Windows only)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    echo "Checking for Npcap..."
    if ! sc query npcap > /dev/null 2>&1; then
        echo "Npcap is not installed. Attempting to download and install Npcap..."

        if command -v powershell > /dev/null; then
            powershell -Command "Start-Process -FilePath 'https://nmap.org/npcap/' -Wait"
        else
            echo "Please download and install Npcap manually from https://nmap.org/npcap/"
        fi

        exit_with_message "Npcap installation required. Exiting..."
    else
        echo "Npcap is already installed."
    fi
fi

echo "All tasks completed successfully!"
exit 0