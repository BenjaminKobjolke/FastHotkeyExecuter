@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat

python src/import_hotkeys.py
pause
