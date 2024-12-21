import os
import platform
import subprocess
import time
import webbrowser

def find_file(file_name, search_path):
    for root, dirs, files in os.walk(search_path):
        if file_name in files:
            return os.path.join(root, file_name)
    return None

class Anonymizer:
    def __init__(self):
        self.os_type = platform.system()
        if self.os_type == "Windows":
            self.proxychains_config = None
            self.tor_command = "tor.exe"
            self.search_path = "C:\\"  # Default search path for Windows
        elif self.os_type == "Linux":
            self.proxychains_config = "/etc/proxychains.conf"
            self.tor_command = "tor"
            self.search_path = "/"  # Default search path for Linux
        self.log_file = "anonymizer_tool_log.txt"

    def log_message(self, message):
        with open(self.log_file, "a") as log:
            log.write(message + "\n")

    def find_tor(self):
        print("[*] Searching for Tor Browser...")
        self.log_message("[*] Searching for Tor Browser...")

        tor_path = find_file("tor.exe" if self.os_type == "Windows" else "tor", self.search_path)

        if tor_path:
            print(f"[+] Tor Browser found: {tor_path}")
            self.log_message(f"[+] Tor Browser found: {tor_path}")
            self.tor_command = tor_path
            return True
        else:
            print("[-] Tor Browser not found.")
            self.log_message("[-] Tor Browser not found.")
            return False

    def check_requirements(self):
        print(f"[*] Checking dependencies for {self.os_type}...")
        self.log_message(f"[*] Checking dependencies for {self.os_type}...")

        required_tools = ["curl"]
        if self.os_type == "Linux":
            required_tools.append("proxychains")

        missing_tools = []

        for tool in required_tools:
            if not self.is_tool_installed(tool):
                print(f"[-] {tool} is not installed. Please install it to continue.")
                self.log_message(f"[-] {tool} is not installed. Please install it to continue.")
                missing_tools.append(tool)

        if not self.find_tor():
            print("[+] Opening Tor installation page...")
            self.log_message("[+] Opening Tor installation page...")
            webbrowser.open("https://www.torproject.org/download/")
            missing_tools.append("tor")

        if missing_tools:
            return False

        print("[+] All required tools are installed.")
        self.log_message("[+] All required tools are installed.")
        return True

    def is_tool_installed(self, tool):
        if self.os_type == "Windows":
            return subprocess.call(f"where {tool} >nul 2>&1", shell=True) == 0
        elif self.os_type == "Linux":
            return subprocess.call(f"which {tool} > /dev/null 2>&1", shell=True) == 0

    def configure_proxychains(self):
        if self.os_type != "Linux":
            print("[-] ProxyChains configuration is only available on Linux.")
            self.log_message("[-] ProxyChains configuration is only available on Linux.")
            return

        print("[*] Configuring ProxyChains...")
        self.log_message("[*] Configuring ProxyChains...")

        try:
            if os.path.exists(self.proxychains_config):
                with open(self.proxychains_config, "r") as file:
                    lines = file.readlines()

                with open(self.proxychains_config, "w") as file:
                    for line in lines:
                        if "strict_chain" in line:
                            file.write("strict_chain\n")
                        elif "dynamic_chain" in line:
                            file.write("#dynamic_chain\n")
                        elif "random_chain" in line:
                            file.write("#random_chain\n")
                        else:
                            file.write(line)
                print("[+] ProxyChains configured successfully.")
                self.log_message("[+] ProxyChains configured successfully.")
            else:
                print(f"[-] ProxyChains config file not found: {self.proxychains_config}")
                self.log_message(f"[-] ProxyChains config file not found: {self.proxychains_config}")
        except Exception as e:
            print(f"[-] Error configuring ProxyChains: {e}")
            self.log_message(f"[-] Error configuring ProxyChains: {e}")

    def start_tor(self):
        print("[*] Starting Tor service...")
        self.log_message("[*] Starting Tor service...")

        try:
            subprocess.Popen(self.tor_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(5)  # Wait for Tor to initialize
            print("[+] Tor service started successfully.")
            self.log_message("[+] Tor service started successfully.")
        except Exception as e:
            print(f"[-] Failed to start Tor service: {e}")
            self.log_message(f"[-] Failed to start Tor service: {e}")

    def test_anonymity(self):
        print("[*] Testing anonymity...")
        self.log_message("[*] Testing anonymity...")

        try:
            if self.os_type == "Windows":
                result = subprocess.check_output("curl http://ifconfig.me", shell=True, universal_newlines=True)
            elif self.os_type == "Linux":
                result = subprocess.check_output("proxychains curl http://ifconfig.me", shell=True, universal_newlines=True)

            print(f"[+] Your anonymized IP: {result.strip()}")
            self.log_message(f"[+] Your anonymized IP: {result.strip()}")
        except Exception as e:
            print(f"[-] Failed to fetch anonymized IP: {e}")
            self.log_message(f"[-] Failed to fetch anonymized IP: {e}")

    def add_custom_proxy(self):
        if self.os_type != "Linux":
            print("[-] Adding custom proxies is only supported on Linux.")
            self.log_message("[-] Adding custom proxies is only supported on Linux.")
            return

        print("[*] Adding custom proxy...")
        self.log_message("[*] Adding custom proxy...")

        proxy = input("Enter the proxy (e.g., socks5 127.0.0.1 9050): ").strip()
        try:
            if os.path.exists(self.proxychains_config):
                with open(self.proxychains_config, "a") as file:
                    file.write(f"\n{proxy}\n")
                print("[+] Custom proxy added successfully.")
                self.log_message("[+] Custom proxy added successfully.")
            else:
                print(f"[-] ProxyChains config file not found: {self.proxychains_config}")
                self.log_message(f"[-] ProxyChains config file not found: {self.proxychains_config}")
        except Exception as e:
            print(f"[-] Failed to add custom proxy: {e}")
            self.log_message(f"[-] Failed to add custom proxy: {e}")

    def perform_dns_leak_test(self):
        print("[*] Performing DNS leak test...")
        self.log_message("[*] Performing DNS leak test...")

        try:
            if self.os_type == "Windows":
                webbrowser.open("https://dnsleaktest.com/")
            elif self.os_type == "Linux":
                subprocess.run("proxychains firefox https://dnsleaktest.com/", shell=True)
            print("[+] DNS leak test page opened in your browser.")
            self.log_message("[+] DNS leak test page opened in your browser.")
        except Exception as e:
            print(f"[-] Failed to perform DNS leak test: {e}")
            self.log_message(f"[-] Failed to perform DNS leak test: {e}")

    def show_menu(self):
        print("\n[ Anonymizer Menu ]")
        print("[1] Check Dependencies")
        print("[2] Configure ProxyChains (Linux only)")
        print("[3] Start Tor Service")
        print("[4] Test Anonymity")
        print("[5] Add Custom Proxy (Linux only)")
        print("[6] Perform DNS Leak Test")
        print("[7] Exit")

    def run(self):
        if not self.check_requirements():
            return

        while True:
            self.show_menu()
            choice = input("> ").strip()

            if choice == "1":
                self.check_requirements()
            elif choice == "2":
                self.configure_proxychains()
            elif choice == "3":
                self.start_tor()
            elif choice == "4":
                self.test_anonymity()
            elif choice == "5":
                self.add_custom_proxy()
            elif choice == "6":
                self.perform_dns_leak_test()
            elif choice == "7":
                print("[+] Exiting anonymizer tool.")
                self.log_message("[+] Exiting anonymizer tool.")
                break
            else:
                print("[-] Invalid choice. Please try again.")
                self.log_message("[-] Invalid choice. Please try again.")

def main():
    anonymizer = Anonymizer()
    anonymizer.run()

if __name__ == "__main__":
    main()