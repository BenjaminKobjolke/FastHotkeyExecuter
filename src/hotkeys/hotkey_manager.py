"""Module for managing global hotkeys with WinHotkeys library."""

from typing import Callable, Dict
try:
    from winhotkeys import HotkeyHandler
except ImportError:
    # Fallback to local import if needed
    from hotkey import HotkeyHandler


class HotkeyManager:
    """Class for managing global hotkeys with WinHotkeys library."""

    def __init__(self):
        """Initialize the hotkey manager."""
        self.registered_callbacks: Dict[str, Callable] = {}
        self.registered_handlers: Dict[str, HotkeyHandler] = {}

    def register_hotkey(self, hotkey: str, callback: Callable) -> None:
        """Register a hotkey with a callback function.

        Args:
            hotkey (str): The hotkey combination (e.g., 'ctrl+shift+p')
            callback (Callable): Function to call when hotkey is pressed
        """
        try:
            # Map special keys if needed
            mapped_hotkey = self._map_hotkey(hotkey)
            print(f"[DEBUG] Registering hotkey: {hotkey} (mapped to: {mapped_hotkey})")
            
            # Create a hotkey handler
            handler = HotkeyHandler(mapped_hotkey, callback, suppress=True)
            handler.start()
            
            # Store handler and callback for reference
            self.registered_handlers[hotkey] = handler
            self.registered_callbacks[hotkey] = callback
            
        except Exception as e:
            print(f"[DEBUG] Unexpected error registering hotkey {hotkey}: {e}")
            # Continue running even if registration fails

    def _map_hotkey(self, hotkey: str) -> str:
        """Map hotkey to format expected by WinHotkeys.
        
        Args:
            hotkey (str): The original hotkey string
            
        Returns:
            str: Mapped hotkey string
        """
        # Handle special case for '+' key
        if '++' in hotkey:
            # Handle ctrl++ case
            parts = hotkey.split('++')
            keys = [k.strip().lower() for k in parts[0].split('+')] + ['+']
            return '+'.join(keys)
        
        # Map special keys if needed
        keys = [k.strip().lower() for k in hotkey.split('+')]
        
        # Map command/control to ctrl and other special keys
        keys = [
            'ctrl' if k in ('command', 'control')
            else '+' if k == 'numpad+'
            else '-' if k == 'numpad-'
            else k for k in keys if k
        ]
        
        return '+'.join(keys)

    def __del__(self):
        """Cleanup by stopping all hotkey handlers."""
        try:
            for handler in self.registered_handlers.values():
                handler.stop()
        except Exception as e:
            print(f"[DEBUG] Error during cleanup: {e}")
