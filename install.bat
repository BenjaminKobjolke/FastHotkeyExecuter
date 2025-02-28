@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing requirements...
pip install -r requirements.txt

echo Checking configuration files...
if not exist config\settings.ini (
    echo Creating settings.ini from example...
    copy config\settings_example.ini config\settings.ini
    echo Please update your OpenAI API key in config\settings.ini
) else (
    echo settings.ini already exists, skipping...
)

echo Installation complete!
pause
