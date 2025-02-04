class SearchManager:
    def __init__(self, hotkey_loader, ui_manager, event_manager, window_manager, hotkey_executor):
        self.hotkey_loader = hotkey_loader
        self.ui_manager = ui_manager
        self.event_manager = event_manager
        self.window_manager = window_manager
        self.hotkey_executor = hotkey_executor
        self.current_results = []
        
        # Bind search change event
        self.ui_manager.get_search_var().trace('w', self.on_search_change)

    def on_search_change(self, *args):
        """Handle search input changes."""
        search_text = self.ui_manager.get_search_var().get()
        print(f"[DEBUG] Search triggered - Text: '{search_text}'")
        
        current_app = self.window_manager.get_current_app()
        if current_app:
            print(f"[DEBUG] Searching hotkeys for application: {current_app}")
            # Get search results
            if not search_text:
                # Show all hotkeys when search is empty
                self.current_results = self.hotkey_loader.get_hotkeys_for_app(current_app)
            else:
                self.current_results = self.hotkey_loader.search_hotkeys(current_app, search_text)
            print(f"[DEBUG] Found {len(self.current_results)} total hotkeys for {current_app}")
        else:
            print("[DEBUG] No application was detected when window was shown")
            self.current_results = []
            if search_text:  # Only show message if user has typed something
                dialog = self.ui_manager.create_dialog(
                    "No hotkeys found for this application"
                )
                self.ui_manager.show_dialog(dialog)
                
        # Update UI with results
        self.ui_manager.update_results(
            self.current_results,
            "No matching hotkeys found" if search_text else "No hotkeys available"
        )
        
        # Reset selection
        self.event_manager.reset_selection()

    def show_initial_results(self):
        """Show initial results when window is displayed."""
        current_app = self.window_manager.get_current_app()
        if not current_app:
            return False
            
        # Get all hotkeys for the current app
        self.current_results = self.hotkey_loader.get_hotkeys_for_app(current_app)
        
        if not self.current_results:
            dialog = self.ui_manager.create_dialog(
                f'No hotkeys found for "{current_app}"'
            )
            self.ui_manager.show_dialog(dialog)
            return False
            
        # Clear search and update UI
        self.ui_manager.clear_search()
        self.ui_manager.update_results(self.current_results)
        self.event_manager.reset_selection()
        return True

    def execute_selected_hotkey(self, index):
        """Execute the selected hotkey."""
        if 0 <= index < len(self.current_results):
            selected_hotkey = self.current_results[index]
            print(f"[DEBUG] Executing hotkey: {selected_hotkey['name']} ({selected_hotkey['hotkey']})")
            self.window_manager.hide()
            self.hotkey_executor.execute_hotkey(selected_hotkey)

    def get_current_results(self):
        """Get the current search results."""
        return self.current_results
