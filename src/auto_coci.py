import sys
import os
import threading
import time
from datetime import datetime
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import InvalidSessionIdException
from urllib3.exceptions import ProtocolError
from dotenv import load_dotenv
from read_password import load_access
from driver_setup import setup_driver
from spinner import spinner

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
    # Siapkan opsi browser jika perlu
    options = Options()
    options.add_argument("--start-maximized")

    # Inisialisasi driver lewat function modular
    driver = setup_driver(options)

    print("[INFO] ⌚ Menjalankan Auto Clock-In / Clock-Out")
    
    wait = WebDriverWait(driver, 15)

    while True:
        try:
            print("[INFO] 🚀 Membuka halaman login")
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
        print("[INFO] ⌨️ Mengisi username")
        username_input = wait.until(EC.presence_of_element_located((By.ID, "txtusername")))
        username_input.send_keys(username)
    except Exception:
        print("[ERR]  ❌ Gagal menemukan field username. Mungkin ID-nya berubah?\a")
        time.sleep(3)
        driver.quit()
        exit()

    try:
        print("[INFO] 🔒 Mengisi password")
        password_input = driver.find_element(By.ID, "txtpassword")
        password_input.send_keys(password)
    except Exception:
        print("[ERR]  ❌ Gagal menemukan field password.\a")
        time.sleep(3)
        driver.quit()
        exit()

    try:
        print("[INFO] ➡️ Menekan tombol login")
        login_button = driver.find_element(By.ID, "btnsubmit")
        try:
            login_button.click()
            time.sleep(1)
        except NoSuchWindowException:
            driver.quit()
            print("\n[ERR]  ❌ Browser telah ditutup secara paksa. Program akan dihentikan.\a")
            delNull()
            # Countdown dengan animasi titik
            for i in range(3, 0, -1):
                sys.stdout.write(f"\r[INFO] 🕒 Menutup aplikasi dalam {i} detik" + "." * (4 - i))
                sys.stdout.flush()
                time.sleep(1)
            exit()
        except Exception as e:
            print(f"[ERR]  ❌Gagal klik tombol login.")
            raise

        try:
            alerts = driver.find_elements(By.ID, "myAlert")
        except NoSuchWindowException:
            driver.quit()
            print("\n[ERR]  ❌ Browser telah ditutup secara paksa. Program akan dihentikan.\a")
            delNull()
            # Countdown dengan animasi titik
            for i in range(3, 0, -1):
                sys.stdout.write(f"\r[INFO] 🕒 Menutup aplikasi dalam {i} detik" + "." * (4 - i))
                sys.stdout.flush()
                time.sleep(1)
            exit()
        
        except ProtocolError as e:
            print(f"\n[ERR]  ❌ Koneksi terputus: {e}")
            delNull()
            exit()
        
        except ConnectionResetError as e:
            driver.quit()
            print(f"\n[ERR]  ❌ Koneksi terputus oleh host: {e}")
            delNull()
            exit()
        
        except InvalidSessionIdException as e:
            print("[ERR]  ❌ Invalid Session Id Exception, kemungkinan karena Browser ditutup paksa.")
            print(f"[ERR]  📝 Detail error:\n {e}")
            delNull()
            # Countdown dengan animasi titik
            for i in range(15, 0, -1):
                sys.stdout.write(f"\r[INFO] 🕒 Menutup aplikasi dalam {i} detik ")
                sys.stdout.flush()
                time.sleep(1)
            exit()

        except Exception as e:
            print(f"\n[ERR]  ❌ Error: {e}")
            delNull()
            # Countdown dengan animasi titik
            for i in range(3, 0, -1):
                sys.stdout.write(f"\r[INFO] 🕒 Menutup aplikasi dalam {i} detik" + "." * (4 - i))
                sys.stdout.flush()
                time.sleep(1)
            exit()


        if alerts:
            body_text = alerts[0].text.lower()
            if "please enter the correct username" in body_text:
                print("[ERR]  ❌ Login gagal. Pastikan username dan password benar!")
                time.sleep(2)
                driver.quit()
                delNull()
                # Countdown dengan animasi titik
                for i in range(3, 0, -1):
                    sys.stdout.write(f"\r[INFO] 🕒 Menutup aplikasi dalam {i} detik" + "." * (4 - i))
                    sys.stdout.flush()
                    time.sleep(1)
                exit()
        else:
            try:
                stop_event = threading.Event()
                spinner_thread = threading.Thread(target=spinner, args=(f"📄 Sedang memuat halaman", stop_event))
                spinner_thread.start()

                # Tunggu hingga elemen halaman berhasil dimuat
                wait.until(EC.presence_of_element_located((By.ID, "divLayout")))

                stop_event.set()
                spinner_thread.join()
                print("\n[INFO] 🎉 Halaman berhasil dimuat.")

            except NoSuchWindowException:
                driver.quit()
                stop_event.set()
                spinner_thread.join()
                print("\n[ERR]  ❌ Browser telah ditutup secara paksa. Program akan dihentikan.\a")
                delNull()
                # Countdown dengan animasi titik
                for i in range(3, 0, -1):
                    sys.stdout.write(f"\r[INFO] 🕒 Menutup aplikasi dalam {i} detik" + "." * (4 - i))
                    sys.stdout.flush()
                    time.sleep(1)
                exit()
            
            except ProtocolError as e:
                driver.quit()
                stop_event.set()
                spinner_thread.join()
                print(f"\n[ERR]  ❌ Koneksi terputus: {e}")
                delNull()
                # Countdown dengan animasi titik
                for i in range(3, 0, -1):
                    sys.stdout.write(f"\r[INFO] 🕒 Menutup aplikasi dalam {i} detik" + "." * (4 - i))
                    sys.stdout.flush()
                    time.sleep(1)
                exit()
            
            except ConnectionResetError as e:
                driver.quit()
                stop_event.set()
                spinner_thread.join()
                print(f"\n[ERR]  ❌ Koneksi terputus oleh host: {e}")
                delNull()
                # Countdown dengan animasi titik
                for i in range(3, 0, -1):
                    sys.stdout.write(f"\r[INFO] 🕒 Menutup aplikasi dalam {i} detik" + "." * (4 - i))
                    sys.stdout.flush()
                    time.sleep(1)
                exit()

            except Exception as e:
                driver.quit()
                stop_event.set()
                spinner_thread.join()
                print(f"\n[ERR]  ❌ 1 Error: {e}")
                delNull()
                # Countdown dengan animasi titik
                for i in range(3, 0, -1):
                    sys.stdout.write(f"\r[INFO] 🕒 Menutup aplikasi dalam {i} detik" + "." * (4 - i))
                    sys.stdout.flush()
                    time.sleep(1)
                exit()

            except KeyboardInterrupt:
                driver.quit()
                stop_event.set()
                spinner_thread.join()
                print("\n[WARN] ⚠️ Program dihentikan oleh pengguna (CTRL+C).")
                driver.quit()
                delNull()
                # Countdown dengan animasi titik
                for i in range(3, 0, -1):
                    sys.stdout.write(f"\r[INFO] 🕒 Menutup aplikasi dalam {i} detik" + "." * (4 - i))
                    sys.stdout.flush()
                    time.sleep(1)
                exit()
    
    except NoSuchWindowException:
        print("\n[ERR]  ❌ Browser telah ditutup secara paksa. Program akan dihentikan.\a")        
        delNull()
        # Countdown dengan animasi titik
        for i in range(3, 0, -1):
            sys.stdout.write(f"\r[INFO] 🕒 Menutup aplikasi dalam {i} detik" + "." * (4 - i))
            sys.stdout.flush()
            time.sleep(1)
        exit()
    
    except ProtocolError as e:
        print(f"\n[ERR]  ❌ Koneksi terputus: {e}")
        delNull()
        # Countdown dengan animasi titik
        for i in range(3, 0, -1):
            sys.stdout.write(f"\r[INFO] 🕒 Menutup aplikasi dalam {i} detik" + "." * (4 - i))
            sys.stdout.flush()
            time.sleep(1)
        exit()
    
    except ConnectionResetError as e:
        print(f"\n[ERR]  ❌ Koneksi terputus oleh host: {e}")
        delNull()
        # Countdown dengan animasi titik
        for i in range(3, 0, -1):
            sys.stdout.write(f"\r[INFO] 🕒 Menutup aplikasi dalam {i} detik" + "." * (4 - i))
            sys.stdout.flush()
            time.sleep(1)
        exit()
    
    except InvalidSessionIdException as e:
        print(f"\n[ERR]  ❌ Invalid Session Id Exception caught: {e}")
        delNull()
        # Countdown dengan animasi titik
        for i in range(3, 0, -1):
            sys.stdout.write(f"\r[INFO] 🕒 Menutup aplikasi dalam {i} detik" + "." * (4 - i))
            sys.stdout.flush()
            time.sleep(1)
        exit()
            
    except Exception as e:
        print("\a")
        print(f"[ERR]  ❌ Error: {e}")
        driver.quit()
        delNull()
        # Countdown dengan animasi titik
        for i in range(3, 0, -1):
            sys.stdout.write(f"\r[INFO] 🕒 Menutup aplikasi dalam {i} detik" + "." * (4 - i))
            sys.stdout.flush()
            time.sleep(1)
        exit()

    try:
        stop_event = threading.Event()
        spinner_thread = threading.Thread(target=spinner, args=(f"🕵️ Mencari elemen Clock In/Out", stop_event))
        spinner_thread.start()
        man_swipe = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ManSwipe")))
        history = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='History']")))    
        
        try:
            # Scroll biar elemen terlihat di layar
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", man_swipe)
        except Exception:
            raise # Naikan ulang error biar ketangkap di outer try-except

        time.sleep(1)  # Delay dikit biar efek scroll kelihatan

        try:
            man_swipe.click()
            stop_event.set()
            spinner_thread.join()
            print("\n[INFO] 👆 Berhasil klik Tombol Clock In/Out!")
        except Exception:
            print("\n[ERR]  ❌ Gagal menemukan atau klik elemen 'ManSwipe' / tombol Clock In/Out.")
            raise

        time.sleep(2)  # Delay dikit tunggu presensi kesimpan

        try:
            history.click()
            print("[INFO] 📋 Berhasil menampilkan history presensi!")
        except Exception:
            print("[ERR]  ❌ Gagal menemukan tombol History.")
            raise

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

        time.sleep(1.5)
        exit()
    
    except Exception:
        stop_event.set()
        spinner_thread.join()
        print("\n[ERR]  ❌ Gagal menemukan tombol Clock In/Out. Pastikan menggunakan Bahasa Inggris!\a")
        driver.quit()
        delNull()
        # Countdown dengan animasi titik
        for i in range(3, 0, -1):
            sys.stdout.write(f"\r[INFO] 🕒 Menutup aplikasi dalam {i} detik" + "." * (4 - i))
            sys.stdout.flush()
            time.sleep(1)
        exit()

    time.sleep(5)
    driver.quit()
    exit()

# === Eksekusi dengan handler Ctrl+C ===
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