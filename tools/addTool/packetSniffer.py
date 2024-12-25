import os
import socket
import platform
import ctypes

def check_admin():
    if platform.system() == "Windows":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    elif platform.system() == "Linux":
        return os.geteuid() == 0
    return False

def require_admin():
    if not check_admin():
        if platform.system() == "Windows":
            print("[!] Administrator privileges required. Restarting as Administrator...")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            exit()
        elif platform.system() == "Linux":
            print("[!] Root privileges required. Please re-run the script as root.")
            exit()

def start_sniffer():
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    print("[*] Packet sniffer started. Press Ctrl+C to stop.")
    try:
        while True:
            data, addr = sniffer.recvfrom(65535)
            print(f"Packet received from {addr}: {data[:32]}")
    except KeyboardInterrupt:
        print("\n[!] Stopping sniffer.")

def main():
    current_platform = platform.system()
    print(f"[*] Detected platform: {current_platform}")

    require_admin()

    if current_platform == "Linux":
        print("[*] Linux detected. Ensure you have the appropriate permissions (e.g., run as root).")
        start_sniffer()
    elif current_platform == "Windows":
        print("[*] Windows detected. Ensure you have Administrator privileges.")
        try:
            start_sniffer()
        except PermissionError:
            print("[!] Permission denied. Please run this script as Administrator.")
    else:
        print(f"[!] Unsupported platform: {current_platform}")

if __name__ == "__main__":
    main()