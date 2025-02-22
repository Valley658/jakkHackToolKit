import os
import socket
import sys
import platform
import ctypes
import asyncio
import aiofiles

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

async def save_packet(data, addr):
    os.makedirs('packets', exist_ok=True)
    async with aiofiles.open('packets/packets.txt', 'a') as packet_file:
        await packet_file.write(f"Packet received from {addr}: {data[:32]}\n")

async def start_sniffer():
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    print("[*] Packet sniffer started. Press Ctrl+C to stop.")
    try:
        while True:
            data, addr = sniffer.recvfrom(65535)
            print(f"Packet received from {addr}: {data[:32]}")
            await save_packet(data, addr)
    except KeyboardInterrupt:
        print("\n[!] Stopping sniffer.")

async def main():
    current_platform = platform.system()
    print(f"[*] Detected platform: {current_platform}")

    require_admin()

    if current_platform == "Linux":
        print("[*] Linux detected. Ensure you have the appropriate permissions (e.g., run as root).")
        await start_sniffer()
    elif current_platform == "Windows":
        print("[*] Windows detected. Ensure you have Administrator privileges.")
        try:
            await start_sniffer()
        except PermissionError:
            print("[!] Permission denied. Please run this script as Administrator.")
    else:
        print(f"[!] Unsupported platform: {current_platform}")

if __name__ == "__main__":
    asyncio.run(main())