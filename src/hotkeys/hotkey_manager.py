"""Module for managing global hotkeys with direct key binding."""

import keyboard
from typing import Callable, Dict, Set


class HotkeyManager:
    """Class for managing global hotkeys with direct key binding."""

    def __init__(self):
        """Initialize the hotkey manager."""
        self.registered_callbacks: Dict[str, Callable] = {}
        self.registered_handlers: Dict[str, Callable] = {}

    def register_hotkey(self, hotkey: str, callback: Callable) -> None:
        """Register a hotkey with a callback function.

        Args:
            hotkey (str): The hotkey combination (e.g., 'ctrl+shift+p')
            callback (Callable): Function to call when hotkey is pressed
        """
        try:
            # Split and handle special case for '+' key
            if '++' in hotkey:
                # Handle ctrl++ case
                parts = hotkey.split('++')
                keys = [k.strip().lower() for k in parts[0].split('+')] + ['+']
            else:
                # Normal case
                keys = [k.strip().lower() for k in hotkey.split('+')]
            
            # Filter out empty strings
            keys = [k for k in keys if k]
            print(f"[DEBUG] Registering hotkey: {hotkey}")
            
            # For single key (like F1)
            if len(keys) == 1:
                try:
                    print(f"[DEBUG] Binding single key: {keys[0]}")
                    handler = lambda e: self._handle_callback(callback)
                    keyboard.on_press_key(keys[0], handler, suppress=True)
                    self.registered_handlers[hotkey] = handler
                except ValueError as e:
                    print(f"[DEBUG] Error binding key {keys[0]}: {e}")
                    return  # Skip this hotkey but continue running
            # For combinations (like ctrl+shift+p)
            else:
                try:
                    main_key = keys[-1]
                    modifiers = set(keys[:-1])
                    print(f"[DEBUG] Binding key {main_key} with modifiers: {modifiers}")
                    handler = self._create_hotkey_handler(modifiers, callback)
                    keyboard.on_press_key(main_key, handler, suppress=True)
                    self.registered_handlers[hotkey] = handler
                except ValueError as e:
                    print(f"[DEBUG] Error binding combination {hotkey}: {e}")
                    return  # Skip this hotkey but continue running
                
            # Store callback for reference
            self.registered_callbacks[hotkey] = callback
            
        except Exception as e:
            print(f"[DEBUG] Unexpected error registering hotkey {hotkey}: {e}")
            # Continue running even if registration fails

    def _create_hotkey_handler(self, modifiers: Set[str], callback: Callable) -> Callable:
        """Create a handler function for a hotkey combination.

        Args:
            modifiers (Set[str]): Set of modifier keys required
            callback (Callable): Function to call when hotkey is pressed

        Returns:
            Callable: Handler function for the hotkey
        """
        def handler(event):
            try:
                # Get currently pressed modifier keys
                pressed = {k.lower() for k in keyboard._pressed_events}
                # Remove the main key from pressed set
                pressed.discard(event.name.lower())
                # Check if our modifiers match exactly
                if pressed == modifiers:
                    return self._handle_callback(callback)
            except Exception as e:
                print(f"[DEBUG] Error in hotkey handler: {e}")
                # Don't let the error affect the hotkey registration
                return False
            return True
        return handler

    def _handle_callback(self, callback: Callable) -> bool:
        """Handle callback execution and return False to suppress the key.

        Args:
            callback (Callable): The callback to execute

        Returns:
            bool: False to suppress the key event
        """
        try:
            callback()
        except Exception as e:
            print(f"[DEBUG] Error in hotkey callback: {e}")
            # Log the error but don't let it affect the hotkey registration
        return False  # Always suppress the key event to maintain hotkey functionality

    def __del__(self):
        """Cleanup by unhooking all keyboard events."""
        try:
            keyboard.unhook_all()
        except Exception as e:
            print(f"[DEBUG] Error during cleanup: {e}")
