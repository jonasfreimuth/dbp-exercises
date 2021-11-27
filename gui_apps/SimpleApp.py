#!/usr/bin/python3
import tkinter as tk
import os
import sys

def gui():
    root = tk.Tk()
    
    root.title('JonasFreimuth')

    base_frame = tk.Frame(root)
    exit_button = tk.Button(root,
     text = 'Exit', width = 20,
     command = lambda: sys.exit(0))

    base_frame.pack()
    exit_button.pack()

    root.mainloop()
    
def onExitButton():
    # implementation
    pass
     
    
if'__main__'== __name__:
    gui()
