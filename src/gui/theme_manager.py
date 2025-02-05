import tkinter as tk
from tkinter import ttk

class ThemeManager:
    def __init__(self, root, config_manager):
        self.window = root
        self.config_manager = config_manager
        self.settings = config_manager.get_window_settings()
        self._configure_theme()

    def _configure_theme(self):
        """Configure global theme settings."""
        # Configure global theme settings
        self.window.configure(bg=self.settings['background_color'])
        
        # Configure dialog styles
        self._configure_dialog_styles()
        
        # Configure ttk styles
        self._configure_ttk_styles()

    def _configure_dialog_styles(self):
        """Configure dialog-specific styles."""
        # Message styles
        self.window.option_add('*Dialog.msg.font', ('Arial', self.settings['font_size']))
        self.window.option_add('*Dialog.msg.background', self.settings['input_background_color'])
        self.window.option_add('*Dialog.msg.foreground', self.settings['input_text_color'])
        self.window.option_add('*Dialog.msg.highlightBackground', self.settings['background_color'])
        self.window.option_add('*Dialog.msg.highlightColor', self.settings['background_color'])
        self.window.option_add('*Dialog.msg.relief', 'flat')
        self.window.option_add('*Dialog.msg.padx', '10')
        self.window.option_add('*Dialog.msg.pady', '10')
        self.window.option_add('*Dialog.msg.wraplength', '300')

        # Window styles
        self.window.option_add('*Dialog.background', self.settings['background_color'])
        self.window.option_add('*Dialog.foreground', self.settings['text_color'])
        self.window.option_add('*Dialog.highlightBackground', self.settings['background_color'])
        self.window.option_add('*Dialog.highlightColor', self.settings['background_color'])

        # Button styles
        self.window.option_add('*Dialog.Button.background', self.settings['input_background_color'])
        self.window.option_add('*Dialog.Button.foreground', self.settings['input_text_color'])
        self.window.option_add('*Dialog.Button.activeBackground', self.settings['input_select_background'])
        self.window.option_add('*Dialog.Button.activeForeground', self.settings['input_select_foreground'])
        self.window.option_add('*Dialog.Button.highlightBackground', self.settings['background_color'])
        self.window.option_add('*Dialog.Button.highlightColor', self.settings['background_color'])
        self.window.option_add('*Dialog.Button.font', ('Arial', self.settings['font_size']))
        self.window.option_add('*Dialog.Button.borderwidth', '1')
        self.window.option_add('*Dialog.Button.relief', 'solid')
        self.window.option_add('*Dialog.Button.padx', '10')
        self.window.option_add('*Dialog.Button.pady', '5')

        # Frame styles
        self.window.option_add('*Dialog.Frame.background', self.settings['background_color'])
        self.window.option_add('*Dialog.Frame.highlightBackground', self.settings['background_color'])
        self.window.option_add('*Dialog.Frame.highlightColor', self.settings['background_color'])
        self.window.option_add('*Dialog.Frame.relief', 'flat')

        # Label styles
        self.window.option_add('*Dialog.Label.background', self.settings['background_color'])
        self.window.option_add('*Dialog.Label.foreground', self.settings['input_text_color'])
        self.window.option_add('*Dialog.Label.highlightBackground', self.settings['background_color'])
        self.window.option_add('*Dialog.Label.highlightColor', self.settings['background_color'])
        self.window.option_add('*Dialog.Label.font', ('Arial', self.settings['font_size']))

    def _configure_ttk_styles(self):
        """Configure ttk widget styles."""
        style = ttk.Style()
        
        # Frame style
        style.configure('Dark.TFrame',
            background=self.settings['background_color'],
            borderwidth=0,
            relief='flat'
        )
        style.map('Dark.TFrame',
            background=[
                ('active', self.settings['background_color']),
                ('!active', self.settings['background_color'])
            ]
        )

    def get_listbox_style(self):
        """Get style configuration for listbox."""
        return {
            'bg': self.settings['input_background_color'],
            'fg': self.settings['input_text_color'],
            'font': ('Arial', self.settings['font_size']),
            'selectmode': tk.SINGLE,
            'selectbackground': self.settings['input_select_background'],
            'selectforeground': self.settings['input_select_foreground'],
            'borderwidth': 1,
            'highlightthickness': 1,
            'relief': 'solid',
            'highlightbackground': self.settings['background_color'],
            'highlightcolor': self.settings['background_color'],
            'bd': 1,
            'activestyle': 'none'
        }

    def get_entry_style(self):
        """Get style name for themed entry widget."""
        return 'Dark.TEntry'

    def get_frame_style(self):
        """Get style name for themed frame."""
        return 'Dark.TFrame'
