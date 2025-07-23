@echo off
setlocal enabledelayedexpansion

:: ==========================================
:: Konfigurasi: ubah ini untuk versi terbaru
set "PYTHON_VERSION=3.13.5"
:: ==========================================

echo [INFO] 🔍 Mengecek arsitektur sistem...
set ARCHITECTURE=%PROCESSOR_ARCHITECTURE%
echo [INFO] 💻 Arsitektur terdeteksi: %ARCHITECTURE%

:: Tentukan installer berdasarkan arsitektur
if /I "%ARCHITECTURE%"=="AMD64" (
    set "INSTALLER=python-%PYTHON_VERSION%-amd64.exe"
) else (
    set "INSTALLER=python-%PYTHON_VERSION%.exe"
)

set "URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%INSTALLER%"

:: Cek apakah Python sudah terinstal
echo [INFO] 🧪 Mengecek apakah Python sudah terinstall?
timeout /t 1 >nul
<nul set /p=[INFO] ⏳ Loading
for /l %%i in (1,1,39) do (
    <nul set /p=.
    ping -n 1 127.0.0.1 >nul
)
echo.
timeout /t 1 >nul

python --version >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo [INFO] ✅ Python sudah terinstal!
    for /f "tokens=*" %%i in ('python --version') do set "pyver=%%i"
    echo [INFO] 🐍 Versi !pyver!
    :: Jalankan installer packages Python yang diperlukan
    cd /d %~dp0
    python ../src/package_checker.py
    exit /b
)

echo [WARN] ❌ Python belum ditemukan!!!
echo.

:: Periksa koneksi internet sebelum mengunduh
:check_internet
echo [INFO] 🌐 Memeriksa koneksi internet...
ping -n 1 www.google.com >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERR]  ❌ Tidak ada koneksi internet. Harap periksa koneksi Anda.
    echo [INFO] 🔄 Mencoba menghubungkan ulang.
    <nul set /p=[INFO] ⏳ Loading
    for /l %%i in (1,1,39) do (
        <nul set /p=.
        ping -n 1 www.google.com>nul 2>&1
    )
    timeout /t 1 >nul
    echo.
    echo.
    goto check_internet
)

echo [INFO] 🔗 Koneksi internet tersedia!
echo [INFO] 📡 Memulai proses download dari: %URL%
echo.

:: Jalankan download di background
start /b powershell -Command "Invoke-WebRequest -Uri '%URL%' -OutFile '%INSTALLER%'" >nul 2>&1
<nul set /p=Downloading Python %PYTHON_VERSION% 

:: Tampilkan animasi loading sampai file selesai di-download
set "spinner=\|/-"
set /a index=0
set "size_old=0"
set /a stable_count=0

:loading
:: Proses pengecekan sampai installer dianggap sudah 100% ter-download
IF EXIST "%INSTALLER%" (
for %%A in ("%INSTALLER%") do set "size_new=%%~zA"
    if "%size_new%"=="%size_old%" (
        set /a stable_count+=1
    ) else (
        set "size_old=%size_new%"
        set "stable_count=0"
    )
    :: Kalau ukuran file sudah stabil selama 3 loop berturut-turut (~3 detik), kita anggap selesai
    if !stable_count! GEQ 3 goto install
)

set /a index=!index! %% 4
set "char=!spinner:~%index%,1!"
<nul set /p=!char! 
ping -n 2 127.0.0.1 >nul
<nul set /p=
set /a index+=1
goto loading

:install
echo.
echo.
echo [INFO] ✅ Installer berhasil diunduh.
echo [INFO] ⚙️ Menjalankan instalasi Python...
echo [INFO] 🔔 Jangan lupa centang "Add Python to PATH" sebelum klik Install ya!

:: Jalankan installer dengan GUI agar user tahu
start "" "%INSTALLER%"

echo [INFO] ⏳ Tunggu hingga proses instalasi selesai secara manual.
echo [INFO] 🔄 Setelah selesai, tekan Enter untuk melanjutkan.
echo [INFO] 🚀 Jangan lupa buka kembali aplikasi run_auto_coci.bat setelah Python berhasil diinstal.
pause

::: Hapus installer setelah instalasi selesai
if EXIST "%INSTALLER%" (
    echo.
    echo [INFO] 🗑️ Menghapus file installer...
    del "%INSTALLER%"
    echo [INFO] ✅ File installer berhasil dihapus.
    echo.
) else (
    echo.
    echo [ERR] ❌ Gagal menghapus file installer.
    echo.
)

::: Hapus file "null" yang mungkin tertinggal
if EXIST "null" del "null"

pause

:: Tutup CMD setelah instalasi selesai
echo.
echo [INFO] ❌ Menutup CMD....
echo [INFO] 🔒 Terima kasih telah menggunakan aplikasi ini.
timeout /t 3 >nul
exit