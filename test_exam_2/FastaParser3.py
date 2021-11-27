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

class FastaParser3(GuiBaseClass):
    def __init__(self, root, filename = ''):
        super().__init__(root)
        
        self.filename = filename
        
        self.base_frame = self.getBaseFrame()
        
        # add menu entries
        menu_file = self.getMenu('menubar', 'File')
        menu_file.insert_command(1, label = 'Open...', command = self.fileOpen)

        # entry frame
        self.entryFrame = tk.Frame(self.base_frame)

        # entry field
        self.idEntry = tk.Entry(self.entryFrame)

        # buttons
        self.SequenceButton = tk.Button(self.entryFrame, text = 'Show Sequence', command = self.fillSequence)
        self.ExitButton = tk.Button(self.entryFrame, text = 'Exit', command = self.Exit)

        # display text
        self.displayFrame = tk.Frame(self.base_frame)
        self.displayText = tk.Text(self.displayFrame)

                
        # pack everything
        self.base_frame.pack(fill = 'both', expand = True)
        self.entryFrame.pack(side = 'top', fill = 'both')
        self.idEntry.pack(side = 'top', fill = 'x', expand = True)
        self.SequenceButton.pack(side = 'left', fill = 'x', expand = True)
        self.ExitButton.pack(side = 'right', fill = 'x', expand = True)

        self.displayFrame.pack(side ='bottom', fill ='both', expand = True)
        self.displayText.pack(fill = 'both', expand = True)

        if not self.filename:
            self.filename = tkfile.askopenfilename(initialdir = os.getcwd())

    def fileOpen(self, *args):
        pass

    def fillSequence(self, *args):
        sequence = self.idEntry.get()

        seqs = self.getSequence(self.filename, sequence)

        if not seqs:
            tk.messagebox.showerror(title = 'Error', message = 'Sequence not found.')
            pass

        i = 0        
        for value in seqs.values():
            self.displayText.insert(f'{i+1}.0', value)   
            i += 1 

    def getN(self, filename = ''):
        pat_start = re.compile(r'^>')
        pat_id = re.compile(r'(?<=^>)\S+')

        infile = open(filename, 'r')

        res = {}

        entry = ''
        seq_id = ''
        
        for line in infile:
            if re.search(pat_start, line):
                if entry:
                    res[seq_id] = len(entry)

                entry = ''
                seq_id = re.search(pat_id, line).group()
            else:
                entry = entry + line.strip('\n')

        else:
            if entry:
                res[seq_id] = len(entry)

        
        infile.close()

        return(res)

    def getSequence(self, filename = '', id = ''):
        if '*' in id:
            id = re.escape(id.strip('*'))
            pat_id = re.compile(f'\S*{id}\S+')

        else:
            pat_id = re.compile(re.escape(id))

        pat_start = re.compile(r'^>')
        # pat_header = re.compile(r'(?<=^>).+')

        res = {}
        entry = ''

        infile = open(filename, 'r')

        found = False

        i = 1
        
        for line in infile:
            if re.search(pat_start, line):
                if entry:
                    res[f'Entry {i}:'] = entry
                    entry = ''
                    i = i + 1

                if re.search(pat_id, line):
                    entry = line.strip('>')
                    found = True

                else:
                    found = False

            elif found:
                entry = entry + line
        
        infile.close()

        return(res)

    def grepSeq(filename = '', pattern = ''):
        pass

if __name__ == '__main__':
    infile_format = 'fasta'
    id_pat = r'\S+'
    alt_id_pat  = r'[A-Za-z_]+'

    parser = argparse.ArgumentParser(description = """
    Fasta utilities.
    """)
    parser.add_argument('-i', '--infile',
        help = f'Speciefies path to input file in {infile_format} format.',
        type = str)

    args = vars(parser.parse_args())

    # argument checks - infile exists
    if args['infile']:
        if not os.path.isfile(args['infile']):
            print(f'File {args["infile"]} not found.')
            sys.exit(0)  

    root = tk.Tk()

    fparser = FastaParser3(root, filename = args['infile'])

    fparser.mainLoop()

        
        