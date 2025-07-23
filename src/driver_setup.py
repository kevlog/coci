import os
import sys
import platform
import winreg
import shutil
import threading
import requests
import time
import zipfile
from threading import Thread, Event
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import edgedriver_autoinstaller
from spinner import spinner

# Fungsi untuk mencetak spinner selama proses unduhan (optional)
def print_spinner():
    import itertools
    import sys
    for char in itertools.cycle(r"|/-\\"):
        sys.stdout.write(f"\r{char}")
        sys.stdout.flush()

# Fungsi untuk mendeteksi sistem operasi
def detect_os():
    system = platform.system()
    machine = platform.machine()

    if system == "Windows":
        if machine == "AMD64" or machine == "x86_64":
            return "Windows x64"
        else:
            return "Windows x86"
    elif system == "Darwin":  # macOS
        if "arm" in machine.lower():  # Untuk Mac dengan chip M1/M2
            return "Mac M1"
        else:
            return "Mac"
    elif system == "Linux":
        return "Linux"
    else:
        raise ValueError("Sistem operasi tidak didukung.")

# Fungsi untuk mengunduh dan mengekstrak driver berdasarkan OS yang terdeteksi
def download_and_extract_driver(edge_version, custom_driver_file):
    os_choice = detect_os()

    # Tentukan URL berdasarkan OS
    if os_choice == "Windows x86":
        url = f"https://msedgedriver.microsoft.com/{edge_version}/edgedriver_win32.zip"
    elif os_choice == "Windows x64":
        url = f"https://msedgedriver.microsoft.com/{edge_version}/edgedriver_win64.zip"
    elif os_choice == "Mac M1":
        url = f"https://msedgedriver.microsoft.com/{edge_version}/edgedriver_mac64_m1.zip"
    elif os_choice == "Mac":
        url = f"https://msedgedriver.microsoft.com/{edge_version}/edgedriver_mac64.zip"
    elif os_choice == "Linux":
        url = f"https://msedgedriver.microsoft.com/{edge_version}/edgedriver_linux64.zip"
    else:
        print(f"[ERROR] OS pilihan '{os_choice}' tidak valid.")
        return
    
    # Unduh file ZIP
    print(f"[INFO] 🔌 Mengunduh driver versi {edge_version} untuk {os_choice}")
    response = requests.get(url)
    response.raise_for_status()  # Pastikan permintaan berhasil (status code 200)

    # Ekstrak file ZIP
    print(f"[INFO] 📦 Mengekstrak driver")
    with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
        # Tentukan folder sementara untuk mengekstrak
        extract_folder = "temp_driver"
        os.makedirs(extract_folder, exist_ok=True)
        zip_ref.extractall(extract_folder)

    # Cari msedgedriver.exe dan ganti nama serta pindahkan
    msedgedriver_path = None
    for root, dirs, files in os.walk(extract_folder):
        if 'msedgedriver.exe' in files:
            msedgedriver_path = os.path.join(root, 'msedgedriver.exe')
            break

    if msedgedriver_path:
        # Ganti nama dan pindahkan
        new_driver_name = f"msedgedriver_{edge_version}.exe"
        # new_driver_path = os.path.join(custom_driver_file, new_driver_name)

        shutil.move(msedgedriver_path, custom_driver_file)
        print(f"\n[INFO] ✅ Driver {new_driver_name} berhasil diunduh dan dipindahkan ke: {custom_driver_file}")
    else:
        print("[ERROR] Tidak dapat menemukan msedgedriver.exe dalam file ZIP.")

    # Hapus folder sementara
    shutil.rmtree(extract_folder)

# Fungsi untuk memulai thread spinner (opsional, jika kamu ingin spinner saat proses berlangsung)
# def start_spinner_thread():
#     spinner_thread = Thread(target=print_spinner)
#     spinner_thread.daemon = True
#     return spinner_thread

def get_edge_version():
    try:
        reg_path = r"SOFTWARE\Microsoft\Edge\BLBeacon"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path) as key:
            version, _ = winreg.QueryValueEx(key, "version")
            return version
    except Exception as e:
        print(f"[ERR] Gagal membaca versi Edge dari Registry: {e}")
        return None

def is_site_reachable(url: str) -> bool:
    try:
        response = requests.get(url, timeout=5)  # Timeout setelah 5 detik
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
    
