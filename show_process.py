import ctypes
import time
import psutil

user32 = ctypes.windll.user32

time.sleep(3)  # Wait 3 seconds before grabbing the active window
hwnd = user32.GetForegroundWindow()  # Handle of the current foreground window

pid = ctypes.c_ulong()
user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

process = psutil.Process(pid.value)
print(process.name())  # Prints the active window's process name
