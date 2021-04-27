import ctypes  # An included library with Python install.   
def createMsgBox(message,title):
    ctypes.windll.user32.MessageBoxW(0, message,title, 1)