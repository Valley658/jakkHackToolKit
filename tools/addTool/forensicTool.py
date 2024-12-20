import os

def main(diretory):
        print(f"[*] Scanning {diretory} for deleted files...")
        for root, dirs, files in os.walk(diretory):
            for file in files:
                print(f"[+] Found file: {os.path.join(root, file)}")