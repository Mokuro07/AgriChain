@echo off
title SimpleAgriChain - MODE NGODING (auto-reload)
cd /d "%~dp0"

echo [SimpleAgriChain] Mode ngoding: server akan restart sendiri tiap file disimpan.
echo.

REM matikan server lama kalau masih jalan di port 5000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr /r /c:":5000 .*LISTENING"') do (
    if not "%%a"=="0" taskkill /f /pid %%a >nul 2>&1
)

set AGRICHAIN_DEBUG=1
set AGRICHAIN_PORT=5000

start "" /b ".venv\Scripts\python.exe" app.py

echo [SimpleAgriChain] Menunggu server siap...
set /a attempts=0
:poll_loop
call :sleep 2
curl -s -f -o nul http://127.0.0.1:5000/healthz
if %errorlevel% equ 0 goto ready
set /a attempts+=1
if %attempts% geq 20 (
    echo [ERROR] Server gagal start. Cek pesan error di jendela ini.
    exit /b 1
)
goto poll_loop

:ready
echo [SimpleAgriChain] Siap di http://127.0.0.1:5000  (edit file -> otomatis reload)
start http://127.0.0.1:5000
exit /b 0

:sleep
ping -n %1 127.0.0.1 >nul 2>&1
exit /b
