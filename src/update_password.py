import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

def get_env():
    load_dotenv() # Load .env
    raw_password = os.getenv("PASSW") # Ambil password mentah
    fernet_key = os.getenv("CODE")

    # Jika PASSWORD belum ada, minta input password dari user
    if not raw_password:
        raw_password = input("[INFO] 🔑 Masukkan password untuk disimpan: ")
        update_env("PASSW", raw_password)

    # Cek apakah sudah ada FERNET_KEY di .env    
    # Generate key jika belum ada
    if not fernet_key:
        key = Fernet.generate_key()
        update_env("CODE", key.decode())
    else:
        key = fernet_key.encode()
    
    return {"raw_password" : raw_password, "key" : key}

def update_env(key, value):
    lines = []
    found = False

    # Baca file .env
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            lines = f.readlines()

    # Tulis ulang ke .env, menambah atau mengupdate key yang sudah ada
    with open(".env", "w") as f:
        for line in lines:
            if line.startswith(f"{key}="):
                f.write(f"{key}={value}\n")
                found = True
            else:
                f.write(line)
        if not found:
            f.write(f"{key}={value}\n")

def encrypt_password(raw_password, key):
    # Enkripsi password dan simpan ke .env
    cipher = Fernet(key)
    encrypted_password = cipher.encrypt(raw_password.encode()).decode()
    update_env("PASSW", encrypted_password)

def main():
    # Ambil return dari get_env & encrypt password
    data = get_env()
    encrypt_password(data["raw_password"], data["key"])
    print("[INFO] 🔒 Password berhasil dienkripsi dan disimpan ke .env")

main()