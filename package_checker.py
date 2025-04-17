# package_checker.py
import subprocess
import sys
print(f"Using Python at: {sys.executable}")

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
    # Memeriksa paket yang hilang
    missing_packages = [package for package, _ in required_packages if install_if_missing(package)]

    # Menampilkan daftar paket yang hilang ke pengguna
    if missing_packages:
        print("\n📦 Daftar paket yang belum terinstal:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\n🔧 Memulai instalasi...")

        # Instalasi paket yang hilang
        for package in missing_packages:
            print(f"📦 Installing package: {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    else:
        print("✅ Semua paket sudah terinstal!")

    print("🎉 Proses instalasi selesai!")
