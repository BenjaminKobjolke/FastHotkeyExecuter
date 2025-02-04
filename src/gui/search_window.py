import tkinter as tk
from tkinter import ttk, messagebox
import os
import time

class SearchWindow:
    def __init__(self, config_manager, process_manager, hotkey_loader, hotkey_executor):
        # Store dependencies
        self.config_manager = config_manager
        self.process_manager = process_manager
        self.hotkey_loader = hotkey_loader
        self.hotkey_executor = hotkey_executor
        
        # Get settings before creating any widgets
        settings = self.config_manager.get_window_settings()
        
        # Configure global theme settings before creating root window
        root = tk.Tk()
        root.option_add('*TEntry*Background', settings['input_background_color'])
        root.option_add('*TEntry*Foreground', settings['input_text_color'])
        root.option_add('*TEntry*selectBackground', settings['input_select_background'])
        root.option_add('*TEntry*selectForeground', settings['input_select_foreground'])
        root.option_add('*TEntry*highlightBackground', settings['background_color'])
        root.option_add('*TEntry*highlightColor', settings['background_color'])
        root.option_add('*TEntry*insertBackground', settings['input_text_color'])
        root.withdraw()
        
        # Use the configured root window
        self.window = root
        
        self.setup_window()
        self.current_results = []
        self.selected_index = 0
        self.current_app = None  # Store the current application name
        
    def setup_window(self):
        """Configure the window appearance and behavior."""
        # Configure window behavior
        self.window.overrideredirect(True)  # Remove window decorations
        self.window.attributes('-topmost', True)  # Keep window on top
        self.window.resizable(False, False)  # Prevent resizing
        self.window.protocol("WM_DELETE_WINDOW", lambda: None)  # Prevent Alt+F4
        
        # Prevent window movement and focus loss
        self.window.bind('<B1-Motion>', lambda e: 'break')
        self.window.bind('<Button-1>', lambda e: 'break')
        self.window.bind('<FocusOut>', self._handle_focus_loss)
        self.window.bind('<Alt-Tab>', lambda e: 'break')  # Prevent Alt+Tab
        self.window.bind('<Alt-F4>', lambda e: 'break')   # Prevent Alt+F4
        
        # Get window settings
        settings = self.config_manager.get_window_settings()
        
        # Configure window and global styles
        self.window.configure(bg=settings['background_color'])
        
        # Configure global theme settings
        self.window.option_add('*TEntry*Background', settings['input_background_color'])
        self.window.option_add('*TEntry*Foreground', settings['input_text_color'])
        self.window.option_add('*TEntry*selectBackground', settings['input_select_background'])
        self.window.option_add('*TEntry*selectForeground', settings['input_select_foreground'])
        self.window.option_add('*TEntry*highlightBackground', settings['background_color'])
        self.window.option_add('*TEntry*highlightColor', settings['background_color'])
        self.window.option_add('*TEntry*insertBackground', settings['input_text_color'])  # Cursor color
        
        # Configure dialog message styles
        self.window.option_add('*Dialog.msg.font', ('Arial', settings['font_size']))
        self.window.option_add('*Dialog.msg.background', settings['input_background_color'])
        self.window.option_add('*Dialog.msg.foreground', settings['input_text_color'])
        self.window.option_add('*Dialog.msg.highlightBackground', settings['background_color'])
        self.window.option_add('*Dialog.msg.highlightColor', settings['background_color'])
        self.window.option_add('*Dialog.msg.relief', 'flat')
        self.window.option_add('*Dialog.msg.padx', '10')
        self.window.option_add('*Dialog.msg.pady', '10')
        self.window.option_add('*Dialog.msg.wraplength', '300')  # Wrap long messages
        
        # Configure dialog window styles
        self.window.option_add('*Dialog.background', settings['background_color'])
        self.window.option_add('*Dialog.foreground', settings['text_color'])
        self.window.option_add('*Dialog.highlightBackground', settings['background_color'])
        self.window.option_add('*Dialog.highlightColor', settings['background_color'])
        
        # Configure additional dialog styles for consistent dark theme
        self.window.option_add('*Dialog.Button.background', settings['input_background_color'])
        self.window.option_add('*Dialog.Button.foreground', settings['input_text_color'])
        self.window.option_add('*Dialog.Button.activeBackground', settings['input_select_background'])
        self.window.option_add('*Dialog.Button.activeForeground', settings['input_select_foreground'])
        self.window.option_add('*Dialog.Button.highlightBackground', settings['background_color'])
        self.window.option_add('*Dialog.Button.highlightColor', settings['background_color'])
        self.window.option_add('*Dialog.Button.font', ('Arial', settings['font_size']))
        self.window.option_add('*Dialog.Button.borderwidth', '1')
        self.window.option_add('*Dialog.Button.relief', 'solid')
        self.window.option_add('*Dialog.Button.padx', '10')
        self.window.option_add('*Dialog.Button.pady', '5')
        
        # Configure dialog button hover and pressed states
        self.window.option_add('*Dialog.Button.disabledBackground', settings['input_background_color'])
        self.window.option_add('*Dialog.Button.disabledForeground', settings['input_text_color'])
        self.window.option_add('*Dialog.Button.highlightThickness', '0')
        self.window.option_add('*Dialog.Button.bd', '1')
        
        # Configure dialog frame styles
        self.window.option_add('*Dialog.Frame.background', settings['background_color'])
        self.window.option_add('*Dialog.Frame.highlightBackground', settings['background_color'])
        self.window.option_add('*Dialog.Frame.highlightColor', settings['background_color'])
        self.window.option_add('*Dialog.Frame.relief', 'flat')
        
        # Configure dialog icon styles
        self.window.option_add('*Dialog.Image.background', settings['background_color'])
        self.window.option_add('*Dialog.Label.background', settings['background_color'])
        self.window.option_add('*Dialog.Label.foreground', settings['input_text_color'])
        self.window.option_add('*Dialog.Label.highlightBackground', settings['background_color'])
        self.window.option_add('*Dialog.Label.highlightColor', settings['background_color'])
        self.window.option_add('*Dialog.Label.font', ('Arial', settings['font_size']))
        
        # Configure dialog padding and spacing
        self.window.option_add('*Dialog.padx', '10')
        self.window.option_add('*Dialog.pady', '10')
        self.window.option_add('*Dialog.Frame.padx', '10')
        self.window.option_add('*Dialog.Frame.pady', '10')
        
        # Configure styles
        style = ttk.Style()
        style.configure('Dark.TFrame', 
            background=settings['background_color'],
            borderwidth=0,  # Remove frame border
            relief='flat'   # Flat appearance
        )
        style.map('Dark.TFrame',
            background=[
                ('active', settings['background_color']),
                ('!active', settings['background_color'])
            ]
        )
        
        # Create and configure the search frame with dark theme
        self.search_frame = ttk.Frame(self.window, style='Dark.TFrame')
        self.search_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Configure dark theme style for Entry
        style.configure(
            'Dark.TEntry',
            fieldbackground=settings['input_background_color'],
            foreground=settings['input_text_color'],
            selectbackground=settings['input_select_background'],
            selectforeground=settings['input_select_foreground'],
            padding=[5, 2, 5, 2],  # [left, top, right, bottom]
            borderwidth=1,
            relief='solid',
            bordercolor=settings['background_color']
        )
        style.map('Dark.TEntry',
            fieldbackground=[
                ('readonly', settings['input_background_color']),
                ('disabled', settings['input_background_color']),
                ('active', settings['input_background_color']),
                ('focus', settings['input_background_color']),
                ('!focus', settings['input_background_color']),  # Important: also set unfocused state
                ('hover', settings['input_background_color']),   # Ensure dark background on hover
                ('pressed', settings['input_background_color']), # Ensure dark background when clicked
                ('alternate', settings['input_background_color']) # Ensure dark background in alternate state
            ],
            background=[
                ('readonly', settings['input_background_color']),
                ('disabled', settings['input_background_color']),
                ('active', settings['input_background_color']),
                ('focus', settings['input_background_color']),
                ('!focus', settings['input_background_color']),
                ('hover', settings['input_background_color']),
                ('pressed', settings['input_background_color']),
                ('alternate', settings['input_background_color'])
            ],
            selectbackground=[('focus', settings['input_select_background'])],
            selectforeground=[('focus', settings['input_select_foreground'])]
        )
        
        # Override system theme for Entry widgets
        self.window.option_add('*TEntry*Listbox*Background', settings['input_background_color'])
        self.window.option_add('*TEntry*Listbox*Foreground', settings['input_text_color'])
        self.window.option_add('*TEntry*Listbox*selectBackground', settings['input_select_background'])
        self.window.option_add('*TEntry*Listbox*selectForeground', settings['input_select_foreground'])
        
        # Create search entry with dark theme
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            self.search_frame,
            textvariable=self.search_var,
            font=('Arial', settings['font_size']),
            style='Dark.TEntry',
            width=1  # Force single-line by setting minimal width
        )
        self.search_entry.pack(fill=tk.X, expand=False, padx=5, pady=5)
        
        # Override Entry widget's default background
        self.search_entry.configure(background=settings['input_background_color'])
        
        # Create listbox for results with consistent dark theme
        self.results_listbox = tk.Listbox(
            self.search_frame,
            bg=settings['input_background_color'],
            fg=settings['input_text_color'],
            font=('Arial', settings['font_size']),
            selectmode=tk.SINGLE,
            height=0,  # Will be shown only when needed
            selectbackground=settings['input_select_background'],
            selectforeground=settings['input_select_foreground'],
            borderwidth=1,
            highlightthickness=1,
            relief='solid',
            highlightbackground=settings['background_color'],
            highlightcolor=settings['background_color'],
            bd=1,
            activestyle='none',  # Remove dotted line around selected item
            takefocus=0  # Prevent listbox from taking focus
        )
        self.results_listbox.pack(fill=tk.BOTH, expand=True, padx=5)
        
        # Prevent listbox from taking focus and handle mouse events
        self.results_listbox.bind('<Button-1>', self._handle_listbox_click)
        self.results_listbox.bind('<Double-Button-1>', self._handle_listbox_double_click)
        self.results_listbox.bind('<B1-Motion>', lambda e: 'break')
        self.results_listbox.bind('<MouseWheel>', self._handle_mouse_wheel)
        self.results_listbox.bind('<Button-4>', self._handle_mouse_wheel)  # Linux mouse wheel up
        self.results_listbox.bind('<Button-5>', self._handle_mouse_wheel)  # Linux mouse wheel down
        
        # Bind events
        self.search_var.trace('w', self.on_search_change)
        # Bind events for input field
        self.search_entry.bind('<Return>', self.on_enter)
        self.search_entry.bind('<Escape>', self.hide)
        self.search_entry.bind('<Up>', self.on_up)
        self.search_entry.bind('<Down>', self.on_down)
        self.search_entry.bind('<Control-Up>', self.on_ctrl_up)  # Quick navigation up
        self.search_entry.bind('<Control-Down>', self.on_ctrl_down)  # Quick navigation down
        self.search_entry.bind('<Prior>', self.on_page_up)  # PageUp
        self.search_entry.bind('<Next>', self.on_page_down)  # PageDown
        self.search_entry.bind('<Control-Prior>', self.on_ctrl_page_up)  # Ctrl+PageUp
        self.search_entry.bind('<Control-Next>', self.on_ctrl_page_down)  # Ctrl+PageDown
        self.search_entry.bind('<Control-Home>', self.on_home)  # Jump to first
        self.search_entry.bind('<Control-End>', self.on_end)  # Jump to last
        
        # Prevent multiline input and ensure single-line behavior
        self.search_entry.bind('<Control-Return>', lambda e: 'break')
        self.search_entry.bind('<Shift-Return>', lambda e: 'break')
        self.search_entry.bind('<Alt-Return>', lambda e: 'break')
        self.search_entry.bind('<Tab>', lambda e: 'break')  # Prevent focus change
        self.search_entry.bind('<Control-Tab>', lambda e: 'break')
        self.search_entry.bind('<Control-a>', lambda e: self.search_entry.select_range(0, tk.END))  # Select all text
        
        # Set window size
        self.window.geometry(f"{settings['width']}x{settings['height']}")
        
    def show(self):
        """Show the search window centered on the active window."""
        try:
            # Get the process name when window is first shown
            self.current_app = self.process_manager.get_active_window_process()
            print(f"[DEBUG] Detected application on show: {self.current_app}")
            
            # Don't show window if no active window detected
            if not self.current_app:
                print("[DEBUG] No active window detected, not showing search window")
                return
            
            # Show message if no hotkeys found for the application
            if not self.hotkey_loader.get_hotkeys_for_app(self.current_app):
                self.window.withdraw()
                # Create custom dialog with OK button
                dialog = tk.Toplevel(self.window)  # Use main window as parent
                dialog.withdraw()  # Hide initially
                dialog.title("No Hotkeys")
                
                # Create message label
                msg = tk.Label(
                    dialog,
                    text=f'No hotkeys found for "{self.current_app}"',
                    bg=self.config_manager.get_window_settings()['input_background_color'],
                    fg=self.config_manager.get_window_settings()['input_text_color'],
                    font=('Arial', self.config_manager.get_window_settings()['font_size']),
                    wraplength=300,
                    padx=10,
                    pady=10
                )
                msg.pack(padx=10, pady=10)
                
                # Create OK button
                # Create OK button with hover effects
                ok_button = tk.Button(
                    dialog,
                    text="OK",
                    command=dialog.destroy,
                    bg=self.config_manager.get_window_settings()['input_background_color'],
                    fg=self.config_manager.get_window_settings()['input_text_color'],
                    activebackground=self.config_manager.get_window_settings()['input_select_background'],
                    activeforeground=self.config_manager.get_window_settings()['input_select_foreground'],
                    font=('Arial', self.config_manager.get_window_settings()['font_size']),
                    relief='solid',
                    bd=1,
                    padx=10,
                    pady=5,
                    cursor='hand2'  # Show hand cursor on hover
                )
                
                # Add hover effects
                def on_enter(e):
                    ok_button.config(
                        bg=self.config_manager.get_window_settings()['input_select_background'],
                        fg=self.config_manager.get_window_settings()['input_select_foreground']
                    )
                
                def on_leave(e):
                    ok_button.config(
                        bg=self.config_manager.get_window_settings()['input_background_color'],
                        fg=self.config_manager.get_window_settings()['input_text_color']
                    )
                
                ok_button.bind('<Enter>', on_enter)
                ok_button.bind('<Leave>', on_leave)
                ok_button.pack(pady=(0, 10))
                # Show dialog
                self._show_dialog(dialog)
                return
        
            # Get active window position
            active_pos = self.process_manager.get_active_window_position()
            if not active_pos:
                print("[DEBUG] Could not get active window position")
                return
                
            # Calculate center position
            window_width = self.config_manager.get_window_settings()['width']
            window_height = self.config_manager.get_window_settings()['height']
            
            x = active_pos['x'] + (active_pos['width'] - window_width) // 2
            y = active_pos['y'] + (active_pos['height'] - window_height) // 2
            
            self.window.geometry(f"+{x}+{y}")
            
            # Clear previous search and show all available hotkeys
            self.search_var.set('')
            self.current_results = self.hotkey_loader.get_hotkeys_for_app(self.current_app)
            
            # Update results display
            self.results_listbox.delete(0, tk.END)
            if self.current_results:
                for hotkey in self.current_results:
                    self.results_listbox.insert(tk.END, f"{hotkey['name']} ({hotkey['hotkey']})")
                self.results_listbox.configure(height=min(5, len(self.current_results)))  # Show up to 5 results
                self.window.geometry(f"{self.config_manager.get_window_settings()['width']}x{200}")
                # Select first result
                self.selected_index = 0
                self.results_listbox.selection_clear(0, tk.END)
                self.results_listbox.selection_set(0)
            else:
                self.results_listbox.insert(tk.END, "No hotkeys available")
                self.results_listbox.itemconfig(0, fg='#666666')  # Gray out the message
                self.results_listbox.configure(height=1)
                self.window.geometry(f"{self.config_manager.get_window_settings()['width']}x{80}")
            
            # Show window and focus search
            self.window.deiconify()
            self.window.lift()
            self.window.focus_force()
            self.search_entry.focus()
            
        except Exception as e:
            print(f"[DEBUG] Error showing search window: {e}")
            self.window.withdraw()
        
    def hide(self, event=None):
        """Hide the search window."""
        print("[DEBUG] Hiding search window")
        self.window.withdraw()
        self.window.update()  # Force window update
        time.sleep(0.1)  # Small delay to ensure window is hidden
        print("[DEBUG] Search window hidden")
        self.current_app = None  # Clear the current app so it will be re-detected next time
        
    def on_search_change(self, *args):
        """Handle search input changes."""
        search_text = self.search_var.get()
        print(f"[DEBUG] Search triggered - Text: '{search_text}'")
        
        if self.current_app:
            print(f"[DEBUG] Searching hotkeys for application: {self.current_app}")
            # Get search results
            if not search_text:
                # Show all hotkeys when search is empty
                self.current_results = self.hotkey_loader.get_hotkeys_for_app(self.current_app)
            else:
                self.current_results = self.hotkey_loader.search_hotkeys(self.current_app, search_text)
            print(f"[DEBUG] Found {len(self.current_results)} total hotkeys for {self.current_app}")
        else:
            print("[DEBUG] No application was detected when window was shown")
            self.current_results = []
            if search_text:  # Only show message if user has typed something
                self.window.withdraw()
                # Create custom dialog with OK button
                dialog = tk.Toplevel(self.window)  # Use main window as parent
                dialog.withdraw()  # Hide initially
                dialog.title("No Hotkeys")
                
                # Create message label
                msg = tk.Label(
                    dialog,
                    text="No hotkeys found for this application",
                    bg=self.config_manager.get_window_settings()['input_background_color'],
                    fg=self.config_manager.get_window_settings()['input_text_color'],
                    font=('Arial', self.config_manager.get_window_settings()['font_size']),
                    wraplength=300,
                    padx=10,
                    pady=10
                )
                msg.pack(padx=10, pady=10)
                
                # Create OK button
                # Create OK button with hover effects
                ok_button = tk.Button(
                    dialog,
                    text="OK",
                    command=dialog.destroy,
                    bg=self.config_manager.get_window_settings()['input_background_color'],
                    fg=self.config_manager.get_window_settings()['input_text_color'],
                    activebackground=self.config_manager.get_window_settings()['input_select_background'],
                    activeforeground=self.config_manager.get_window_settings()['input_select_foreground'],
                    font=('Arial', self.config_manager.get_window_settings()['font_size']),
                    relief='solid',
                    bd=1,
                    padx=10,
                    pady=5,
                    cursor='hand2'  # Show hand cursor on hover
                )
                
                # Add hover effects
                def on_enter(e):
                    ok_button.config(
                        bg=self.config_manager.get_window_settings()['input_select_background'],
                        fg=self.config_manager.get_window_settings()['input_select_foreground']
                    )
                
                def on_leave(e):
                    ok_button.config(
                        bg=self.config_manager.get_window_settings()['input_background_color'],
                        fg=self.config_manager.get_window_settings()['input_text_color']
                    )
                
                ok_button.bind('<Enter>', on_enter)
                ok_button.bind('<Leave>', on_leave)
                ok_button.pack(pady=(0, 10))
                # Show dialog
                self._show_dialog(dialog)
                
                self.window.deiconify()
                self.window.lift()
                self.window.focus_force()
                self.search_entry.focus()
            
        # Update results display
        self.results_listbox.delete(0, tk.END)
        for hotkey in self.current_results:
            self.results_listbox.insert(tk.END, f"{hotkey['name']} ({hotkey['hotkey']})")
        
        # Show/hide results list
        if self.current_results:
            self.results_listbox.configure(height=min(5, len(self.current_results)))  # Show up to 5 results
            self.results_listbox.pack(fill=tk.BOTH, expand=True, padx=5)
            self.window.geometry(f"{self.config_manager.get_window_settings()['width']}x{200}")
        else:
            # Show "No results" message in listbox
            self.results_listbox.delete(0, tk.END)
            self.results_listbox.insert(tk.END, "No matching hotkeys found")
            self.results_listbox.itemconfig(0, fg='#666666')  # Gray out the message
            self.results_listbox.configure(height=1)  # Set fixed height for placeholder
            self.results_listbox.pack(fill=tk.BOTH, expand=True, padx=5)
            self.window.geometry(f"{self.config_manager.get_window_settings()['width']}x{80}")  # Smaller height for no results
        
        # Reset selection
        self.selected_index = 0
        if self.current_results:
            self.results_listbox.selection_clear(0, tk.END)
            self.results_listbox.selection_set(0)
                
    def on_enter(self, event):
        """Handle enter key press."""
        if self.current_results:
            selected_hotkey = self.current_results[self.selected_index]
            print(f"[DEBUG] Executing hotkey: {selected_hotkey['name']} ({selected_hotkey['hotkey']})")
            self.hide()
            self.hotkey_executor.execute_hotkey(selected_hotkey)
            
    def on_up(self, event):
        """Handle up arrow key."""
        if self.current_results:
            self.selected_index = max(0, self.selected_index - 1)
            self.results_listbox.selection_clear(0, tk.END)
            self.results_listbox.selection_set(self.selected_index)
            self.results_listbox.see(self.selected_index)
            
    def on_down(self, event):
        """Handle down arrow key."""
        if self.current_results:
            self.selected_index = min(len(self.current_results) - 1, self.selected_index + 1)
            self.results_listbox.selection_clear(0, tk.END)
            self.results_listbox.selection_set(self.selected_index)
            self.results_listbox.see(self.selected_index)
            
    def on_page_up(self, event):
        """Handle page up key."""
        if self.current_results:
            # Move up by the listbox height (max 5)
            self.selected_index = max(0, self.selected_index - 5)
            self.results_listbox.selection_clear(0, tk.END)
            self.results_listbox.selection_set(self.selected_index)
            self.results_listbox.see(self.selected_index)
            
    def on_page_down(self, event):
        """Handle page down key."""
        if self.current_results:
            # Move down by the listbox height (max 5)
            self.selected_index = min(len(self.current_results) - 1, self.selected_index + 5)
            self.results_listbox.selection_clear(0, tk.END)
            self.results_listbox.selection_set(self.selected_index)
            self.results_listbox.see(self.selected_index)
            
    def on_ctrl_up(self, event):
        """Handle Ctrl+Up key."""
        if self.current_results:
            # Move up while preserving cursor position
            cursor_pos = self.search_entry.index(tk.INSERT)
            self.selected_index = max(0, self.selected_index - 1)
            self.results_listbox.selection_clear(0, tk.END)
            self.results_listbox.selection_set(self.selected_index)
            self.results_listbox.see(self.selected_index)
            self.search_entry.icursor(cursor_pos)
            return 'break'  # Prevent default Up key behavior
            
    def on_ctrl_page_up(self, event):
        """Handle Ctrl+PageUp key."""
        if self.current_results:
            # Move up by page while preserving cursor position
            cursor_pos = self.search_entry.index(tk.INSERT)
            self.selected_index = max(0, self.selected_index - 5)
            self.results_listbox.selection_clear(0, tk.END)
            self.results_listbox.selection_set(self.selected_index)
            self.results_listbox.see(self.selected_index)
            self.search_entry.icursor(cursor_pos)
            return 'break'  # Prevent default PageUp key behavior
            
    def on_ctrl_page_down(self, event):
        """Handle Ctrl+PageDown key."""
        if self.current_results:
            # Move down by page while preserving cursor position
            cursor_pos = self.search_entry.index(tk.INSERT)
            self.selected_index = min(len(self.current_results) - 1, self.selected_index + 5)
            self.results_listbox.selection_clear(0, tk.END)
            self.results_listbox.selection_set(self.selected_index)
            self.results_listbox.see(self.selected_index)
            self.search_entry.icursor(cursor_pos)
            return 'break'  # Prevent default PageDown key behavior
            
    def on_ctrl_down(self, event):
        """Handle Ctrl+Down key."""
        if self.current_results:
            # Move down while preserving cursor position
            cursor_pos = self.search_entry.index(tk.INSERT)
            self.selected_index = min(len(self.current_results) - 1, self.selected_index + 1)
            self.results_listbox.selection_clear(0, tk.END)
            self.results_listbox.selection_set(self.selected_index)
            self.results_listbox.see(self.selected_index)
            self.search_entry.icursor(cursor_pos)
            return 'break'  # Prevent default Down key behavior
            
    def on_home(self, event):
        """Handle Ctrl+Home key."""
        if self.current_results:
            # Jump to first result while preserving cursor position
            cursor_pos = self.search_entry.index(tk.INSERT)
            self.selected_index = 0
            self.results_listbox.selection_clear(0, tk.END)
            self.results_listbox.selection_set(self.selected_index)
            self.results_listbox.see(self.selected_index)
            self.search_entry.icursor(cursor_pos)
            return 'break'  # Prevent default Home key behavior
            
    def on_end(self, event):
        """Handle Ctrl+End key."""
        if self.current_results:
            # Jump to last result while preserving cursor position
            cursor_pos = self.search_entry.index(tk.INSERT)
            self.selected_index = len(self.current_results) - 1
            self.results_listbox.selection_clear(0, tk.END)
            self.results_listbox.selection_set(self.selected_index)
            self.results_listbox.see(self.selected_index)
            self.search_entry.icursor(cursor_pos)
            return 'break'  # Prevent default End key behavior
            
    def _handle_listbox_click(self, event):
        """Handle listbox click without losing focus."""
        if not self.current_results:
            return 'break'
            
        # Get clicked item index
        index = self.results_listbox.nearest(event.y)
        if 0 <= index < len(self.current_results):
            self.selected_index = index
            self.results_listbox.selection_clear(0, tk.END)
            self.results_listbox.selection_set(index)
            self.results_listbox.see(index)
            
        # Keep focus on search entry
        self.search_entry.focus()
        return 'break'
        
    def _handle_listbox_double_click(self, event):
        """Handle listbox double-click to execute hotkey."""
        if not self.current_results:
            return 'break'
            
        # Get clicked item index and execute hotkey
        index = self.results_listbox.nearest(event.y)
        if 0 <= index < len(self.current_results):
            self.selected_index = index
            selected_hotkey = self.current_results[self.selected_index]
            print(f"[DEBUG] Double-click executing hotkey: {selected_hotkey['name']} ({selected_hotkey['hotkey']})")
            self.hide()
            self.hotkey_executor.execute_hotkey(selected_hotkey)
            
        return 'break'
        
    def _handle_mouse_wheel(self, event):
        """Handle mouse wheel scrolling."""
        if not self.current_results:
            return 'break'
            
        # Check if Ctrl is pressed
        ctrl_pressed = event.state & 0x4  # Check Control key state
        
        # Get scroll direction
        if event.num == 5 or event.delta < 0:  # Scroll down
            if ctrl_pressed:
                # Move down by page while preserving cursor position
                cursor_pos = self.search_entry.index(tk.INSERT)
                self.selected_index = min(len(self.current_results) - 1, self.selected_index + 5)
                self.search_entry.icursor(cursor_pos)
            else:
                self.selected_index = min(len(self.current_results) - 1, self.selected_index + 1)
        else:  # Scroll up
            if ctrl_pressed:
                # Move up by page while preserving cursor position
                cursor_pos = self.search_entry.index(tk.INSERT)
                self.selected_index = max(0, self.selected_index - 5)
                self.search_entry.icursor(cursor_pos)
            else:
                self.selected_index = max(0, self.selected_index - 1)
            
        # Update selection
        self.results_listbox.selection_clear(0, tk.END)
        self.results_listbox.selection_set(self.selected_index)
        self.results_listbox.see(self.selected_index)
        
        # Keep focus on search entry
        self.search_entry.focus()
        return 'break'
        
    def _handle_focus_loss(self, event):
        """Handle window focus loss."""
        print("[DEBUG] Window lost focus, forcing focus back")
        self.window.after(10, lambda: (
            self.window.lift(),
            self.window.focus_force(),
            self.search_entry.focus()
        ))
        return 'break'
        
    def _show_dialog(self, dialog):
        """Configure and show a dialog window."""
        # Configure dialog window
        dialog.withdraw()  # Hide initially
        dialog.attributes('-topmost', True)  # Keep dialog on top
        dialog.overrideredirect(True)  # Remove title bar
        dialog.configure(bg=self.config_manager.get_window_settings()['background_color'])
        
        # Configure dialog styles
        dialog.option_add('*Dialog.msg.font', ('Arial', self.config_manager.get_window_settings()['font_size']))
        dialog.option_add('*Dialog.msg.background', self.config_manager.get_window_settings()['input_background_color'])
        dialog.option_add('*Dialog.msg.foreground', self.config_manager.get_window_settings()['input_text_color'])
        dialog.option_add('*Dialog.msg.highlightBackground', self.config_manager.get_window_settings()['background_color'])
        dialog.option_add('*Dialog.msg.highlightColor', self.config_manager.get_window_settings()['background_color'])
        dialog.option_add('*Dialog.msg.relief', 'flat')
        dialog.option_add('*Dialog.msg.padx', '10')
        dialog.option_add('*Dialog.msg.pady', '10')
        dialog.option_add('*Dialog.msg.wraplength', '300')
        
        # Allow closing dialog with any key or clicking outside
        close_dialog = lambda e: dialog.destroy()
        dialog.bind('<Key>', close_dialog)  # Bind to any key press
        dialog.bind('<Button-1>', close_dialog)
        dialog.bind('<Button-3>', close_dialog)
        
        # Center dialog on screen
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Show dialog and wait for it to be destroyed
        dialog.deiconify()
        dialog.grab_set()  # Make dialog modal
        dialog.wait_window()  # Wait for dialog to be destroyed
        
    def run(self):
        """Start the window's main loop."""
        self.window.mainloop()
