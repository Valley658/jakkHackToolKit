#!/bin/bash

# Set locale to UTF-8
export LC_ALL=en_US.UTF-8

# Function to exit with a message
exit_with_message() {
    echo "$1"
    read -p "Press any key to exit..." -n1 -s
    exit 1
}

# Check if Python is installed
if python3 --version > /dev/null 2>&1; then
    echo "Thank you USER, Python is installed!"
    sleep 0.5
else
    echo "Python is not installed. Attempting to download and install Python..."
    
    if command -v xdg-open > /dev/null; then
        xdg-open https://www.python.org/downloads/
    else
        echo "Please download Python manually from https://www.python.org/downloads"
    fi
    
    exit_with_message "Python installation required. Exiting..."
fi

# Upgrade pip using --break-system-packages
echo "Attempting to upgrade pip..."
python3 -m pip install --upgrade pip --break-system-packages
if [ $? -eq 0 ]; then
    echo "pip has been successfully upgraded."
else
    exit_with_message "Failed to upgrade pip. Check your configuration."
fi

# Create a virtual environment and install requirements
echo "Setting up a virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    exit_with_message "Failed to create a virtual environment. Check your Python installation."
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "Requirements have been successfully installed."
else
    echo "Failed to install requirements. Check your configuration."
    deactivate
    exit_with_message "Exiting..."
fi

# Check and install colorama if missing
echo "Checking for 'colorama' module..."
pip show colorama > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "'colorama' not found. Installing 'colorama'..."
    pip install colorama
    if [ $? -eq 0 ]; then
        echo "'colorama' has been successfully installed."
    else
        echo "Failed to install 'colorama'. Check your configuration."
        deactivate
        exit_with_message "Exiting..."
    fi
else
    echo "'colorama' is already installed."
fi

# Run jakk.py
echo "Running jakk.py..."
python3 jakk.py
if [ $? -eq 0 ]; then
    echo "jakk.py executed successfully."
else
    echo "Failed to execute jakk.py. Check your script for errors."
fi

read -p "Press any key to exit..." -n1 -s
deactivate