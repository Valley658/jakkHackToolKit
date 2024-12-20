import zipfile

def main():
    zip_file = input("Enter the path to the ZIP file: ").strip()
    dictionary_file = input("Enter the path to the dictionary file: ").strip()

    try:
        with zipfile.ZipFile(zip_file, 'r') as zf:
            with open(dictionary_file, 'r') as df:
                for password in df:
                    password = password.strip()
                    try:
                        zf.extractall(pwd=password.encode('utf-8'))
                        print(f"\033[92m[+] Password found: {password}\033[0m")
                        return
                    except (RuntimeError, zipfile.BadZipFile):
                        continue
        print("\033[91m[-] Password not found in dictionary.\033[0m")
    except FileNotFoundError as e:
        print(f"\033[91m[!] File not found: {e}\033[0m")
    except Exception as e:
        print(f"\033[91m[!] An error occurred: {e}\033[0m")

if __name__ == "__main__":
    main()