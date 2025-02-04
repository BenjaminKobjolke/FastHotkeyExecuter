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

Settings can be modified in `config/settings.ini`:

```ini
[Hotkeys]
toggle_search = ctrl+shift+p

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

Create JSON files in the `data` directory named after the application process (e.g., `evernote.json`):

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

## Requirements

- Windows 10/11
- Python 3.7+
- Required packages (installed automatically):
  - keyboard
  - psutil
  - pywin32

## License

MIT License
