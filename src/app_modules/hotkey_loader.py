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
            
            # Load and combine all JSON files in the app directory, ignoring duplicates
            all_hotkeys = []
            seen_hotkeys = set()  # Track seen hotkey combinations
            json_files = Path(app_dir).glob('*.json')
            
            for json_file in json_files:
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Handle both old format (array) and new format (object with metadata)
                        if isinstance(data, dict) and 'hotkeys' in data:
                            hotkeys = data['hotkeys']
                            # Get prefix from metadata if it exists
                            prefix = data.get('metadata', {}).get('prefix', '')
                        else:
                            hotkeys = data
                            prefix = ''
                        
                        if isinstance(hotkeys, list):
                            for hotkey in hotkeys:
                                # Handle new format with array of actions
                                if 'hotkeys' in hotkey:
                                    if prefix:
                                        hotkey['name'] = f"{prefix} {hotkey['name']}"
                                    all_hotkeys.append(hotkey)
                                # Handle old format with single hotkey
                                elif 'hotkey' in hotkey and hotkey['hotkey'] not in seen_hotkeys:
                                    seen_hotkeys.add(hotkey['hotkey'])
                                    if prefix:
                                        hotkey['name'] = f"{prefix} {hotkey['name']}"
                                    all_hotkeys.append(hotkey)
                        else:
                            print(f"[DEBUG] Invalid hotkey format in {json_file}")
                except json.JSONDecodeError as e:
                    print(f"[DEBUG] Error parsing hotkey file {json_file}: {e}")
                    continue
            
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
