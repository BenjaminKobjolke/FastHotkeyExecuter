import sys
import os
from data.config_manager import ConfigManager
from data.hotkey_loader import HotkeyLoader
from hotkeys.hotkey_executor import HotkeyExecutor
from hotkeys.hotkey_manager import HotkeyManager
from process.process_manager import ProcessManager
from gui.search_window import SearchWindow

def main():
    try:
        # Initialize components
        print("[DEBUG] Initializing components...")
        config_manager = ConfigManager()
        process_manager = ProcessManager()
        hotkey_loader = HotkeyLoader()
        hotkey_executor = HotkeyExecutor()
        
        # Create search window
        print("[DEBUG] Creating SearchWindow")
        search_window = SearchWindow(
            config_manager,
            process_manager,
            hotkey_loader,
            hotkey_executor
        )
        
        # Get toggle hotkey from config
        toggle_hotkey = config_manager.get_hotkey('toggle_search')
        if not toggle_hotkey:
            print("[ERROR] No toggle hotkey configured")
            sys.exit(1)
            
        # Initialize hotkey manager and register toggle hotkey
        print(f"[DEBUG] Registering toggle hotkey: {toggle_hotkey}")
        hotkey_manager = HotkeyManager()
        hotkey_manager.register_hotkey(toggle_hotkey, search_window.show)
        
        # Start main loop
        print("[DEBUG] Starting main loop")
        search_window.run()
        
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
        
if __name__ == '__main__':
    main()