def download_driver(driver_filename, custom_driver_file, edge_version):
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner, args=(f"📥 Mengunduh driver Edge versi {edge_version}", stop_event))

    driver_url = "https://msedgedriver.azureedge.net" # diambil dari class EdgeChromiumDriverManager
    retries = 3
    attemp = 0

    # if not is_site_reachable(driver_url):
    #     print(f"\n[ERR]  ❌ Tidak dapat mengakses situs {driver_url}. Pastikan koneksi internet Anda stabil.")
    #     print(f"[WARN] ⚠️ Jika koneksi Anda sedang stabil, maka masalah terjadi pada situs di atas yang gagal diakses.")
    #     print(f"[WARN] 🙏 Silahkan tunggu beberapa saat dan coba lagi.")
    #     stop_event.set()
    #     spinner_thread.join()
    #     for i in range(5, 0, -1):
    #         sys.stdout.write(f"\r[INFO] 🕒 Menutup aplikasi dalam {i} detik" + "." * (4 - i))
    #         sys.stdout.flush()
    #         time.sleep(1)
    #     exit()  # Keluar jika situs tidak dapat dijangkau

    while attemp < retries:
        try:
            if is_site_reachable(driver_url):
                print("[INFO] 🥇 Opsi 1: Mengunduh driver dengan EdgeChromium Driver Manager.")
                spinner_thread.start()
                
                driver_path = EdgeChromiumDriverManager(version=edge_version).install()
                stop_event.set()
                spinner_thread.join()

                shutil.move(driver_path, custom_driver_file)
                print(f"\n[INFO] ✅ Driver {driver_filename} berhasil diunduh dan dipindahkan ke: {custom_driver_file}")
                attemp += 3
            else:
                print("[INFO] 🥈 Opsi 2: Mengunduh driver secara manual")
                # spinner_thread.start()
                # spinner_thread = start_spinner_thread()

                # Proses unduhan dan ekstraksi
                try:
                    download_and_extract_driver(edge_version, custom_driver_file)
                except Exception as e:
                    print(f"[ERROR] Terjadi kesalahan: {e}")
                finally:
                    # Menghentikan spinner setelah selesai
                    stop_event.set()
                    spinner_thread.join()
    
                # shutil.move(driver_path, custom_driver_file)
                # print(f"\n[INFO] ✅ Driver {driver_filename} berhasil diunduh dan dipindahkan ke: {custom_driver_file}")
                attemp += 3
        except requests.exceptions.RequestException as e:
            print(f"[ERR]  ❌ Koneksi gagal: {e}. Coba lagi...")
            stop_event.set()
            spinner_thread.join()
        except Exception as e:
            stop_event.set()
            spinner_thread.join()
            print(f"[ERR]  ❌ Gagal mengunduh driver versi {edge_version}. Detail: {e}")
        finally:
            attemp+=1
            if attemp < retries:
                time.sleep(2)
            else:
                stop_event.set()
                spinner_thread.join()
            break

def setup_driver(options=None):
    # Ambil versi Edge
    edge_version = get_edge_version()
    if not edge_version:
        print("[ERR]  ❌ Tidak bisa menentukan versi Microsoft Edge.")
        exit()

    # Tentukan nama dan path driver berdasarkan versi
    print(f"[INFO] 📜 Versi Microsoft Edge saat ini: {edge_version}")
    custom_driver_path = "./assets/driver"
    os.makedirs(custom_driver_path, exist_ok=True)
    driver_filename = f"msedgedriver_{edge_version}.exe"
    custom_driver_file = os.path.join(custom_driver_path, driver_filename)

    # Ambil semua file yang cocok pola msedgedriver_*.exe
    driver_files = [f for f in os.listdir(custom_driver_path) if f.startswith("msedgedriver_") and f.endswith(".exe")]

    try:
        if driver_filename in driver_files:
            # ✅ Driver ada
            print(f"[INFO] ✅ Driver ditemukan di : {custom_driver_path}")
        elif driver_files:
            # ⚠️ Ada driver tapi beda versi → hapus semua
            print(f"[INFO] ⚠️ Driver ditemukan namun versinya tidak cocok dengan Edge yang terinstall!")
            print(f"[INFO] 🧹 Menghapus driver lama yang tidak cocok.")
            for file in driver_files:
                try:
                    os.remove(os.path.join(custom_driver_path, file))
                    print(f"[INFO] 🗑️ Berhasil menghapus: {file}")
                except Exception as e:
                    print(f"[WARN] ⚠️ Gagal menghapus {file}: {e}")
            download_driver(driver_filename, custom_driver_file, edge_version)
        else:
            # ❌ Driver tidak ditemukan
            print("[INFO] 🙏 Driver tidak ditemukan")
            download_driver(driver_filename, custom_driver_file, edge_version)

    except Exception as e:
        print(f"[ERR] ❌ Gagal mengunduh atau memvalidasi driver. Detail: {e}\a")
        for i in range(5, 0, -1):
            sys.stdout.write(f"\r[INFO] 🕒 Menutup aplikasi dalam {i} detik" + "." * (4 - i))
            sys.stdout.flush()
            time.sleep(1)
        exit()  # Keluar jika situs tidak dapat dijangkau

    try:
        service = EdgeService(executable_path=custom_driver_file)
        driver = webdriver.Edge(service=service, options=options)
        print("[INFO] 🚑 Driver berhasil dijalankan.")
        return driver
    except Exception as e:
        print(f"[INFO] ⚒️ Versi Microsoft Edge: {edge_version}")
        print(f"[ERR]  ❌ Gagal menginisialisasi driver. Detail: {e}\a")
        for i in range(20, 0, -1):
            sys.stdout.write(f"\r[INFO] 🕒 Menutup aplikasi dalam {i} detik" + "." * (4 - i))
            sys.stdout.flush()
            time.sleep(1)
        exit()  # Keluar jika situs tidak dapat dijangkau
