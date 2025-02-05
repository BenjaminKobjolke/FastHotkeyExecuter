import tkinter as tk
from tkinter import ttk

class UIManager:
    def __init__(self, root, theme_manager):
        self.window = root
        self.theme_manager = theme_manager
        self.search_frame = None
        self.search_entry = None
        self.search_var = None
        self.results_listbox = None
        self.base_height = self.theme_manager.settings['height']
        self._create_ui()

    def _create_ui(self):
        """Create and configure UI components."""
        # Create main search frame
        self.search_frame = tk.Frame(
            self.window,
            bg=self.theme_manager.settings['background_color']
        )
        self.search_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Create search entry
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            self.search_frame,
            textvariable=self.search_var,
            font=('Arial', self.theme_manager.settings['font_size']),
            width=1  # Force single-line
        )
        # Configure entry appearance
        self._configure_entry_appearance()
        self.search_entry.pack(fill=tk.X, expand=False, padx=5, pady=5)

        # Create results listbox
        self.results_listbox = tk.Listbox(
            self.search_frame,
            **self.theme_manager.get_listbox_style(),
            height=0,  # Will be shown only when needed
            takefocus=0  # Prevent listbox from taking focus
        )
        self.results_listbox.pack(fill=tk.BOTH, expand=True, padx=5)

    def get_search_entry(self):
        """Get the search entry widget."""
        return self.search_entry

    def get_search_var(self):
        """Get the search StringVar."""
        return self.search_var

    def get_results_listbox(self):
        """Get the results listbox widget."""
        return self.results_listbox

    def update_results(self, results, placeholder_message="No results"):
        """Update the results listbox with new items."""
        self.results_listbox.delete(0, tk.END)
        
        if results:
            for result in results:
                # Check if it's a hotkey (has 'hotkey' field) or a command
                if 'hotkey' in result:
                    self.results_listbox.insert(tk.END, f"{result['name']} ({result['hotkey']})")
                else:
                    self.results_listbox.insert(tk.END, result['name'])
            list_height = min(5, len(results))
            self.results_listbox.configure(height=list_height)
            # Calculate total height based on base height plus additional space for results
            total_height = self.base_height + (list_height * 20)  # Approximate 20 pixels per list item
            self.window.geometry(f"{self.theme_manager.settings['width']}x{total_height}")
        else:
            self.results_listbox.insert(tk.END, placeholder_message)
            self.results_listbox.itemconfig(0, fg='#666666')  # Gray out message
            self.results_listbox.configure(height=1)
            # Use base height for empty results
            self.window.geometry(f"{self.theme_manager.settings['width']}x{self.base_height}")

    def create_dialog(self, message, on_ok=None):
        """Create and return a styled dialog window."""
        dialog = tk.Toplevel(self.window)
        dialog.withdraw()
        dialog.title("Message")
        
        # Configure dialog window
        dialog.attributes('-topmost', True)
        dialog.overrideredirect(True)
        dialog.configure(bg=self.theme_manager.settings['background_color'])
        
        # Create message label
        msg = tk.Label(
            dialog,
            text=message,
            bg=self.theme_manager.settings['input_background_color'],
            fg=self.theme_manager.settings['input_text_color'],
            font=('Arial', self.theme_manager.settings['font_size']),
            wraplength=300,
            padx=10,
            pady=10
        )
        msg.pack(padx=10, pady=10)
        
        # Create OK button with hover effects and default focus
        ok_button = tk.Button(
            dialog,
            text="OK",
            command=on_ok if on_ok else dialog.destroy,
            bg=self.theme_manager.settings['input_background_color'],
            fg=self.theme_manager.settings['input_text_color'],
            activebackground=self.theme_manager.settings['input_select_background'],
            activeforeground=self.theme_manager.settings['input_select_foreground'],
            font=('Arial', self.theme_manager.settings['font_size']),
            relief='solid',
            bd=1,
            padx=10,
            pady=5,
            cursor='hand2',
            default='active'  # Make it the default button
        )
        
        # Schedule focus to OK button after dialog appears
        dialog.after(1, lambda: ok_button.focus_set())
        
        # Add hover effects
        def on_enter(e):
            ok_button.config(
                bg=self.theme_manager.settings['input_select_background'],
                fg=self.theme_manager.settings['input_select_foreground']
            )
        
        def on_leave(e):
            ok_button.config(
                bg=self.theme_manager.settings['input_background_color'],
                fg=self.theme_manager.settings['input_text_color']
            )
        
        ok_button.bind('<Enter>', on_enter)
        ok_button.bind('<Leave>', on_leave)
        ok_button.pack(pady=(0, 10))

        # Allow closing dialog with any key or clicking outside
        dialog.bind('<Key>', lambda e: dialog.destroy())
        dialog.bind('<Button-1>', lambda e: dialog.destroy())
        dialog.bind('<Button-3>', lambda e: dialog.destroy())

        return dialog

    def show_dialog(self, dialog):
        """Show a dialog window centered on screen."""
        # Center dialog on screen
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Show dialog and focus it
        dialog.deiconify()
        dialog.grab_set()
        dialog.focus_force()  # Force focus to dialog window
        dialog.lift()         # Ensure dialog is on top
        dialog.wait_window()

    def clear_search(self):
        """Clear the search entry."""
        self.search_var.set('')

    def _configure_entry_appearance(self):
        """Configure the appearance of the search entry."""
        self.search_entry.configure(
            bg=self.theme_manager.settings['input_background_color'],
            fg=self.theme_manager.settings['input_text_color'],
            insertbackground=self.theme_manager.settings['input_text_color'],
            selectbackground=self.theme_manager.settings['input_select_background'],
            selectforeground=self.theme_manager.settings['input_select_foreground'],
            relief='solid',
            bd=1,
            highlightthickness=0,
            disabledbackground=self.theme_manager.settings['input_background_color'],
            disabledforeground=self.theme_manager.settings['input_text_color'],
            readonlybackground=self.theme_manager.settings['input_background_color']
        )
