@echo off
title Izinkan AgriChain diakses dari HP (butuh izin Administrator)
cd /d "%~dp0"

REM --- pastikan jalan sebagai Administrator ---
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [AgriChain] Meminta izin Administrator... klik "Yes" pada jendela yang muncul.
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

echo [AgriChain] Membuka port 5000 untuk jaringan lokal (Wi-Fi / hotspot)...
netsh advfirewall firewall delete rule name="AgriChain 5000" >nul 2>&1
REM profile=any: Wi-Fi kampus/hotspot sering dikategorikan "Public" oleh Windows,
REM jadi aturan harus berlaku untuk semua tipe jaringan supaya HP bisa membuka.
netsh advfirewall firewall add rule name="AgriChain 5000" dir=in action=allow protocol=TCP localport=5000 profile=any

echo.
echo Selesai. Sekarang HP di jaringan yang sama bisa membuka alamat yang tampil di jendela server.
echo Kalau alamatnya belum tahu: jalankan run-agrichain.bat, alamatnya tertulis "Perangkat lain: http://..."
echo.
pause
