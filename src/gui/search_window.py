import tkinter as tk
from .window_manager import WindowManager
from .theme_manager import ThemeManager
from .event_manager import EventManager
from .ui_manager import UIManager
from .search_manager import SearchManager

class SearchWindow:
    def __init__(self, config_manager, process_manager, hotkey_loader, hotkey_executor):
        # Configure global theme settings before creating root window
        root = tk.Tk()
        root.withdraw()
        
        # Initialize managers
        self.window_manager = WindowManager(root, config_manager, process_manager)
        self.theme_manager = ThemeManager(root, config_manager)
        self.ui_manager = UIManager(root, self.theme_manager)
        
        # Set search entry in window manager for focus management
        self.window_manager.set_search_entry(self.ui_manager.get_search_entry())
        
        # Initialize event manager with callbacks
        self.event_manager = EventManager(
            self.ui_manager.get_search_entry(),
            self.ui_manager.get_results_listbox(),
            None,  # Search change is handled by SearchManager
            self._on_hotkey_selected,
            self.hide
        )
        
        # Initialize search manager
        self.search_manager = SearchManager(
            hotkey_loader,
            self.ui_manager,
            self.event_manager,
            self.window_manager,
            hotkey_executor
        )
        
        # Bind focus loss to window manager
        root.bind('<FocusOut>', lambda e: self.window_manager.handle_focus_loss())

    def show(self):
        """Show the search window."""
        if self.window_manager.show():
            if self.search_manager.show_initial_results():
                self.ui_manager.get_search_entry().focus()

    def hide(self, event=None):
        """Hide the search window."""
        self.window_manager.hide()

    def _on_hotkey_selected(self, index):
        """Handle hotkey selection."""
        self.search_manager.execute_selected_hotkey(index)

    def run(self):
        """Start the window's main loop."""
        self.window_manager.window.mainloop()
