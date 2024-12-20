import socket
import time
import os
import threading

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

def save_results(open_ports, closed_ports):
    os.makedirs('portscanner', exist_ok=True)
    with open('portscanner/open_ports.txt', 'w') as open_file:
        open_file.write("Open Ports:\n")
        if open_ports:
            for port in open_ports:
                open_file.write(f"Port {port} is OPEN\n")
        else:
            open_file.write("No open ports found.\n")
    with open('portscanner/closed_ports.txt', 'w') as closed_file:
        closed_file.write("Closed Ports:\n")
        if closed_ports:
            for port in closed_ports:
                closed_file.write(f"Port {port} is CLOSED\n")
        else:
            closed_file.write("No closed ports found.\n")

def main():
    print("[ PortScanner ]")
    input("Press Enter to continue")

    print("1. Scan your own IP")
    print("2. Enter a target IP")
    choice = input("Choose an option: ")

    if choice == "1":
        target = socket.gethostbyname(socket.gethostname())
    elif choice == "2":
        target = input("Enter the target IP: ")
    else:
        print("Invalid choice. Exiting.")
        return

    start_port = int(input("Enter the starting port: "))
    end_port = int(input("Enter the ending port: "))

    clearConsole()
    print(f"\nStarting port scan on {target}...\n")

    open_ports = []
    closed_ports = []

    def scan_port(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.2)
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
                print(f"\033[92m[OPEN]\033[0m Port {port} on {target}")
            else:
                closed_ports.append(port)
                print(f"[CLOSED] Port {port} on {target}")
            sock.close()
        except KeyboardInterrupt:
            print("\nScan interrupted.")
            return
        except socket.error as err:
            print(f"Socket error: {err}")
            return

    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(port,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    save_results(open_ports, closed_ports)

    print("\n" + "=" * 40)
    print(f"Scan on {target} completed!")
    if open_ports:
        print(f"\033[92mOpen ports:\033[0m {', '.join(map(str, open_ports))}")
    else:
        print("No open ports found.")
    print(f"Closed ports: {len(closed_ports)}")
    print("Results saved in 'portscanner' folder.")
    print("=" * 40 + "\n")

if __name__ == "__main__":
    main()