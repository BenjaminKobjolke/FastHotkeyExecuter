@echo off
REM Move to the folder containing this .bat
cd /d %~dp0

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting FastHotkeyExecuter...
python main.py
