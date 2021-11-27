#!/usr/bin/python3
import tkinter as tk
import os
import sys

class LabelCount():
    def __init__(self):
        self.n = 0
        self.user = os.getenv('USER')        

    def gui(self):
        self.root = tk.Tk()
        
        self.root.title(self.user)

        self.frame_1 = tk.Frame(self.root)
        self.frame_2 = tk.Frame(self.root)

        self.text_1 = f'label_1, n = {self.n}'
        self.text_2 = f'label_2, n = {self.n}'

        self.label_1 = tk.Label(self.frame_1, text = self.text_1, width = 20)
        self.label_2 = tk.Label(self.frame_1, text = self.text_2, width = 20)

        self.click_me = tk.Button(self.frame_2, text = 'Click me!',
            command = lambda: self.onClickMeButton())

        self.exit_button = tk.Button(self.root,
            text = 'Exit',
            command = lambda: self.onExitButton())

        self.label_1.pack(side = 'left')
        self.label_2.pack(side = 'right')
        self.frame_1.pack()
        self.click_me.pack(side = 'bottom')
        self.exit_button.pack(side = 'bottom')
        self.frame_2.pack()

        self.root.mainloop()
        
    def onExitButton(self):
        sys.exit(0)

    def onClickMeButton(self):

        self.n += 1

        self.text_1 = f'label_1, n = {self.n}'
        self.text_2 = f'label_2, n = {self.n}'

        self.label_1.configure(text = self.text_1)
        self.label_2.configure(text = self.text_2)


if'__main__'== __name__:
    
    gui = LabelCount()
    gui.gui()