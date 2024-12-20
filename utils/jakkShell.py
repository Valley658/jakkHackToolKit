import subprocess
import getpass

from tools.cmdDict import CommandDictionary

USER_CREDENTIALS = {
    "jaxk": "jaxk"
}

def login():
    print("[+] Welcome to Jaxk Shell!")
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        print("[+] Login successful!")
        return username
    else:
        print("[-] Invalid username or password. Exiting.")
        exit()

def main():
    username = login()
    cmd_dict = CommandDictionary()

    print("[+] Jaxk Shell For Hacking!")

    while True:
        try:
            cmd = input(f"{username}@JaxkShell-[~] ").strip()
            if cmd == "exit":
                print("[+] Good Bye!!! :D")
                break
            
            if not cmd_dict.is_valid_command(cmd):
                print(f"[-] Unknown command: {cmd}")
                continue

            for c in cmd_dict.get_commands():
                cmd = cmd.replace(c, cmd_dict.get_commands()[c])

            cmd_list = cmd.split()
            result = subprocess.run(cmd_list, shell=True)
        except KeyboardInterrupt:
            print("\n[!] Session terminated by user.")
            break
        except Exception as e:
            print(f"[-] Error: {e}")

if __name__ == "__main__":
    main()