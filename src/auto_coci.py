import sys
import os
import threading
import time
import itertools
import shutil
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from read_password import load_access

# Spinner
def spinner(text, stop_event):
    dots = itertools.cycle(['.', '..', '...'])
    space = itertools.cycle(['   '])
    frame = 0
    dot = next(dots)

    while not stop_event.is_set():
        if frame % 5 == 0:
            dot = next(dots)
        sys.stdout.write(f'\r[INFO] {text}{dot}{next(space)}')
        sys.stdout.flush()
        time.sleep(0.1)
        frame += 1

# === Path ke file null ===
def delNull():
    # Path ke file ini (auto_coci.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    null_file = os.path.join(current_dir, "..", "null")

    if os.path.exists(null_file):
        os.remove(null_file)
        print(f"[INFO] 🗑️ File '{null_file}' berhasil dihapus.")
    else:
        print(f"[WARN] ⚠️ File '{null_file}' tidak ditemukan.")
    time.sleep(2)

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

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

sys.stdout = LoggerWriter(sys.stdout, "logs/log.log")
sys.stderr = LoggerWriter(sys.stderr, "logs/log.log")

# === Load ENV ===
load_dotenv()
data = load_access()
username = os.getenv("UNAME")
password = data

# === Selenium options ===
options = Options()
options.add_argument('--ignore-certificate-errors') # Abaikan kesalahan sertifikat
options.add_argument('--disable-logging') # Disable logging
options.add_argument('--log-level=3') # Suppress logs
options.add_argument("start-maximized") # Buka jendela penuh
options.add_argument('--inprivate') # Mode InPrivate (Incognito)
options.add_argument('--disable-features=RendererCodeIntegrity') # Disable code integrity checks
options.add_argument('--disable-software-rasterizer') # Disable software rasterizer
options.add_argument('--disable-gpu') # Disable GPU acceleration

# === Fungsi utama ===
def main():
    # Tentukan lokasi custom untuk driver
    custom_driver_path = "./assets/driver"
    os.makedirs(custom_driver_path, exist_ok=True)  # Buat folder jika belum ada
    driver_filename = "msedgedriver.exe"  # Nama file driver
    custom_driver_file = os.path.join(custom_driver_path, driver_filename)

    # Inisialisasi driver Microsoft Edge
    try:
        # Validasi apakah folder dan file driver sudah ada
        if os.path.exists(custom_driver_file):
            print(f"[INFO] ✅ Driver ditemukan di : {custom_driver_path}")
        else:
            print("[INFO] 🙏 Driver tidak ditemukan")
            stop_event = threading.Event()
            spinner_thread = threading.Thread(target=spinner, args=(f"🔄 Mengunduh driver", stop_event))
            spinner_thread.start()

            # Unduh driver menggunakan webdriver-manager
            driver_path = EdgeChromiumDriverManager().install()
            stop_event.set()
            spinner_thread.join()

            # Pindahkah driver ke folder custom
            shutil.move(driver_path, custom_driver_path)
            print(f"\n[INFO] ✅ Driver berhasil diunduh dan dipindahkan ke: {custom_driver_path}")
    except Exception as e:
        stop_event.set()
        spinner_thread.join()
        print(f"[ERR]  ❌ Gagal mengunduh atau memvalidasi driver. Detail: {e}\a")
        exit()

    # Inisialisasi driver
    try:
        service = EdgeService(executable_path=custom_driver_file)
        driver = webdriver.Edge(service=service, options=options)
        print("[INFO] 🚑 Driver berhasil dijalankan.")
    except Exception as e:
        print(f"[ERR]  ❌ Gagal menginisialisasi driver. Detail: {e}\a")
        exit()

    print("[INFO] ⌚ Menjalankan Auto Clock-In / Clock-Out ...")
    
    wait = WebDriverWait(driver, 15)

    while True:
        try:
            print("[INFO] 🚀 Membuka halaman login...")
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
        time.sleep(3)
        driver.quit()
        exit()

    try:
        print("[INFO] 🔒 Mengisi password...")
        password_input = driver.find_element(By.ID, "txtpassword")
        password_input.send_keys(password)
    except Exception:
        print("[ERR]  ❌ Gagal menemukan field password.\a")
        time.sleep(3)
        driver.quit()
        exit()

    try:
        print("[INFO] ➡️ Menekan tombol login...")
        login_button = driver.find_element(By.ID, "btnsubmit")
        login_button.click()
    except Exception:
        print("\a")
        print("[ERR]  ❌ Gagal klik tombol login.")
        time.sleep(3)
        driver.quit()
        exit()

    try:
        print("[INFO] 🕵️ Menunggu elemen Clock In/Out...")
        man_swipe = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ManSwipe")))
        history = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='History']")))
        
        # Scroll biar elemen terlihat di layar
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", man_swipe)
        time.sleep(1)  # Delay dikit biar efek scroll kelihatan
        man_swipe.click()
        print("[INFO] 👆 Berhasil klik Tombol Clock In/Out!")
        time.sleep(2)  # Delay dikit tunggu presensi kesimpan
        history.click()
        print("[INFO] 📋 Berhasil menampilkan history presensi!")
        time.sleep(1)  # Delay dikit biar ada waktu buat user baca history

        # Animasi titik-titik selama 1,5 detik
        for i in range(3, 0, -1):
            sys.stdout.write(f"\r[INFO] 🧹 Menutup browser dalam {i} detik" + "." * (4 - i))
            sys.stdout.flush()
            time.sleep(1)

        print("\n[INFO] ✅ Browser ditutup. Sampai jumpa!")
        delNull()
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
        delNull()
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
            delNull()
            print("[WARN] ⛔ Proses dibatalkan oleh pengguna.")
            exit()
        else:
            print("[INFO] ✅ Proses akan dilanjutkan...\n")
            main()  # Jalankan ulang
    except Exception:
        print("[ERR]  ❌ Terjadi kesalahan saat konfirmasi. Keluar.")
        exit()