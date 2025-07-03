import os
import winreg
import shutil
import threading
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from spinner import spinner

def get_edge_version():
    try:
        reg_path = r"SOFTWARE\Microsoft\Edge\BLBeacon"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path) as key:
            version, _ = winreg.QueryValueEx(key, "version")
            return version
    except Exception as e:
        print(f"[ERR] Gagal membaca versi Edge dari Registry: {e}")
        return None

def download_driver(driver_filename, custom_driver_file, edge_version):
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner, args=(f"📥 Mengunduh driver Edge versi {edge_version}", stop_event))
    spinner_thread.start()

    try:
        driver_path = EdgeChromiumDriverManager(version=edge_version).install()
        stop_event.set()
        spinner_thread.join()

        shutil.move(driver_path, custom_driver_file)
        print(f"\n[INFO] ✅ Driver {driver_filename} berhasil diunduh dan dipindahkan ke: {custom_driver_file}")
    except Exception as e:
        stop_event.set()
        spinner_thread.join()
        print(f"[ERR] ❌ Gagal mengunduh driver versi {edge_version}. Detail: {e}")
        exit()

def setup_driver(options=None):
    # Ambil versi Edge
    edge_version = get_edge_version()
    if not edge_version:
        print("[ERR] Tidak bisa menentukan versi Microsoft Edge.")
        exit()

    # Tentukan nama dan path driver berdasarkan versi
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
        exit()

    try:
        service = EdgeService(executable_path=custom_driver_file)
        driver = webdriver.Edge(service=service, options=options)
        print("[INFO] 🚑 Driver berhasil dijalankan.")
        return driver
    except Exception as e:
        print(f"[ERR] ❌ Gagal menginisialisasi driver. Detail: {e}\a")
        exit()
