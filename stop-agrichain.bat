@echo off
title SimpleAgriChain Stopper
echo [SimpleAgriChain] Menghentikan server di port 5000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr /r /c:":5000 .*LISTENING"') do (
    if not "%%a"=="0" (
        taskkill /f /pid %%a >nul 2>&1
    )
)
echo Server berhasil dihentikan.
pause
