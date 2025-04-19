import subprocess
import sys
import socket
import time

print(f"Using Python at: {sys.executable}")

# Fungsi untuk memeriksa koneksi internet
def check_internet_connection():
    try:
        # Mencoba terhubung ke google.com pada port 80 (HTTP)
        socket.create_connection(("www.google.com", 80), timeout=5)
        return True
    except OSError:
        return False

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
    # Memeriksa koneksi internet hingga tersedia
    while not check_internet_connection():
        print("\n[ERR]  ❌ Tidak ada koneksi internet. Harap periksa koneksi Anda dan coba lagi.\a")
        for i in range(10, 0, -1):
            dot_count = (10 - i) % 3 + 1  # Akan menghasilkan 1, 2, 3, lalu ulang
            sys.stdout.write(f"\r[INFO] Mencoba menghubungkan ulang dalam {i} detik " + "." * dot_count + "   ")  # Extra spasi utk overwrite
            sys.stdout.flush()
            time.sleep(1)

    # Memeriksa paket yang hilang
    missing_packages = [package for package, _ in required_packages if install_if_missing(package)]

    # Menampilkan daftar paket yang hilang ke pengguna
    if missing_packages:
        print("\n[INFO] 📦 Daftar paket yang belum terinstal:\a")
        for package in missing_packages:
            print(f"  - {package}")
        print("\n[INFO] 🔧 Memulai instalasi...")

        # Instalasi paket yang hilang
        for package in missing_packages:
            print(f"[INFO] 📦 Installing package: {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    else:
        print("[INFO] ✅ Semua paket sudah terinstal!")

    print("[INFO] 🎉 Proses instalasi selesai!")
