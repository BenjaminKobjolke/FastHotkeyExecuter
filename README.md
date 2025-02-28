# FastHotkeyExecuter

A Python application that provides quick access to application-specific hotkeys through a searchable interface.

## Features

- Global hotkey (Ctrl+Shift+P by default) to show/hide the search window
- Application-specific hotkey lists loaded from JSON files
- Search functionality to quickly find hotkeys
- Dark theme with customizable colors
- Keyboard navigation with arrow keys and Enter to execute hotkeys

## Installation

1. Make sure you have Python 3.7+ installed
2. Run `install.bat` to:
   - Create a virtual environment
   - Install required dependencies

## Usage

1. Run `run.bat` to start the application
2. Press Ctrl+Shift+P (default) to show the search window
3. Type to search for hotkeys
4. Use arrow keys to navigate results
5. Press Enter to execute the selected hotkey
6. Press Escape to hide the window

## Configuration

The application uses configuration files in the `config` directory:

- `settings.ini` contains application settings including API keys
- When you run `install.bat`, it will automatically create `settings.ini` from the example file if it doesn't exist
- You'll need to update the OpenAI API key in `settings.ini` to use the hotkey import feature

Settings you can modify in `config/settings.ini`:

```ini
[Hotkeys]
toggle_search = F1

[OpenAI]
api_key = your_openai_api_key_here

[chromium]
# Optional Chrome extensions to load
extension_1 = \tools\chrome_extensions\cookies.crx
extension_2 = \tools\chrome_extensions\ublock.crx
```

### Window Settings

Window appearance can be customized in `config/window_settings.ini`:

```ini
[Window]
width = 400
height = 40
background_color = #2E2E2E
text_color = #FFFFFF
font_size = 12
input_background_color = #2E2E2E
input_text_color = #FFFFFF
input_select_background = #404040
input_select_foreground = #FFFFFF
```

## Adding Hotkeys

### Manual Method

Create JSON files in the `data/hotkeys` directory named after the application process (e.g., `evernote.json`):

```json
[
  {
    "name": "New Note",
    "hotkey": "ctrl+n"
  },
  {
    "name": "Search Notes",
    "hotkey": "ctrl+q"
  }
]
```

### Importing Hotkeys

The application includes a feature to import hotkeys from websites using OpenAI:

1. Ensure you have an OpenAI API key set in `config/settings.ini`
2. Run `import.bat` or use the command line:
   ```
   python src/import_hotkeys.py --name "app_name" --url "https://website-with-hotkeys.com"
   ```
3. The imported hotkeys will be saved to `data/hotkeys/app_name/app_name.json`

#### Requirements for Web Import

For the web import feature to work properly:

- You need to have Google Chrome installed on your system
- Your Chrome version needs to be compatible with the version of Selenium you're using
- You need internet access during the first run (so Selenium can download the appropriate driver if needed)

If you encounter issues with the automatic Chrome driver detection, you can manually specify the path to your ChromeDriver in `settings.ini`:

```ini
[chromium]
driver_path = C:\path\to\chromedriver.exe
```

## Requirements

- Windows 10/11
- Python 3.7+
- Required packages (installed automatically):
  - keyboard
  - psutil
  - pywin32

## License

MIT License
