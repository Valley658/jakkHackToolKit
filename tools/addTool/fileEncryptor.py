import os
from cryptography.fernet import Fernet

def generate_key(key_path='encryption.key'):
    """
    Generates and saves a key for encryption.
    """
    key = Fernet.generate_key()
    with open(key_path, 'wb') as key_file:
        key_file.write(key)
    print(f"[+] Key saved to {key_path}")
    return key

def load_key(key_path='encryption.key'):
    """
    Loads an existing key from a file.
    """
    try:
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
        print(f"[+] Key loaded from {key_path}")
        return key
    except FileNotFoundError:
        print(f"[-] Key file not found at {key_path}. Please generate a key first.")
        return None

def encrypt_file(file_path, key, delete_original=False):
    """
    Encrypts a file using the provided key.
    """
    try:
        cipher = Fernet(key)
        with open(file_path, 'rb') as file:
            data = file.read()
        encrypted_data = cipher.encrypt(data)
        encrypted_file_path = f"{file_path}.enc"
        with open(encrypted_file_path, 'wb') as file:
            file.write(encrypted_data)
        print(f"[+] File encrypted: {encrypted_file_path}")
        if delete_original:
            os.remove(file_path)
            print(f"[+] Original file deleted: {file_path}")
    except Exception as e:
        print(f"[-] Failed to encrypt {file_path}: {e}")

def decrypt_file(file_path, key, delete_encrypted=False):
    """
    Decrypts an encrypted file using the provided key.
    """
    try:
        cipher = Fernet(key)
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = cipher.decrypt(encrypted_data)
        original_file_path = file_path.replace('.enc', '')
        with open(original_file_path, 'wb') as file:
            file.write(decrypted_data)
        print(f"[+] File decrypted: {original_file_path}")
        if delete_encrypted:
            os.remove(file_path)
            print(f"[+] Encrypted file deleted: {file_path}")
    except Exception as e:
        print(f"[-] Failed to decrypt {file_path}: {e}")

def encrypt_folder(folder_path, key, delete_original=False):
    """
    Encrypts all files in a folder.
    """
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key, delete_original)

def decrypt_folder(folder_path, key, delete_encrypted=False):
    """
    Decrypts all encrypted files in a folder.
    """
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.enc'):
                file_path = os.path.join(root, file)
                decrypt_file(file_path, key, delete_encrypted)

def encrypt_specific_types(folder_path, key, file_types, delete_original=False):
    """
    Encrypts files of specific types in a folder.
    """
    for root, _, files in os.walk(folder_path):
        for file in files:
            if any(file.endswith(ext) for ext in file_types):
                file_path = os.path.join(root, file)
                encrypt_file(file_path, key, delete_original)

def decrypt_specific_types(folder_path, key, file_types, delete_encrypted=False):
    """
    Decrypts encrypted files of specific types in a folder.
    """
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.enc') and any(file.replace('.enc', '').endswith(ext) for ext in file_types):
                file_path = os.path.join(root, file)
                decrypt_file(file_path, key, delete_encrypted)

def list_files(folder_path):
    """
    Lists all files in a folder.
    """
    print(f"Files in {folder_path}:")
    for root, _, files in os.walk(folder_path):
        for file in files:
            print(f" - {os.path.join(root, file)}")

def main():
    print("File Encryptor/Decryptor v2.0")
    key_file_path = 'encryption.key'

    # Generate or load a key
    key = generate_key(key_file_path)  # Uncomment this line to generate a new key
    # key = load_key(key_file_path)  # Uncomment this line to load an existing key

    if not key:
        print("[-] Exiting: No key available.")
        return

    # Options
    print("\nChoose an option:")
    print("1. Encrypt a file")
    print("2. Decrypt a file")
    print("3. Encrypt a folder")
    print("4. Decrypt a folder")
    print("5. Encrypt specific file types in a folder")
    print("6. Decrypt specific file types in a folder")
    print("7. List all files in a folder")
    choice = input("Enter your choice (1-7): ")

    if choice == "1":
        file_path = input("Enter the file path: ")
        delete_original = input("Delete original file after encryption? (yes/no): ").strip().lower() == 'yes'
        encrypt_file(file_path, key, delete_original)
    elif choice == "2":
        file_path = input("Enter the encrypted file path: ")
        delete_encrypted = input("Delete encrypted file after decryption? (yes/no): ").strip().lower() == 'yes'
        decrypt_file(file_path, key, delete_encrypted)
    elif choice == "3":
        folder_path = input("Enter the folder path: ")
        delete_original = input("Delete original files after encryption? (yes/no): ").strip().lower() == 'yes'
        encrypt_folder(folder_path, key, delete_original)
    elif choice == "4":
        folder_path = input("Enter the folder path: ")
        delete_encrypted = input("Delete encrypted files after decryption? (yes/no): ").strip().lower() == 'yes'
        decrypt_folder(folder_path, key, delete_encrypted)
    elif choice == "5":
        folder_path = input("Enter the folder path: ")
        file_types = input("Enter file types to encrypt (comma-separated, e.g., .txt,.jpg): ").split(",")
        delete_original = input("Delete original files after encryption? (yes/no): ").strip().lower() == 'yes'
        encrypt_specific_types(folder_path, key, file_types, delete_original)
    elif choice == "6":
        folder_path = input("Enter the folder path: ")
        file_types = input("Enter file types to decrypt (comma-separated, e.g., .txt,.jpg): ").split(",")
        delete_encrypted = input("Delete encrypted files after decryption? (yes/no): ").strip().lower() == 'yes'
        decrypt_specific_types(folder_path, key, file_types, delete_encrypted)
    elif choice == "7":
        folder_path = input("Enter the folder path: ")
        list_files(folder_path)
    else:
        print("[-] Invalid choice. Exiting.")

if __name__ == "__main__":
    main()