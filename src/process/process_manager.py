import win32gui
import win32process
import psutil
import os

class ProcessManager:
    def __init__(self):
        """Initialize the process manager."""
        self.last_window = None
        self.last_process = None
    
    def get_active_window_process(self):
        """Get the process name of the currently active window."""
        try:
            # Get foreground window handle
            hwnd = win32gui.GetForegroundWindow()
            if not hwnd:
                print("[DEBUG] No foreground window found")
                return None
                
            # Get process ID from window handle
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            if not pid:
                print("[DEBUG] Could not get process ID")
                return None
                
            # Get process name
            try:
                process = psutil.Process(pid)
                process_name = process.name().lower()
                # Remove extension
                process_name = os.path.splitext(process_name)[0]
                print(f"[DEBUG] Active window process: {process_name}")
                return process_name
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                print("[DEBUG] Could not access process")
                return None
                
        except Exception as e:
            print(f"[DEBUG] Error getting active window process: {e}")
            return None
            
    def get_active_window_position(self):
        """Get the position and size of the currently active window."""
        try:
            # Get foreground window handle
            hwnd = win32gui.GetForegroundWindow()
            if not hwnd:
                print("[DEBUG] No foreground window found")
                return None
                
            # Get window rect
            try:
                left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                width = right - left
                height = bottom - top
                
                print(f"[DEBUG] Window position: x={left}, y={top}, width={width}, height={height}")
                return {
                    'x': left,
                    'y': top,
                    'width': width,
                    'height': height
                }
            except Exception as e:
                print(f"[DEBUG] Could not get window rect: {e}")
                return None
                
        except Exception as e:
            print(f"[DEBUG] Error getting window position: {e}")
            return None
