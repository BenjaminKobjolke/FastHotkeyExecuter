@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting FastHotkeyExecuter...
python src/main.py
pause
