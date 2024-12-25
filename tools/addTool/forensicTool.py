import os
import platform
import time

def scan_linux(directory):
    print(f"[*] Scanning {directory} for deleted files (Linux-specific)...")
    # Linux-specific scanning logic here
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(f"[+] Found file: {os.path.join(root, file)}")

def scan_windows(directory):
    print(f"[*] Scanning {directory} for deleted files (Windows-specific)...")
    # Windows-specific scanning logic here
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(f"[+] Found file: {os.path.join(root, file)}")

def list_files(directory):
    print(f"[*] Listing all files in {directory}...")
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(f"[+] File: {os.path.join(root, file)}")

def find_large_files(directory, size_limit):
    print(f"[*] Searching for files larger than {size_limit} bytes in {directory}...")
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getsize(file_path) > size_limit:
                print(f"[+] Large file: {file_path} ({os.path.getsize(file_path)} bytes)")

def search_file_by_name(directory, file_name):
    print(f"[*] Searching for file named '{file_name}' in {directory}...")
    for root, dirs, files in os.walk(directory):
        if file_name in files:
            print(f"[+] Found file: {os.path.join(root, file_name)}")

def scan_for_hidden_files(directory):
    print(f"[*] Scanning for hidden files in {directory}...")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith('.'):
                print(f"[+] Hidden file: {os.path.join(root, file)}")

def log_activity(log_file, message):
    with open(log_file, 'a') as log:
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    print(f"[*] Logged: {message}")

def main(directory):
    current_platform = platform.system()
    print(f"[*] Detected platform: {current_platform}")

    if current_platform == "Linux":
        scan_linux(directory)
    elif current_platform == "Windows":
        scan_windows(directory)
    else:
        print(f"[!] Unsupported platform: {current_platform}")

    # Additional functionalities
    list_files(directory)
    find_large_files(directory, 1048576)  # Files larger than 1MB
    search_file_by_name(directory, "example.txt")
    scan_for_hidden_files(directory)
    log_activity("scan_log.txt", f"Scan completed for {directory} on {current_platform}")

if __name__ == "__main__":
    directory_to_scan = input("Enter the directory to scan: ")
    main(directory_to_scan)