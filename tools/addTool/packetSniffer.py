import socket

def main():
        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        print("[*] Packet sniffer started. Press Ctrl+C to stop.")
        try:
            while True:
                data, addr = sniffer.recvfrom(65535)
                print(f"Packet received from {addr}: {data[:32]}")
        except KeyboardInterrupt:
            print("\n[!] Stopping sniffer.")
