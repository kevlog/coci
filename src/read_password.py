import os
import time
from dotenv import load_dotenv
from cryptography.fernet import Fernet

def get_env():
    load_dotenv()
    encrypted = os.getenv("PASSW")
    fernet_key = os.getenv("CODE")
    return {"encrypted" : encrypted, "fernet_key" : fernet_key}

def get_password():
    data = get_env()
    encrypted = data["encrypted"]
    fernet_key = data["fernet_key"]
    
    if not encrypted or not fernet_key or fernet_key == "":
        print("[INFO] 🚫 Data tidak lengkap di .env! Harap periksa file .env Anda.\a")
        time.sleep(2)
        exit(1)
    else:
        cipher = Fernet(fernet_key.encode())
        original_password = cipher.decrypt(encrypted.encode()).decode()

    def getPassword():
        return original_password

    return getPassword()

def load_access():
    return get_password()

def main():
    return load_access()

main()