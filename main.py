import sys
import os
import argparse
from src.app_modules.config_manager import ConfigManager
import src.import_hotkeys
from src.app_modules.hotkey_loader import HotkeyLoader
from src.hotkeys.hotkey_executor import HotkeyExecutor
from src.hotkeys.hotkey_manager import HotkeyManager
from src.process.process_manager import ProcessManager
from src.gui.search_window import SearchWindow

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='FastHotkeyExecuter')
    parser.add_argument('--name', help='Name of the application for importing hotkeys')
    parser.add_argument('--url', help='URL of the webpage containing hotkeys')
    return parser.parse_args()

def prompt_for_missing_args(args):
    """Prompt for missing arguments."""
    if not args.name:
        args.name = input("Please enter the application name: ")
    if not args.url:
        args.url = input("Please enter the URL containing hotkeys: ")
    return args

def main():
    try:
        # Parse arguments
        args = parse_arguments()
        
        # If either name or url is provided, assume we're in import mode
        if args.name or args.url:
            args = prompt_for_missing_args(args)
            sys.argv = [sys.argv[0], '--name', args.name, '--url', args.url]
            import_hotkeys.main()
            return

        # Initialize components for normal operation
        config_manager = ConfigManager()
        process_manager = ProcessManager()
        hotkey_loader = HotkeyLoader()
        hotkey_executor = HotkeyExecutor()
        
        # Create search window
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
        hotkey_manager = HotkeyManager()
        hotkey_manager.register_hotkey(toggle_hotkey, search_window.show)
        
        # Start main loop
        search_window.run()
        
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
        
if __name__ == '__main__':
    main()
