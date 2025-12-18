import configparser
import os
import sys # Added import for sys

class ConfigManager:
    def __init__(self, config_file='config/settings.ini', window_config_file='config/window_settings.ini'):
        """Initialize the config manager."""
        # Determine the base path for accessing bundled files
        if getattr(sys, 'frozen', False):
            # Running in a PyInstaller bundle
            base_path = sys._MEIPASS
        else:
            # Running in a normal Python environment
            # Go up two levels from src/app_modules to project root
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        self.config_file = os.path.join(base_path, config_file)
        self.window_config_file = os.path.join(base_path, window_config_file)
        self.config = configparser.ConfigParser()
        self.window_config = configparser.ConfigParser()
        self.load_config()
        
    def load_config(self):
        """Load configuration from files."""
        try:
            # Check if config files exist
            if not os.path.exists(self.config_file) or not os.path.exists(self.window_config_file):
                print("[DEBUG] Config files not found, creating defaults")
                self.create_default_config()
                return
                
            # Load config files
            self.config.read(self.config_file)
            self.window_config.read(self.window_config_file)
            """
            print("[DEBUG] Configuration loaded successfully")
            print("[DEBUG] Current configuration:")
            for section in self.config.sections():
                print(f"[DEBUG] [{section}]")
                for key, value in self.config[section].items():
                    print(f"[DEBUG]   {key} = {value}")
            print("[DEBUG] Current window configuration:")
            for section in self.window_config.sections():
                print(f"[DEBUG] [{section}]")
                for key, value in self.window_config[section].items():
                    print(f"[DEBUG]   {key} = {value}")
            """
                    
        except Exception as e:
            print(f"[DEBUG] Error loading config: {e}")
            print("[DEBUG] Creating default configuration")
            self.create_default_config()
            
    def create_default_config(self):
        """Create default configuration files."""
        try:
            # Create config directory if it doesn't exist
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            # Set default values for main config
            self.config['Hotkeys'] = {
                'toggle_search': 'ctrl+shift+p'
            }
            
            # Set default values for window config
            self.window_config['Window'] = {
                'width': '400',
                'height': '40',
                'background_color': '#2E2E2E',
                'text_color': '#FFFFFF',
                'font_size': '12',
                'input_background_color': '#2E2E2E',
                'input_text_color': '#FFFFFF',
                'input_select_background': '#404040',
                'input_select_foreground': '#FFFFFF'
            }
            
            # Save to files
            with open(self.config_file, 'w') as f:
                self.config.write(f)
                
            with open(self.window_config_file, 'w') as f:
                self.window_config.write(f)
                
            print("[DEBUG] Default configurations created")
            
        except Exception as e:
            print(f"[DEBUG] Error creating default config: {e}")
            
    def get_hotkey(self, name):
        """Get a hotkey configuration value."""
        try:
            return self.config['Hotkeys'].get(name)
        except:
            return None
            
    def get_window_settings(self):
        """Get all window-related settings."""
        try:
            settings = dict(self.window_config['Window'])
            # Convert numeric values
            settings['width'] = int(settings['width'])
            settings['height'] = int(settings['height'])
            settings['font_size'] = int(settings['font_size'])
            return settings
        except Exception as e:
            print(f"[DEBUG] Error getting window settings: {e}")
            return {
                'width': 400,
                'height': 40,
                'background_color': '#2E2E2E',
                'text_color': '#FFFFFF',
                'font_size': 12,
                'input_background_color': '#2E2E2E',
                'input_text_color': '#FFFFFF',
                'input_select_background': '#404040',
                'input_select_foreground': '#FFFFFF'
            }
