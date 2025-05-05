@echo off
call activate_environment.bat
call pyinstaller --name FastHotkeyExecuter --onefile main.py --add-data "data;data" --add-data "config;config"
pause
