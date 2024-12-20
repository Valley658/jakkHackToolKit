from cryptography.fernet import Fernet

def file_encryptor(file_path):
    key = Fernet.generate_key()
    cipher = Fernet(key)
    with open(file_path, 'rb') as file:
        data = file.read()
    encrypted_data = cipher.encrypt(data)
    with open(f"{file_path}.enc", 'wb') as file:
        file.write(encrypted_data)
    print(f"[+] File encrypted: {file_path}.enc")