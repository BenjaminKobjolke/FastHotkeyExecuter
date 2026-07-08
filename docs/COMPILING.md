# Compiling to a standalone EXE

How this app builds a single-file Windows executable, with a configurable
output path and a graceful shutdown mechanism so the running exe can be
overwritten. This pattern is reusable across other PyInstaller apps — the
only app-specific values are the exe name, the entry script, and the
`--add-data` folders.

## Files

| File | Tracked? | Purpose |
|------|----------|---------|
| `compile_exe.bat` | yes | The build script. |
| `compile_settings.bat` | **no** (gitignored) | Per-machine output path. |
| `compile_settings.bat.example` | yes | Template to copy. |
| `activate_environment.bat` | yes | Activates the local `venv`. |

## Setup (per machine)

1. Copy `compile_settings.bat.example` → `compile_settings.bat`.
2. Edit `OUTPUT_PATH` to where the exe should land, e.g.:
   ```bat
   @echo off
   set OUTPUT_PATH=E:\[--Sync--]\BKTools\Apps\FastHotkeyExecuter
   ```
3. If `compile_settings.bat` is absent, the build falls back to PyInstaller's
   default `dist/` folder.

`compile_settings.bat` is in `.gitignore` so each machine keeps its own path
without touching version control.

## Building

Run `compile_exe.bat`. It:

1. Activates the venv (`activate_environment.bat`).
2. Loads `compile_settings.bat` if present (sets `OUTPUT_PATH`).
3. Writes a `.shutdown` sentinel to the output folder and waits (bounded, ~20s)
   for any running instance to exit gracefully — so the exe isn't file-locked.
4. Deletes the sentinel and runs PyInstaller, using `--distpath "%OUTPUT_PATH%"`
   when set so the exe is written directly to the target (no copy step).

## Graceful shutdown (`.shutdown` sentinel)

PyInstaller cannot overwrite an exe that is currently running. Instead of
force-killing (`taskkill /F`), the app watches for a `.shutdown` file next to
itself and exits cleanly when it appears.

**App side** (`src/gui/search_window.py`): a self-rescheduling tkinter
`after()` poller checks every 500ms, deletes the sentinel when found, and
calls the existing `exit_application()`.

```python
# path to the sentinel — next to the exe, NOT the PyInstaller temp dir
if getattr(sys, 'frozen', False):
    base = os.path.dirname(sys.executable)   # folder the exe runs from
else:
    base = <project root>                    # dev mode
self._shutdown_file = os.path.join(base, '.shutdown')

def _check_shutdown(self):
    if os.path.exists(self._shutdown_file):
        try:
            os.remove(self._shutdown_file)
        except OSError:
            pass
        self.exit_application()
        return
    self.window_manager.window.after(500, self._check_shutdown)
```

Kick it off before `mainloop()`:
```python
def run(self):
    self.window_manager.window.after(500, self._check_shutdown)
    self.window_manager.window.mainloop()
```

The app deletes the sentinel as it consumes it, so a leftover file can never
kill the next launch.

**Build side** (`compile_exe.bat`): write the sentinel where the running exe
watches (= `OUTPUT_PATH`), poll `tasklist` until the process is gone, then
build. Bounded so it never hangs.

```bat
if defined OUTPUT_PATH (set "TARGET=%OUTPUT_PATH%") else (set "TARGET=%~dp0")
set "SENTINEL=%TARGET%\.shutdown"
echo shutdown > "%SENTINEL%"

set /a TRIES=0
:waitloop
tasklist /FI "IMAGENAME eq FastHotkeyExecuter.exe" 2>nul | find /I "FastHotkeyExecuter.exe" >nul
if %errorlevel%==0 (
    if %TRIES% GEQ 20 ( echo Timed out; goto build )
    set /a TRIES+=1
    timeout /t 1 /nobreak >nul
    goto waitloop
)
:build
del "%SENTINEL%" >nul 2>&1
```

### Behavior in each case
- **Exe running (new build):** exits within ~1s, build proceeds unlocked.
- **Exe not running:** `tasklist` finds nothing → wait loop skipped → sentinel
  deleted → build immediately. No delay.
- **Exe running but too old to know about `.shutdown`:** wait times out (~20s),
  build proceeds; the locked exe may fail the build. Kill it manually once —
  every build after supports graceful shutdown.

## Reusing in another app

1. Copy `compile_exe.bat`, `compile_settings.bat.example`, and the
   `activate_environment.bat` pattern.
2. Add `compile_settings.bat` to that repo's `.gitignore`.
3. In `compile_exe.bat`, change the exe name (`--name`), the entry script
   (`main.py`), the `--add-data` folders, and the `IMAGENAME` in the tasklist
   check.
4. Port the `.shutdown` poller into that app's event loop:
   - tkinter → `root.after(...)` (as above)
   - PyQt → `QTimer`
   - plain loop → check the file each iteration
   Anchor the sentinel path to `os.path.dirname(sys.executable)` when frozen.
