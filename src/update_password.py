import os
import sys
import threading
import base64
import itertools
import time
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

def spinner(text, stop_event):
    spin = itertools.cycle(['⠋', '⠙', '⠸', '⠴', '⠦', '⠇'])
    while not stop_event.is_set():
        sys.stdout.write(f'\r[INFO]  {next(spin)} {text}')
        sys.stdout.flush()
        time.sleep(0.1)
    print()

def get_env():
    load_dotenv()
    raw_password = os.getenv("PASSW")
    if not raw_password: # Jika password tidak ada, minta user untuk memasukkan password
        raw_password = reset_password()
    return raw_password

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

def gen_key():
    fernet_key = Fernet.generate_key()
    cipher = Fernet(fernet_key)
    return fernet_key, cipher

def is_valid_key():
    load_dotenv()
    key = os.getenv("CODE")

    if not key:
        # print("[WARN] ⚠️ Kunci belum ditemukan di .env")
        return False

    try:
        # Uji apakah key bisa didecode dari base64 dan membentuk cipher Fernet
        decoded_key = base64.urlsafe_b64decode(key)
        if len(decoded_key) != 32:
            print("[ERR]  ❌ Kunci tidak memiliki panjang 32-byte")
            return False

        _ = Fernet(key)  # Akan gagal jika key tidak valid
        return True
    except Exception as e:
        print(f"[ERR]  ❌ Kunci tidak valid.")
        print(f"          Detail: {e}")
        return False

def is_encrypted(password: str) -> bool:
    password = password.strip()
    load_dotenv()
    key = os.getenv("CODE")
    is_decryptable = is_decryptable_password(password, key)
    rule = password.startswith("gAAAA") and len(password) > 80 and password.endswith("==") or is_decryptable
    return rule

def is_decryptable_password(password: str, key: str) -> bool:
    try:
        cipher = Fernet(key)
        _ = cipher.decrypt(password.encode())
        return True
    except InvalidToken:
        return False
    except Exception as e:
        # print(f"[ERR]  ❌ Gagal decrypt: {e}")
        return False
    
def is_valid(raw_password):
    encrypt_password = is_encrypted(raw_password)
    key_valid = is_valid_key()
    if encrypt_password and key_valid:
        print("1")
        print("[INFO] 🔒 Password sudah terenkripsi. Lewati proses enkripsi.")
    elif encrypt_password and not key_valid:
        print("2")
        raw_password_ = reset_password()
        load_encrpypt_password(raw_password_)
    elif not encrypt_password and not key_valid: #ketika user baru pertama kali pakai
        load_encrpypt_password(raw_password)
    elif not encrypt_password and key_valid:
        print("[INFO] 🔒 Password belum terenkripsi.")
        print("4")
        load_encrpypt_password(raw_password)
    else:
        encrypt_password(raw_password)
        print("[INFO] 🔒 Password berhasil dienkripsi dan disimpan ke .env")

def load_encrpypt_password(raw_password):
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner, args=("Mengenkripsi password..", stop_event))
    spinner_thread.start()
    time.sleep(2)  # Simulasi proses
    stop_event.set()
    spinner_thread.join()
    encrypt_password(raw_password)
    print("[INFO] 🔒 Password berhasil dienkripsi!")

def encrypt_password(raw_password):
    # Enkripsi password dan simpan ke .env
    fernet_key, cipher = gen_key()
    encrypted_password = cipher.encrypt(raw_password.encode()).decode()
    key = fernet_key.decode()
    update_env("PASSW", encrypted_password)
    update_env("CODE", key)

def reset_password():
    print("[INFO] 🔑 UP Masukkan password untuk disimpan: ", end="", flush=True)
    raw_password = input()

    while not raw_password.strip():
        raw_password = input("[WARN] ❗ Password tidak boleh kosong. Masukkan ulang: ").strip()
    
    update_env("PASSW", raw_password)
    return raw_password
    
def main():
    # Ambil return dari get_env & encrypt password
    raw_password = get_env()
    is_valid(raw_password)

main()