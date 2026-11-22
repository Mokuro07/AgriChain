@echo off
title Buka SimpleAgriChain di VS Code
cd /d "%~dp0"

set CODE="C:\Tools\VS Code\Microsoft VS Code\bin\code.cmd"
if not exist %CODE% (
    where code >nul 2>&1 && set CODE=code
)

echo [SimpleAgriChain] Membuka folder proyek di VS Code...
%CODE% .
