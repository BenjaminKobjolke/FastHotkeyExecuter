@echo off
call activate_environment.bat
if exist compile_settings.bat call compile_settings.bat

if defined OUTPUT_PATH (set "TARGET=%OUTPUT_PATH%") else (set "TARGET=%~dp0")
set "SENTINEL=%TARGET%\.shutdown"

echo Requesting graceful shutdown of any running instance...
echo shutdown > "%SENTINEL%"

set /a TRIES=0
:waitloop
tasklist /FI "IMAGENAME eq FastHotkeyExecuter.exe" 2>nul | find /I "FastHotkeyExecuter.exe" >nul
if %errorlevel%==0 (
    if %TRIES% GEQ 20 (
        echo Timed out waiting for exit; build may fail if exe is locked.
        goto build
    )
    set /a TRIES+=1
    timeout /t 1 /nobreak >nul
    goto waitloop
)

:build
del "%SENTINEL%" >nul 2>&1
if defined OUTPUT_PATH (
    call pyinstaller --name FastHotkeyExecuter --onefile --windowed main.py --add-data "data;data" --add-data "config;config" --distpath "%OUTPUT_PATH%"
) else (
    call pyinstaller --name FastHotkeyExecuter --onefile --windowed main.py --add-data "data;data" --add-data "config;config"
)
pause
