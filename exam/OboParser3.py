#!/usr/bin/python3

import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog as tkfile
import tkinter.ttk as ttk
import sys
import os
import re
import argparse
from OboParser2 import *
from GuiBaseClass import *

# # add location of GuiBaseClass
# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../GuiApp2/'))

class OboParser3(GuiBaseClass):
    def __init__(self, root, filenames = ''):
        super().__init__(root)
        
        self.filenames = filenames
        
        self.base_frame = self.getBaseFrame()
        
        # add menu entries
        menu_file = self.getMenu('menubar', 'File')
        menu_file.insert_command(1, label = 'Open...', command = self.fileOpen)

        # action frame
        self.actionLabframe = ttk.LabelFrame(self.base_frame, text = 'Actions')

        # buttons
        self.fileOpenButton = tk.Button(self.actionLabframe, text = 'Open Files', command = self.fileOpen)
        self.ShowStatsButton = tk.Button(self.actionLabframe, text = 'Show Statistics', command = self.fillStats)
        self.ExitButton = tk.Button(self.actionLabframe, text = 'Exit', command = self.Exit)

        # display frame
        self.dispFrame = tk.Frame(self.base_frame)
        self.displayText = tk.Text(self.dispFrame,
            width = 50, height = 50)
        self.infoLabel = tk.Label(self.dispFrame, text = 'Click Open File')
                
        # pack everything
        self.base_frame.pack(fill = 'both', expand = True)
        self.actionLabframe.pack(side = 'top', fill = 'both')

        # pack buttons
        self.fileOpenButton.pack(expand = True, fill = 'x')
        self.ShowStatsButton.pack(side = 'bottom', fill = 'x', expand = True)
        self.ExitButton.pack(side = 'bottom', fill = 'x', expand = True)

        # display frame
        self.dispFrame.pack(expand = True, fill = 'both', side = 'top')
        self.displayText.pack(expand = True, fill = 'both', side = 'top')
        self.infoLabel.pack(expand = False, fill = 'x', side = 'bottom')

        if not self.filenames:
            self.fileOpen()
        else:
            self.infoLabel.configure(text = ', '.join([os.path.splitext(filename)[0] for filename in self.filenames]))
        
    def fileOpen(self, *args):
        """
        Saves filename chosen in file dialog.
        """
        self.filenames = tkfile.askopenfilenames(initialdir = os.getcwd(), title = 'Select files')

        self.infoLabel.configure(text = ', '.join([os.path.splitext(filename)[0] for filename in self.filenames]))

        # self.loadNbPages()

    # def loadNbPages(self, *args):
    #     if not self.filenames:
    #         pass

    #     # give each file a notebook
    #     self.filenb.forget(0)

    #     self.filetxt = {}

    #     for filename in self.filenames:

    #         # extract date from filename
    #         date = re.search(r'[0-9]+-[0-9]+-[0-9]+(?=.gz$)', filename).group()

    #         self.filetxt[date] = tk.Text(self.filenb)
    #         self.filenb.add(self.filetxt[date], text = date)

    def fillStats(self, *args):
        stats = getGOStats(self.filenames)
                
        for i in range(len(stats)):
            self.displayText.insert(f'{i+1}.0', stats[i])

if __name__ == '__main__':

    cmd_opts = ['getGOStats', 'getECInfo']
    namespace_pat = r'[a-z_]+'
    go_id_pat = r'GO:[0-9]{7}$'
    xref_id_pat = r'[a-zA-Z]+:\S+'

    parser = argparse.ArgumentParser(
        description = 'Utility functions for multiple gene ontology obo files.')
    parser.add_argument('-i','--infiles',
        help = 'A number of gzipped input files to work with.', default = '',
        nargs = '*') 
    parser.add_argument('-g','--gui',
        help = 'Start gui application', default = False,
        action = "store_true",
        required = False)   
    parser.add_argument('-c','--command',
        help = f'Command to be executed on the obo files. One of {cmd_opts}', default = '', nargs = '+')

    args = vars(parser.parse_args())

    print(args)
        
    if not bool(args['gui']):
        # check if each file exists and is valid
        for filename in args['infiles']:
            if not os.path.isfile(filename):
                print(f'File {filename} not found.')
                sys.exit(0)
                
            elif not re.search(r'\.gz$', filename):
                print(f'Error: {filename} is not a gz file.')
                sys.exit(0)


        # check if commands are valid
        if args['command']:
            for command in args['command']:
                if command not in cmd_opts:
                    print(f'Error: {command} is not a valid Command.')
                    sys.exit(0)

        # initialise results dict
        res = {}

        # check which command to execute    
        for command in args['command']:
            if command in cmd_opts[0]:
                res['getGOStats'] = getGOStats(args['infiles'])
                
            elif command in cmd_opts[1]:
                res['getECInfo'] = getECInfo(args['infiles'])


        for func, result in res.items():
            print(func)
            [print(entry) for entry in result]

    else:

        ne_files = []    
        
        # check if each file exists and is valid
        for filename in args['infiles']:
            if not os.path.isfile(filename) or not re.search(r'\.gz$', filename):
                ne_files.append(filename)
                args['infiles'].remove(filename)

        root = tk.Tk()

        if ne_files:

            tk.messagebox.showwarning(master = root, title = 'Files not found', message = f'File(s) {", ".join(ne_files)} not found, proceeding without them.')
            
        app = OboParser3(root, args['infiles'])
        app.mainLoop()
        