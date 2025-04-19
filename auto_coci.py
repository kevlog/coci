from package_checker import check_and_install_packages

# Daftar paket yang diperlukan
required_packages = [
    ("selenium", "selenium"),
    ("python-dotenv", "dotenv")
]

# Memeriksa dan menginstal paket yang hilang
check_and_install_packages(required_packages)

import subprocess
import sys
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# === Logging ke terminal dan file ===
class LoggerWriter:
    def __init__(self, stream, logfile):
        self.stream = stream
        self.logfile = open(logfile, "a", encoding="utf-8")

    def write(self, message):
        if message.strip():
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_line = f"[{timestamp}] {message}"
            self.stream.write(message)
            self.logfile.write(log_line)
        else:
            self.stream.write(message)
            self.logfile.write(message)

    def flush(self):
        self.stream.flush()
        self.logfile.flush()

sys.stdout = LoggerWriter(sys.stdout, "log.log")
sys.stderr = LoggerWriter(sys.stderr, "log.log")

# === Load ENV ===
load_dotenv()
username = os.getenv("MY_USERNAME")
password = os.getenv("MY_PASSWORD")

# === Selenium options ===
options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-logging')
options.add_argument('--log-level=3')
options.add_argument("start-maximized")

# === Fungsi utama ===
def main():
    print("\n[INFO] ⌚ Menjalankan Auto Clock-In / Clock-Out ...")
    # Inisialisasi driver
    service = EdgeService(executable_path="msedgedriver.exe")
    driver = webdriver.Edge(service=service, options=options)

    wait = WebDriverWait(driver, 15)

    while True:
        try:
            print("\n[INFO] 🚀 Membuka halaman login...")
            driver.get("https://metrodata.peopleshr.com")
            break  # Keluar dari loop jika berhasil membuka halaman
        except Exception as e:
            error_str = str(e)
            if "net_error -101" in error_str or "SSL" in error_str:
                print("[ERR]  ❌ Gagal melakukan koneksi aman (🔒 SSL handshake failed).\a")
                print("       🧠 Coba periksa 📶jaringan, 🛡️VPN, atau pastikan 📜sertifikat situs valid.")
            else:
                print("[ERR]  ❌ Gagal mengakses situs. 🌐\a")
                print("       🔍 Coba periksa:")
                print("         - 📶 Koneksi internet")
                print("         - 🛡️ VPN atau firewall yang aktif")
                print("         - 📜 Sertifikat SSL situs")
            print(f"[INFO] 🔍 Detail teknis:\n{e}")
            print("[INFO] 📡 Wah sepertinya tidak ada internet nih.")
            print("[INFO] 🌐 Coba sambungin ke internet ya, kami akan coba menghubungkan lagi!")
            time.sleep(3)  # Tunggu 5 detik sebelum mencoba lagi
    try:
        print("[INFO] ⌨️ Mengisi username...")
        username_input = wait.until(EC.presence_of_element_located((By.ID, "txtusername")))
        username_input.send_keys(username)
    except Exception:
        print("[ERR]  ❌ Gagal menemukan field username. Mungkin ID-nya berubah?\a")
        driver.quit()
        exit()

    try:
        print("[INFO] 🔒 Mengisi password...")
        password_input = driver.find_element(By.ID, "txtpassword")
        password_input.send_keys(password)
    except Exception:
        print("[ERR]  ❌ Gagal menemukan field password.\a")
        driver.quit()
        exit()

    try:
        print("[INFO] ➡️ Menekan tombol login...")
        login_button = driver.find_element(By.ID, "btnsubmit")
        login_button.click()
    except Exception:
        print("\a")
        print("[ERR]  ❌ Gagal klik tombol login.")
        driver.quit()
        exit()

    try:
        print("[INFO] 🕵️ Menunggu elemen Clock In/Out...")
        man_swipe = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ManSwipe")))
        
        # Scroll biar elemen terlihat di layar
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", man_swipe)
        time.sleep(1)  # Delay dikit biar efek scroll kelihatan
        
        # man_swipe.click()
        print("[INFO] ✅ Berhasil klik Tombol Clock In/Out!")

        print("[INFO] 🧹 Menutup browser dalam 3 detik", end="", flush=True)
        # Animasi titik-titik selama 1,5 detik
        for _ in range(3):
            time.sleep(0.5)
            sys.stdout.write(".")
            sys.stdout.flush()
        # Ada jeda 1,5 setelah titik terakhir biar pas 3 detik
        time.sleep(1.5)

        print("\n[INFO] ✅ Browser ditutup. Sampai jumpa!")
        driver.quit()

        for i in range(3, 0, -1):
            sys.stdout.write(f"\r[INFO] 🕒 Menutup aplikasi dalam {i} detik" + "." * (4 - i))
            sys.stdout.flush()
            time.sleep(1)
            
        # print("[INFO] 🕒 Menutup aplikasi dalam 3 detik", end="", flush=True)
        # Animasi titik-titik selama 1,5 detik
        # for _ in range(3):
        #     time.sleep(0.5)
        #     sys.stdout.write(".")
        #     sys.stdout.flush()
        # Jeda ladgi 1,5 detik biar pas 3 detik
        time.sleep(1.5)
        exit()
        
    except Exception:
        print("[ERR]  ❌ Gagal menemukan atau klik elemen 'ManSwipe' / tombol Clock In/Out. Pastikan login sukses.\a")
        driver.quit()
        # Countdown dengan animasi titik
        for i in range(3, 0, -1):
            sys.stdout.write(f"\r[INFO] 🕒 Menutup aplikasi dalam {i} detik" + "." * (4 - i))
            sys.stdout.flush()
            time.sleep(1)
        # print("🕒 Menutup aplikasi dalam 3 detik", end="", flush=True)
        # Animasi titik-titik selama 1,5 detik
        # for _ in range(3):
        #     time.sleep(0.5)
        #     sys.stdout.write(".")
        #     sys.stdout.flush()
        # Jeda ladgi 1,5 detik biar pas 3 detik
        # time.sleep(1.5)
        exit()

    time.sleep(5)
    driver.quit()
    exit()

# === Eksekusi dengan handler Ctrl+C ===
try:
    main()
except KeyboardInterrupt:
    print("\n[WARN] ⚠️  Deteksi interupsi dari keyboard (Ctrl+C).")
    try:
        confirm = input("❓ Yakin ingin membatalkan proses? (y/n): ").lower()
        if confirm == 'y':
            print("\a")
            print("[WARN] ⛔ Proses dibatalkan oleh pengguna.")
            exit()
        else:
            print("[INFO] ✅ Proses akan dilanjutkan...\n")
            main()  # Jalankan ulang
    except Exception:
        print("[ERR]  ❌ Terjadi kesalahan saat konfirmasi. Keluar.")
        exit()