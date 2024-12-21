echo "Running jakk.py..."
python3 jakk.py
if [ $? -eq 0 ]; then
    echo "jakk.py executed successfully."
else
    echo "Failed to execute jakk.py. Check your script for errors."
fi

read -p "Press any key to exit..." -n1 -s
deactivate