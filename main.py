import tkinter as tk
from gui import setup_ui

# create main application window
root = tk.Tk()
root.title("BMP Image Display")
root.resizable(False, False)

# setup ui components
setup_ui(root)

# run the application
root.mainloop()