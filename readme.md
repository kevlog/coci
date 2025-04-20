# 🕒 Auto Clock-In / Clock-Out (Auto COCI)

Otomatisasi absensi PeoplesHR via browser Microsoft Edge.

---

## 🧰 Tools yang Dibutuhkan

1. **Microsoft Edge** – sebagai browser utama.
2. **WebDriver Microsoft Edge** – untuk mengotomatisasi browser.
3. **Python** – untuk menjalankan script automation.

---

## 🚀 Cara Menggunakan

1. Clone atau download repo ini pake git clone
2. **Pindahkan folder repo ke `C:\`**  
   → Supaya kamu cukup isi username dan password saja (tidak perlu isi path Python script).
3. Rename folder menjadi coci
4. Buka folder repo tersebut, lalu **buat shortcut file `run_auto_coci.bat`** ke lokasi mana pun (misalnya: Desktop).  
   ⚠️ *Ingat, **buat shortcut** ya, jangan di-*copy*!
5. Klik dua kali file shortcut `run_auto_coci.bat`.
7. Aplikasi akan menyiapkan semua yang dibutuhkan seperti: Instalasi Python (jika belum terinstall), Package Python yg dibutuhkan dan driver Microsoft Edge berdasarkan versi Microsoft Edge yang sudah terinstall.
8. Masukkan username dan password akun PeoplesHR.
9. Masukkan path direktori `auto_coci.py` (misal: `C:\Users\ASUS-ROG\Desktop\coci`)  
   → *Kalau kamu sudah simpan repo di `C:\`, bagian ini akan otomatis dilewati.*
10. Tunggu proses selesai. Aplikasi akan menutup otomatis.

---

## 📝 Catatan

- Menggunakan browser Microsoft Edge.
- Harus download dan masukin `msedgedriver.exe` ke repo ini biar automation bisa berjalan. Udah saya kasih di sini, kalo ga berjalan coba download lagi aja yang terbaru, terus taruh di repo ini. Link tertera di referensi.
- Jika ingin memindahkan `run_auto_coci.bat`, **wajib buat shortcut**, bukan di-*copy* ke tempat lain.
- Shortcut bisa kamu taruh di mana saja, bahkan bisa diatur agar auto-start saat laptop dinyalakan (belum dites 😅).
- Masih ada beberapa validasi yang perlu ditambahkan.
- Kalo mau ubah username dan pass peopleshr bisa di file .env ya (sementara)
- File null tergenerate karena `chcp 65001 >null` di file bat
- Udah ada fitur auto-install Python (biar makin praktis).
- Masih harus pake git clone buat dapetin aplikasinya, gatau kenapa kalo dari Download Zip di tombol Code warna hijau itu, ataupun dari Download Zip di Release, dia ga bakal bisa dibuka, aneh wkwk
- Di rilis v1.2.0 udah bisa jalan dari Download Zip, ternyata masalahnya ada di CRLF yang berubah menjadi LF saat diunduh dari GitHub (tidak untuk clone)
- Kalo hasil dari download zip gabisa dibuka, kamu bisa jalankan convert_to_crlf.ps1 menggunakan PowerShell. Caranya tinggal klik kanan lalu pilih 'open in powershell'
- Okedeh, segini dulu yak catetannya..

---

## ❓ FAQ

### Kenapa selalu muncul instalasi `python-dotenv` meskipun sudah diinstall sebelumnya?

Biasanya terjadi jika kamu menginstall Python lewat **Microsoft Store**.

#### Kenapa bisa begitu?

Karena Python dari Microsoft Store:
- Terisolasi di direktori khusus.
- Pip menginstall ke user site-packages (`--user` mode), bukan global.
- Beberapa alat Python (termasuk `__import__`) dan `PYTHONPATH` tidak sinkron dengan site-packages user.

### Solusi?

Install Python dari website resminya: https://www.python.org/downloads/

---

## 🔗 Referensi

- [📥 Download Python](https://www.python.org/downloads/)
- [🌐 Download Microsoft Edge](https://www.microsoft.com/id-id/edge/download?form=MA13FJ)
- [📦 Download Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH#installation)
- [📚 Dokumentasi Edge WebDriver](https://learn.microsoft.com/en-us/microsoft-edge/webdriver-chromium/?tabs=c-sharp&form=MA13LH)
