import os
import json

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
                
            # Construct json file path
            json_path = os.path.join(self.data_dir, f"{app_name}.json")
            
            # Check if file exists
            if not os.path.exists(json_path):
                print(f"[DEBUG] No hotkey file found for {app_name}")
                self.hotkey_cache[app_name] = []  # Cache empty result
                return []
                
            # Load and parse json file
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    hotkeys = json.load(f)
                print(f"[DEBUG] Loaded {len(hotkeys)} hotkeys for {app_name}")
                self.hotkey_cache[app_name] = hotkeys  # Cache results
                return hotkeys
            except json.JSONDecodeError as e:
                print(f"[DEBUG] Error parsing hotkey file for {app_name}: {e}")
                self.hotkey_cache[app_name] = []  # Cache empty result
                return []
                
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
            
            # Filter hotkeys by search text
            results = []
            for hotkey in hotkeys:
                if search_text in hotkey['name'].lower():
                    results.append(hotkey)
                    
            print(f"[DEBUG] Found {len(results)} matching hotkeys")
            return results
            
        except Exception as e:
            print(f"[DEBUG] Error searching hotkeys: {e}")
            return []
