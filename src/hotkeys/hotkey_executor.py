import keyboard
import mouse
import time

class HotkeyExecutor:
    def __init__(self):
        """Initialize the hotkey executor."""
        self.mouse_actions = {
            'wheelup': 1,     # Positive for scroll up
            'wheeldown': -1   # Negative for scroll down
        }
        
    def execute_hotkey(self, hotkey_data):
        """Execute a hotkey by simulating key presses."""
        try:
            # Get the hotkey combination
            hotkey = hotkey_data['hotkey'].lower()
            print(f"[DEBUG] Executing hotkey: {hotkey}")
            
            # Split into individual keys
            keys = hotkey.split('+')
            keys = [key.strip() for key in keys]
            
            # Check if last key is a mouse wheel action
            last_key = keys[-1]
            if last_key in self.mouse_actions:
                # Press all modifier keys
                modifiers = []
                for key in keys[:-1]:  # All except last key
                    keyboard.press(key)
                    modifiers.append(key)
                    time.sleep(0.05)  # Small delay between key presses

                # Simulate mouse wheel
                mouse.wheel(self.mouse_actions[last_key])
                time.sleep(0.05)

                # Release modifiers in reverse order
                for key in reversed(modifiers):
                    keyboard.release(key)
                    time.sleep(0.05)
            else:
                # Handle regular keyboard shortcuts
                modifiers = []
                for key in keys[:-1]:  # All except last key
                    keyboard.press(key)
                    modifiers.append(key)
                    time.sleep(0.05)  # Small delay between key presses
                
                # Press and release the final key
                keyboard.press(keys[-1])
                time.sleep(0.05)
                keyboard.release(keys[-1])
                
                # Release modifiers in reverse order
                for key in reversed(modifiers):
                    keyboard.release(key)
                    time.sleep(0.05)
                
            print("[DEBUG] Hotkey executed successfully")
            
        except Exception as e:
            print(f"[DEBUG] Error executing hotkey: {e}")
