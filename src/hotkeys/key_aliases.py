"""Module containing key name aliases for consistent key mapping."""

KEY_ALIASES = {
    # Command/Control variants
    'command': 'ctrl',
    'control': 'ctrl',
    
    # Numpad keys
    'numpad+': '+',
    'numpad-': '-',
    
    # Plus key variants
    'plus': '+',
    
    # Page Up/Down variants
    'pgup': 'pageup',
    'pgdn': 'pagedown',
    'pgdown': 'pagedown'
}

# Set of valid keys for validation
VALID_KEYS = {
    'esc', 'enter', 'tab', 'space', 'backspace', 'delete',
    'up', 'down', 'left', 'right', 'home', 'end', 'pageup', 'pagedown',
    'insert', '+', '-', '*', '/', '\\', '=', 'win', 'command', 'control',
    'numpad+', 'numpad-', '?', ';', ','
}

# Add letters
VALID_KEYS.update(chr(i) for i in range(ord('a'), ord('z') + 1))

# Add numbers
VALID_KEYS.update(str(i) for i in range(10))

# Add function keys
VALID_KEYS.update(f'f{i}' for i in range(1, 13))
