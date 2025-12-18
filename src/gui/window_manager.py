import tkinter as tk
import time

class WindowManager:
    def __init__(self, root, config_manager, process_manager):
        self.window = root
        self.config_manager = config_manager
        self.process_manager = process_manager
        self.current_app = None
        self._configure_window()
        self.search_entry = None  # Will be set by set_search_entry
        self._showing = False  # Flag to prevent focus loss during show

    def _configure_window(self):
        """Configure the window appearance and behavior."""
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Prevent window movement
        self.window.bind('<B1-Motion>', lambda e: 'break')
        self.window.bind('<Button-1>', lambda e: 'break')
        self.window.bind('<Alt-Tab>', lambda e: 'break')
        self.window.bind('<Alt-F4>', lambda e: 'break')

        # Set window size
        settings = self.config_manager.get_window_settings()
        self.window.geometry(f"{settings['width']}x{settings['height']}")

    def set_search_entry(self, entry):
        """Set the search entry widget for focus management."""
        self.search_entry = entry

    def show(self):
        """Show the search window centered on the active window."""
        try:
            self.current_app = self.process_manager.get_active_window_process()
            if not self.current_app:
                return False

            # Get active window position
            active_pos = self.process_manager.get_active_window_position()
            if not active_pos:
                return False

            # Calculate center position
            settings = self.config_manager.get_window_settings()
            window_width = settings['width']
            window_height = settings['height']

            x = active_pos['x'] + (active_pos['width'] - window_width) // 2
            y = active_pos['y'] + (active_pos['height'] - window_height) // 2

            self.window.geometry(f"+{x}+{y}")

            # Set flag to prevent focus loss during show
            self._showing = True

            self.window.deiconify()
            self.window.lift()
            self.window.focus_force()
            if self.search_entry:
                self.search_entry.focus_set()

            # Clear the showing flag after a short delay
            self.window.after(100, self._clear_showing_flag)

            return True

        except Exception as e:
            self.window.withdraw()
            return False

    def hide(self):
        """Hide the search window."""
        self.window.withdraw()
        self.window.update()
        time.sleep(0.1)
        self.current_app = None

    def _clear_showing_flag(self):
        """Clear the showing flag after window is fully shown."""
        self._showing = False

    def handle_focus_loss(self):
        """Handle window focus loss by hiding the window."""
        if self._showing:
            return 'break'
        self.hide()
        return 'break'

    def get_current_app(self):
        """Get the current application name."""
        return self.current_app

    def update_size(self, height):
        """Update window height while maintaining width."""
        settings = self.config_manager.get_window_settings()
        # Only update if the new height is larger than the configured base height
        if height > settings['height']:
            self.window.geometry(f"{settings['width']}x{height}")
        else:
            self.window.geometry(f"{settings['width']}x{settings['height']}")
