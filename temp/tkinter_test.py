#!/usr/bin/python3

import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog as tkfile
import tkinter.ttk as ttk
import sys
import os
import re
import argparse
import gzip

# add location of GuiBaseClass
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../GuiApp2/'))

from GuiBaseClass import GuiBaseClass

class examTest(GuiBaseClass):
    def __init__(self, root, filename = ''):
        super().__init__(root)
        
        self.filename = filename
        
        self.base_frame = self.getBaseFrame()
        
        # add menu entries
        menu_file = self.getMenu('menubar', 'File')
        menu_file.insert_command(1, label = 'Open...', command = self.fileOpen)

        self.notebook = ttk.Notebook(self.base_frame)

        self.text = ttk.Label(self.notebook, text = 'Your ad here', anchor = tk.CENTER)

        self.labframes = [None] * len(self.filename)
        self.txtbxs = [None] * len(self.filename)

        for i in range(len(self.filename)):
            self.labframes[i] = tk.LabelFrame(self.notebook, width = 200, height = 200)

            self.labframes[i].configure(text = self.filename[i])

            self.txtbxs[i] = ttk.Label(self.labframes[i], text = self.getHead(self.filename[i]))
        
        # pack everything
        self.base_frame.pack(fill = 'both', expand = True)
        self.notebook.pack(fill = 'both', expand = True)

        self.notebook.add(self.text, text = 'This is an ad.')

        for i in range(len(self.labframes)):
            self.notebook.add(self.labframes[i], text = f'Labelframe {i}')
            self.txtbxs[i].pack(expand = True, fill = 'both')

    def fileOpen(self, *args):
        """
        Saves filename chosen in file dialog.
        """ 
        self.filename = tkfile.askopenfilename(initialdir = os.getcwd())    

    def getHead(self, filename):
        infile = gzip.open(filename)

        head = next(infile)

        infile.close()

        return(head)
        
if __name__ == '__main__':    
    parser = argparse.ArgumentParser(
        description = 'Test for DBP Exam, learning new tkinter widgets.')
    parser.add_argument('-i','--infile',
        help = 'Specifies input file location.', default = '',
            required = False, nargs = '*')
    
    args = vars(parser.parse_args())
    filenames = args['infile']

    print(args)

    [print(name) for name in filenames]
    
    root = tk.Tk()

    app = examTest(root, filename = filenames)

    app.mainLoop()