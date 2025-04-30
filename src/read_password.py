import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

def get_env():
    load_dotenv()
    password = os.getenv("PASSW")
    fernet_key = os.getenv("CODE")
    return {"password" : password, "fernet_key" : fernet_key}

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
            
def get_password():
    data = get_env()
    password = data["password"]
    fernet_key = data["fernet_key"]
    try:
        if not password or not fernet_key:
            print("[INFO] 🚫 Data .env bermasalah! Memulai reset data .env.\a")
            reset_password()
            return get_password()
        else:
            try:
                # Dekripsi password
                cipher = Fernet(fernet_key.encode())
                original_password = cipher.decrypt(password.encode()).decode()
                return original_password
            except InvalidToken:
                print("[ERR]  ❌ Token tidak valid. Mungkin password terenkripsi salah atau rusak.")
                reset_password()
                return get_password()
                
            except Exception as e:
                print(f"[ERR]  ❌ Error tidak terduga. Detail: {e}")
                print(f"[WARN] ⚠️ Kode enkripsi rusak, buat ulang password!")
                reset_password()
                return get_password()

    except Exception as e:
        print(f"[ERR]  ❌ Error tidak terduga. Detail: {e}")
        os.system("pause")
        return None

def getPassword():
    original_password = get_password()
    return original_password

def reset_password():
    # Enkripsi password dan simpan ke .env
    key = Fernet.generate_key()
    cipher = Fernet(key)
    original_password = input("[INFO] 🔑 RP Masukkan password untuk disimpan: ")
    encrypted_password = cipher.encrypt(original_password.encode()).decode()
    update_env("PASSW", encrypted_password)
    update_env("CODE", key)
    print("[INFO] 🔒 Reset Password berhasil! Terenkripsi dan disimpan ke .env")
    return original_password

def load_access():
    return get_password()

def main():
    return load_access()

main()