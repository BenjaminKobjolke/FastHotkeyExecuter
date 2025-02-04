import keyboard
import mouse
import time
import win32gui
import win32con

class HotkeyExecutor:
    def __init__(self):
        """Initialize the hotkey executor."""
        self.mouse_actions = {
            'wheelup': 1,     # Positive for scroll up
            'wheeldown': -1   # Negative for scroll down
        }
        
    def _validate_keys(self, keys):
        """Validate that all keys in the combination are valid keyboard keys."""
        # Create set of valid keys
        valid_keys = keyboard.all_modifiers.union({
            'esc', 'enter', 'tab', 'space', 'backspace', 'delete',
            'up', 'down', 'left', 'right', 'home', 'end', 'pageup', 'pagedown',
            'insert', '+', '-', '*', '/', '=', 'win'
        })
        
        # Add letters
        valid_keys.update(chr(i) for i in range(ord('a'), ord('z') + 1))
        
        # Add numbers
        valid_keys.update(str(i) for i in range(10))
        
        # Add function keys
        valid_keys.update(f'f{i}' for i in range(1, 13))

        for key in keys:
            key = key.lower()
            if key not in valid_keys:
                raise ValueError(f"Invalid key: {key}")
        return True

    def execute_hotkey(self, hotkey_data):
        """Execute a hotkey by simulating key presses."""
        try:
            if not isinstance(hotkey_data, dict) or 'hotkey' not in hotkey_data:
                raise ValueError("Invalid hotkey data format")

            # Get the hotkey combination
            hotkey = hotkey_data['hotkey'].lower()
            print(f"[DEBUG] Executing hotkey: {hotkey}")
            
            # Split and handle special case for '+' key
            if '++' in hotkey:
                # Handle ctrl++ case
                parts = hotkey.split('++')
                keys = parts[0].split('+') + ['+']  # Add '+' as the final key
            else:
                # Normal case
                keys = hotkey.split('+')
            
            # Clean up keys and filter out empty strings
            keys = [key.strip() for key in keys if key.strip()]
            
            # Validate keys before execution
            try:
                self._validate_keys(keys)
            except ValueError as e:
                print(f"[DEBUG] Invalid hotkey combination: {e}")
                return
            
            # Get the foreground window
            foreground_window = win32gui.GetForegroundWindow()
            
            # Check if last key is a mouse wheel action
            last_key = keys[-1]
            if last_key in self.mouse_actions:
                # Press all modifier keys
                modifiers = []
                for key in keys[:-1]:  # All except last key
                    # Handle Windows key specifically
                    if key == 'win':
                        keyboard.press('windows')  # Use 'windows' instead of 'win'
                    else:
                        keyboard.press(key)
                    modifiers.append(key)
                    time.sleep(0.05)  # Small delay between key presses

                # Simulate mouse wheel
                mouse.wheel(self.mouse_actions[last_key])
                time.sleep(0.05)

                # Release modifiers in reverse order
                for key in reversed(modifiers):
                    # Handle Windows key specifically
                    if key == 'win':
                        keyboard.release('windows')  # Use 'windows' instead of 'win'
                    else:
                        keyboard.release(key)
                    time.sleep(0.05)
            else:
                # Handle regular keyboard shortcuts
                modifiers = []
                for key in keys[:-1]:  # All except last key
                    # Handle Windows key specifically
                    if key == 'win':
                        keyboard.press('windows')  # Use 'windows' instead of 'win'
                    else:
                        keyboard.press(key)
                    modifiers.append(key)
                    time.sleep(0.05)  # Small delay between key presses
                
                # Press and release the final key
                if keys[-1] == 'win':
                    keyboard.press('windows')
                    time.sleep(0.05)
                    keyboard.release('windows')
                else:
                    keyboard.press(keys[-1])
                    time.sleep(0.05)
                    keyboard.release(keys[-1])
                
                # Release modifiers in reverse order
                for key in reversed(modifiers):
                    # Handle Windows key specifically
                    if key == 'win':
                        keyboard.release('windows')  # Use 'windows' instead of 'win'
                    else:
                        keyboard.release(key)
                    time.sleep(0.05)
            
            # Restore our window as foreground
            win32gui.SetForegroundWindow(foreground_window)
                
            print("[DEBUG] Hotkey executed successfully")
            
        except Exception as e:
            print(f"[DEBUG] Error executing hotkey: {e}")
