import keyboard
import mouse
import time
import win32gui
import win32con
from .key_aliases import KEY_ALIASES, VALID_KEYS

class HotkeyExecutor:
    def __init__(self):
        """Initialize the hotkey executor."""
        self.mouse_actions = {
            'wheelup': 1,     # Positive for scroll up
            'wheeldown': -1   # Negative for scroll down
        }
        self.abort_sequence = False
        self._setup_abort_listeners()
        
    def _setup_abort_listeners(self):
        """Setup keyboard listeners for sequence abort."""
        keyboard.on_press_key('esc', self._abort_sequence_callback)
        
    def _abort_sequence_callback(self, e):
        """Callback for abort key press."""
        self.abort_sequence = True
        print("[DEBUG] Sequence execution aborted")
        
    def _validate_keys(self, keys):
        """Validate that all keys in the combination are valid keyboard keys."""
        valid_keys = keyboard.all_modifiers.union(VALID_KEYS)
        
        for key in keys:
            key = key.lower()
            if key not in valid_keys:
                raise ValueError(f"Invalid key: {key}")
        return True

    def execute_hotkey(self, hotkey_data):
        """Execute a hotkey by simulating key presses."""
        try:
            if not isinstance(hotkey_data, dict):
                raise ValueError("Invalid hotkey data format")

            # Handle new format with array of actions
            if 'hotkeys' in hotkey_data and isinstance(hotkey_data['hotkeys'], list):
                print(f"[DEBUG] Executing hotkey sequence for: {hotkey_data['name']}")
                # Reset abort flag at start of sequence
                self.abort_sequence = False
                
                # Setup abort listener for the main hotkey if it exists
                main_hotkey = hotkey_data['hotkeys'][0].get('hotkey')
                if main_hotkey:
                    # Split the hotkey into individual keys
                    keys = main_hotkey.lower().split('+')
                    # Create a hotkey combination for abort
                    keyboard.add_hotkey('+'.join(keys), self._abort_sequence_callback)
                
                try:
                    for action in hotkey_data['hotkeys']:
                        if self.abort_sequence:
                            print("[DEBUG] Sequence aborted by user")
                            break
                            
                        if 'sleep' in action:
                            time.sleep(action['sleep'] / 1000)  # Convert milliseconds to seconds
                            continue
                        
                        if 'hotkey' not in action:
                            continue

                        # Execute single hotkey
                        self._execute_single_hotkey(action['hotkey'].lower())
                finally:
                    # Remove the main hotkey listener if it was set
                    if main_hotkey:
                        keyboard.remove_hotkey('+'.join(keys))
                    # Reset abort flag after sequence
                    self.abort_sequence = False
                return

            # Handle old format with single hotkey
            if 'hotkey' not in hotkey_data:
                raise ValueError("Invalid hotkey data format - missing hotkey")

            # Execute single hotkey
            hotkey = hotkey_data['hotkey'].lower()
            print(f"[DEBUG] Executing hotkey: {hotkey}")
            self._execute_single_hotkey(hotkey)

        except Exception as e:
            print(f"[DEBUG] Error executing hotkey: {e}")

    def _execute_single_hotkey(self, hotkey):
        """Execute a single hotkey combination."""
        try:
            
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
            
            # Map key aliases to standard forms, but preserve '?' key
            keys = [k if k == '?' else KEY_ALIASES.get(k, k) for k in keys]
            
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
                    # Handle '?' key specially
                    if keys[-1] == '?':
                        keyboard.press('shift')
                        keyboard.press('ß')
                        time.sleep(0.05)
                        keyboard.release('ß')
                        keyboard.release('shift')
                    # Handle ';' key specially for German keyboard layout
                    elif keys[-1] == ';':
                        keyboard.press('shift')
                        keyboard.press(',')  # Comma key
                        time.sleep(0.05)
                        keyboard.release(',')
                        keyboard.release('shift')
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
