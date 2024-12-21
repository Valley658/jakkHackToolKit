@echo off
chcp 65001 >nul 2>&1

echo Running jakk.py...
python jakk.py
if %errorlevel% equ 0 (
    echo jakk.py executed successfully.
) else (
    echo Failed to execute jakk.py. Check your script for errors.
)

pause