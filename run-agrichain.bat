@echo off
title SimpleAgriChain Launcher
cd /d "%~dp0"

echo [SimpleAgriChain] Memulai Web Server...
start "" /b ".venv\Scripts\python.exe" app.py

echo [SimpleAgriChain] Menunggu server aktif di port 5000...
set /a attempts=0

:poll_loop
call :sleep 2
curl -s -f -o nul http://127.0.0.1:5000/healthz
if %errorlevel% equ 0 goto server_ready

set /a attempts+=1
if %attempts% geq 20 (
    echo [ERROR] Server gagal merespons di port 5000 setelah 20 detik.
    exit /b 1
)
goto poll_loop

:server_ready
echo [SimpleAgriChain] Server siap! Membuka browser default...
start http://127.0.0.1:5000
echo SimpleAgriChain aktif di http://127.0.0.1:5000
exit /b 0

:sleep
ping -n %1 127.0.0.1 >nul 2>&1
exit /b
