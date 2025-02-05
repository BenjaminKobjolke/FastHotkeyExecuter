import os
import json
from pathlib import Path

class HotkeyLoader:
    def __init__(self, data_dir='data/hotkeys'):
        """Initialize the hotkey loader."""
        self.data_dir = data_dir
        self.hotkey_cache = {}  # Cache loaded hotkeys
        
    def get_hotkeys_for_app(self, app_name):
        """Get all hotkeys for a specific application."""
        try:
            # Return cached hotkeys if available
            if app_name in self.hotkey_cache:
                return self.hotkey_cache[app_name]
                
            # Construct app directory path
            app_dir = os.path.join(self.data_dir, app_name)
            
            # Check if directory exists
            if not os.path.exists(app_dir):
                print(f"[DEBUG] No hotkey directory found for {app_name}")
                self.hotkey_cache[app_name] = []  # Cache empty result
                return []
            
            # Load and combine all JSON files in the app directory
            all_hotkeys = []
            json_files = Path(app_dir).glob('*.json')
            
            for json_file in json_files:
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        hotkeys = json.load(f)
                        if isinstance(hotkeys, list):
                            all_hotkeys.extend(hotkeys)
                except json.JSONDecodeError as e:
                    print(f"[DEBUG] Error parsing hotkey file {json_file}: {e}")
                    continue
            
            print(f"[DEBUG] Loaded {len(all_hotkeys)} total hotkeys for {app_name}")
            self.hotkey_cache[app_name] = all_hotkeys  # Cache results
            return all_hotkeys
                
        except Exception as e:
            print(f"[DEBUG] Error loading hotkeys: {e}")
            return []
            
    def search_hotkeys(self, app_name, search_text):
        """Search hotkeys for an application by name."""
        try:
            # Get all hotkeys for the app
            hotkeys = self.get_hotkeys_for_app(app_name)
            if not hotkeys:
                return []
                
            # Convert search text to lowercase for case-insensitive search
            search_text = search_text.lower()
            
            # Split search text into words and filter hotkeys
            search_words = search_text.split()
            results = []
            for hotkey in hotkeys:
                hotkey_name = hotkey['name'].lower()
                # Check if all search words appear in the hotkey name
                if all(word.lower() in hotkey_name for word in search_words):
                    results.append(hotkey)
                    
            print(f"[DEBUG] Found {len(results)} matching hotkeys for search terms: {search_words}")
            return results
            
        except Exception as e:
            print(f"[DEBUG] Error searching hotkeys: {e}")
            return []
