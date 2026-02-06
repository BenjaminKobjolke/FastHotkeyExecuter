class SearchManager:
    def __init__(self, hotkey_loader, ui_manager, event_manager, window_manager, hotkey_executor, internal_command_manager, exit_callback, reload_callback=None):
        self.hotkey_loader = hotkey_loader
        self.ui_manager = ui_manager
        self.event_manager = event_manager
        self.window_manager = window_manager
        self.hotkey_executor = hotkey_executor
        self.internal_command_manager = internal_command_manager
        self.exit_callback = exit_callback
        self.reload_callback = reload_callback
        self.current_results = []
        self.is_command_mode = False

        # Bind search change event
        self.ui_manager.get_search_var().trace('w', self.on_search_change)

    def _show_no_hotkeys_dialog(self, message):
        """Show the 'no hotkeys found' dialog with OK, Reload, and Exit buttons."""
        self.window_manager.hide()

        def on_ok(dialog):
            dialog.destroy()

        def on_reload(dialog):
            dialog.destroy()
            if self.reload_callback:
                self.reload_callback()
            self.window_manager.window.after(100, self._retry_show)

        def on_exit(dialog):
            dialog.destroy()
            self.exit_callback()

        buttons = [
            ("OK", on_ok),
            ("Reload configurations and try again", on_reload),
            ("Exit Application", on_exit),
        ]
        dialog = self.ui_manager.create_dialog_with_buttons(message, buttons)
        self.ui_manager.show_dialog(dialog)

    def _retry_show(self):
        """Re-show the search window after reload."""
        if self.window_manager.show():
            current_app = self.window_manager.get_current_app()
            if current_app:
                self.current_results = self.hotkey_loader.get_hotkeys_for_app(current_app)
                if self.current_results:
                    self.ui_manager.clear_search()
                    self.ui_manager.update_results(self.current_results)
                    self.event_manager.reset_selection()
                    self.ui_manager.get_search_entry().focus()
                    return
            self._show_no_hotkeys_dialog(
                f'No hotkeys found for "{current_app}"' if current_app else "No hotkeys found for this application"
            )

    def on_search_change(self, *args):
        """Handle search input changes."""
        search_text = self.ui_manager.get_search_var().get()

        # Check if we're in command mode (starts with /)
        if search_text.startswith('/'):
            self.is_command_mode = True
            search_text = search_text[1:]  # Remove the / prefix
            self.current_results = self.internal_command_manager.search_commands(search_text)
            self.ui_manager.update_results(
                self.current_results,
                "No matching commands found" if search_text else "No commands available"
            )
            self.event_manager.reset_selection()
            return

        self.is_command_mode = False
        current_app = self.window_manager.get_current_app()
        if current_app:
            # Get search results
            if not search_text:
                # Show all hotkeys when search is empty
                self.current_results = self.hotkey_loader.get_hotkeys_for_app(current_app)
            else:
                self.current_results = self.hotkey_loader.search_hotkeys(current_app, search_text)
        else:
            print("[DEBUG] No application was detected when window was shown")
            self.current_results = []
            if search_text:  # Only show message if user has typed something
                self._show_no_hotkeys_dialog("No hotkeys found for this application")
                
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
            self._show_no_hotkeys_dialog(f'No hotkeys found for "{current_app}"')
            return False
            
        # Clear search and update UI
        self.ui_manager.clear_search()
        self.ui_manager.update_results(self.current_results)
        self.event_manager.reset_selection()
        return True

    def execute_selected_hotkey(self, index):
        """Execute the selected hotkey or command."""
        if 0 <= index < len(self.current_results):
            if self.is_command_mode:
                selected_command = self.current_results[index]
                print(f"[DEBUG] Executing command: {selected_command['name']}")
                self.window_manager.hide()
                result = self.internal_command_manager.execute_command(selected_command)
                if result == "exit":
                    self.exit_callback()
                elif result == "reload" and self.reload_callback:
                    self.reload_callback()
            else:
                selected_hotkey = self.current_results[index]
                if 'run' in selected_hotkey:
                    hotkey_desc = f"run: {selected_hotkey['run']}"
                elif 'hotkey' in selected_hotkey:
                    hotkey_desc = selected_hotkey['hotkey']
                else:
                    hotkey_desc = 'sequence'
                print(f"[DEBUG] Executing hotkey: {selected_hotkey['name']} ({hotkey_desc})")
                self.window_manager.hide()
                self.hotkey_executor.execute_hotkey(selected_hotkey)

    def get_current_results(self):
        """Get the current search results."""
        return self.current_results
