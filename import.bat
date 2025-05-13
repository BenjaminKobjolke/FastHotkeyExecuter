@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat

python -m src.import_hotkeys

pause
