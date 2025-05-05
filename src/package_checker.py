import os
import subprocess
import sys
import socket
import time
import json
import threading
import itertools

def spinner(text, stop_event):
    dots = itertools.cycle(['.', '..', '...'])
    space = itertools.cycle(['     '])
    spin = itertools.cycle(['⠋', '⠙', '⠸', '⠴', '⠦', '⠇'])
    frame = 0
    dot = next(dots)

    while not stop_event.is_set():
        if frame % 5 == 0:
            dot = next(dots)
        sys.stdout.write(f'\r[INFO] {next(spin)} {text} {dot} {next(space)}')
        sys.stdout.flush()
        time.sleep(0.1)
        frame += 1

# Fungsi untuk memeriksa koneksi internet
def check_internet_connection():
    try:
        # Mencoba terhubung ke google.com pada port 80 (HTTP)
        socket.create_connection(("www.google.com", 80), timeout=5)
        return True
    except OSError:
        return False

# Fungsi untuk get path dari file json
def get_path():
    file_path = os.path.join(os.path.dirname(__file__), "..", "packages.json")
    return file_path

# Fungsi untuk memuat daftar paket yang diperlukan dari file JSON
def load_required_packages(json_path):
    if not os.path.exists(json_path):
        print(f"[ERR] ❌ File '{json_path}' tidak ditemukan.")
        return []
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
        return [(pkg["pip"], pkg["import"]) for pkg in data]
    except (json.JSONDecodeError, KeyError) as e:
        print(f"[ERR] ❌ Gagal memuat paket dari JSON: {e}")
        return []

# Fungsi untuk memeriksa dan menginstal paket yang hilang
def install_if_missing(pip_package, import_name=None):
    try:
        # Coba impor paket yang dimaksud
        __import__(import_name or pip_package)
        return False  # Paket sudah ada
    except ImportError:
        return True  # Paket belum terinstal

# Fungsi untuk memeriksa dan menginstal semua paket yang diperlukan
def check_and_install_packages(required_packages):
    print(f"[INFO] 📂 Using Python at: {sys.executable}")
    print("[INFO] 🔍 Memeriksa paket yang diperlukan")
    # Memeriksa koneksi internet hingga tersedia
    while not check_internet_connection():
        print("[ERR]  ❌ Tidak ada koneksi internet. Harap periksa koneksi Anda dan coba lagi.\a")
        for i in range(10, 0, -1):
            dot_count = (10 - i) % 3 + 1  # Akan menghasilkan 1, 2, 3, lalu ulang
            sys.stdout.write(f"\r[INFO] Mencoba menghubungkan ulang dalam {i} detik " + "." * dot_count + "   ")  # Extra spasi utk overwrite
            sys.stdout.flush()
            time.sleep(1)
        print()

    # Memeriksa paket yang hilang
    missing_packages = []
    for pip_package, import_name in required_packages:
        if install_if_missing(pip_package, import_name):
            missing_packages.append(pip_package)

    # Menampilkan daftar paket yang hilang ke pengguna
    if missing_packages:
        print("\n[INFO] 📦 Daftar paket yang belum terinstal:\a")
        for package in missing_packages:
            print(f"  - {package}")
        print("\n[INFO] 🔧 Memulai instalasi.")

        # Instalasi paket yang hilang
        for package in missing_packages:
            print(f"[INFO] 📦 Installing package: {package}")
            stop_event = threading.Event()
            spinner_thread = threading.Thread(target=spinner, args=(f" Sedang menginstal '{package}'", stop_event))
            spinner_thread.start()
            start = time.time()

            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                duration = round((time.time() - start), 2)
                stop_event.set()
                spinner_thread.join()
                print(f"\n[INFO] 🎁 Berhasil menginstal package: {package} dalam {duration} detik.\n")
            except KeyboardInterrupt:
                stop_event.set()
                spinner_thread.join()
                print("\n[WARN] ⚠️ Instalasi dihentikan oleh pengguna (Ctrl+C).")
                exit()
            except subprocess.CalledProcessError as e:
                stop_event.set()
                spinner_thread.join()
                print(f"[ERR]  ❌ Gagal menginstal paket '{package}'. Detail: {e}\a")
                # sys.exit(1)  # Keluar jika ada kegagalan instalasi
    else:
        print("[INFO] ✅ Semua paket sudah terinstal!")

def main():
    path = get_path()
    check_and_install_packages(load_required_packages(path))

while True:
    try:
        main()
        break # Keluar dari loop jika main() selesai tanpa error
    except KeyboardInterrupt:
        print("\n[WARN] ⚠️  Deteksi interupsi dari keyboard (Ctrl+C).")
        try:
            confirm = input("❓ Yakin ingin membatalkan proses? (y/n): ").lower()
            if confirm == 'y':
                print("\a")
                delNull()
                print("[WARN] ⛔ Proses dibatalkan oleh pengguna.")
                exit()
            else:
                print("[INFO] ✅ Proses akan dilanjutkan\n")
                main()  # Jalankan ulang
        except Exception:
            print("[ERR]  ❌ Terjadi kesalahan saat konfirmasi. Keluar.")
            exit()