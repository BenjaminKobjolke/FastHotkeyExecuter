import tkinter as tk

class EventManager:
    def __init__(self, search_entry, results_listbox, on_search_change, on_hotkey_selected, on_hide):
        self.search_entry = search_entry
        self.results_listbox = results_listbox
        self.on_search_change = on_search_change
        self.on_hotkey_selected = on_hotkey_selected
        self.on_hide = on_hide
        self.selected_index = 0
        self._bind_events()

    def _bind_events(self):
        """Bind all keyboard and mouse events."""
        # Search entry events
        self.search_entry.bind('<Return>', self._handle_enter)
        self.search_entry.bind('<Escape>', self._handle_escape)
        self.search_entry.bind('<Up>', self._handle_up)
        self.search_entry.bind('<Down>', self._handle_down)
        self.search_entry.bind('<Control-Up>', self._handle_ctrl_up)
        self.search_entry.bind('<Control-Down>', self._handle_ctrl_down)
        self.search_entry.bind('<Prior>', self._handle_page_up)
        self.search_entry.bind('<Next>', self._handle_page_down)
        self.search_entry.bind('<Control-Prior>', self._handle_ctrl_page_up)
        self.search_entry.bind('<Control-Next>', self._handle_ctrl_page_down)
        self.search_entry.bind('<Control-Home>', self._handle_home)
        self.search_entry.bind('<Control-End>', self._handle_end)

        # Prevent unwanted behavior
        self.search_entry.bind('<Control-Return>', lambda e: 'break')
        self.search_entry.bind('<Shift-Return>', lambda e: 'break')
        self.search_entry.bind('<Alt-Return>', lambda e: 'break')
        self.search_entry.bind('<Tab>', lambda e: 'break')
        self.search_entry.bind('<Control-Tab>', lambda e: 'break')
        
        # Select all text shortcut
        self.search_entry.bind('<Control-a>', 
            lambda e: self.search_entry.select_range(0, tk.END))

        # Listbox events
        self.results_listbox.bind('<Button-1>', self._handle_listbox_click)
        self.results_listbox.bind('<Double-Button-1>', self._handle_listbox_double_click)
        self.results_listbox.bind('<B1-Motion>', lambda e: 'break')
        self.results_listbox.bind('<MouseWheel>', self._handle_mouse_wheel)
        self.results_listbox.bind('<Button-4>', self._handle_mouse_wheel)
        self.results_listbox.bind('<Button-5>', self._handle_mouse_wheel)

    def _handle_enter(self, event):
        """Execute selected hotkey."""
        self.on_hotkey_selected(self.selected_index)
        return 'break'

    def _handle_escape(self, event):
        """Hide the window."""
        self.on_hide()
        return 'break'

    def _handle_up(self, event):
        """Navigate up in results."""
        if self.results_listbox.size() > 0:
            self.selected_index = max(0, self.selected_index - 1)
            self._update_selection()
        return 'break'

    def _handle_down(self, event):
        """Navigate down in results."""
        if self.results_listbox.size() > 0:
            self.selected_index = min(self.results_listbox.size() - 1, 
                                    self.selected_index + 1)
            self._update_selection()
        return 'break'

    def _handle_page_up(self, event):
        """Move up by page."""
        if self.results_listbox.size() > 0:
            self.selected_index = max(0, self.selected_index - 5)
            self._update_selection()
        return 'break'

    def _handle_page_down(self, event):
        """Move down by page."""
        if self.results_listbox.size() > 0:
            self.selected_index = min(self.results_listbox.size() - 1, 
                                    self.selected_index + 5)
            self._update_selection()
        return 'break'

    def _handle_ctrl_up(self, event):
        """Quick navigation up."""
        cursor_pos = self.search_entry.index(tk.INSERT)
        self._handle_up(event)
        self.search_entry.icursor(cursor_pos)
        return 'break'

    def _handle_ctrl_down(self, event):
        """Quick navigation down."""
        cursor_pos = self.search_entry.index(tk.INSERT)
        self._handle_down(event)
        self.search_entry.icursor(cursor_pos)
        return 'break'

    def _handle_ctrl_page_up(self, event):
        """Quick page up."""
        cursor_pos = self.search_entry.index(tk.INSERT)
        self._handle_page_up(event)
        self.search_entry.icursor(cursor_pos)
        return 'break'

    def _handle_ctrl_page_down(self, event):
        """Quick page down."""
        cursor_pos = self.search_entry.index(tk.INSERT)
        self._handle_page_down(event)
        self.search_entry.icursor(cursor_pos)
        return 'break'

    def _handle_home(self, event):
        """Jump to first result."""
        if self.results_listbox.size() > 0:
            cursor_pos = self.search_entry.index(tk.INSERT)
            self.selected_index = 0
            self._update_selection()
            self.search_entry.icursor(cursor_pos)
        return 'break'

    def _handle_end(self, event):
        """Jump to last result."""
        if self.results_listbox.size() > 0:
            cursor_pos = self.search_entry.index(tk.INSERT)
            self.selected_index = self.results_listbox.size() - 1
            self._update_selection()
            self.search_entry.icursor(cursor_pos)
        return 'break'

    def _handle_listbox_click(self, event):
        """Handle listbox click without losing focus."""
        if self.results_listbox.size() > 0:
            index = self.results_listbox.nearest(event.y)
            if 0 <= index < self.results_listbox.size():
                self.selected_index = index
                self._update_selection()
                self.search_entry.focus()
        return 'break'

    def _handle_listbox_double_click(self, event):
        """Handle listbox double-click to execute hotkey."""
        if self.results_listbox.size() > 0:
            index = self.results_listbox.nearest(event.y)
            if 0 <= index < self.results_listbox.size():
                self.selected_index = index
                self.on_hotkey_selected(self.selected_index)
        return 'break'

    def _handle_mouse_wheel(self, event):
        """Handle mouse wheel scrolling."""
        if self.results_listbox.size() > 0:
            ctrl_pressed = event.state & 0x4
            
            if event.num == 5 or event.delta < 0:  # Scroll down
                if ctrl_pressed:
                    self._handle_ctrl_page_down(event)
                else:
                    self._handle_down(event)
            else:  # Scroll up
                if ctrl_pressed:
                    self._handle_ctrl_page_up(event)
                else:
                    self._handle_up(event)
                    
            self.search_entry.focus()
        return 'break'

    def _update_selection(self):
        """Update listbox selection and ensure visibility."""
        self.results_listbox.selection_clear(0, tk.END)
        self.results_listbox.selection_set(self.selected_index)
        self.results_listbox.see(self.selected_index)

    def reset_selection(self):
        """Reset selection to first item."""
        self.selected_index = 0
        if self.results_listbox.size() > 0:
            self._update_selection()

    def get_selected_index(self):
        """Get current selection index."""
        return self.selected_index
