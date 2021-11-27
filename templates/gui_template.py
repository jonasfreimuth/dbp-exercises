#!/usr/bin/python3

import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog as tkfile
import tkinter.ttk as ttk
import sys
import os
import re
import argparse

# add location of GuiBaseClass
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../GuiApp2/'))

from GuiBaseClass import GuiBaseClass

class tpClass(GuiBaseClass):
    def __init__(self, root, filename = ''):
        super().__init__(root)

        self.filename = filename       

        self.base_frame = self.getBaseFrame()

        # add menu entries
        menu_file = self.getMenu('menubar', 'File')
        menu_file.insert_command(1, label = 'Open...', command = self.fileOpen)        

        # pack everything
        self.base_frame.pack()

        pass

    def fileOpen(self, *args, filename = ''):
        
        if not filename:
            self.filename = tkfile.askopenfilename(initialdir = os.getcwd())
            infile = open(self.filename, 'r')

        else: 
            infile = open(filename)

        print(infile)

        infile.close()


if __name__ == '__main__':

    infile_format = ''

    parser = argparse.ArgumentParser(description = """ """)
    parser.add_argument('-i', '--infile',
        help = f'Speciefies path to input file in {infile_format} format.',
        type = str)        

    args = vars(parser.parse_args())

    # argument checks - infile exists
    if not os.path.isfile(args['infile']):
        print(f'File {args["infile"]} not found.')
        sys.exit(0) 

    root = tk.Tk()

    tp_inst = tpClass(root, args['infile'])

    tp_inst.mainLoop()



