#!/usr/bin/python3

import gzip
import re
import sys
import argparse
import os.path
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as tkfile

# add GuiApp2 dir to module search path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'../GuiApp2'))

from GuiBaseClass import GuiBaseClass

class GoParserGui(GuiBaseClass):
    def __init__(self, root, filename = ''):
        super().__init__(root)

        self.base_frame = self.getBaseFrame()
        self.filename = filename

        # add menu entries
        menu_file = self.getMenu('menubar', 'File')
        menu_file.insert_command(1, label = 'Open...', command = self.fileOpen)

        # entry frame
        self.entryFrame = tk.Frame(self.base_frame)

        # entry field
        self.idEntry = tk.Entry(self.entryFrame)

        # buttons
        self.ParentButton = tk.Button(self.entryFrame, text = 'Show Parents', command = self.fillParent)
        self.XrefButton = tk.Button(self.entryFrame, text = 'Show Xref', command = self.fillXref)

        # panedwindow
        self.GoPW = ttk.PanedWindow(self.base_frame, orient = 'horizontal')

        # GoID listbox
        self.GoIDListbox = tk.Listbox(self.GoPW)
        self.GoIDListbox.bind('<<ListboxSelect>>', self.fillEntry)

        # Entry Text
        self.EntryTextbox = tk.Text(self.GoPW)

        # pack everything
        self.base_frame.pack()
        self.entryFrame.pack(side = 'top', expand = True, fill = 'both')
        self.idEntry.pack(side = 'top', fill = 'x')
        self.ParentButton.pack(side = 'bottom', fill = 'x')
        self.XrefButton.pack(side = 'bottom', fill = 'x')
        self.GoPW.pack(side = 'bottom', fill = 'both')

        self.GoPW.add(self.GoIDListbox)
        self.GoPW.add(self.EntryTextbox)


    def fileOpen(self, *args):
        """
        Saves filename chosen in file dialog.
        """ 
        self.filename = tkfile.askopenfilename(initialdir = os.getcwd())

    def fillXref(self, *args):       
        """
        Method using the getXref method to retrieve GoIds from the 
        given XrefId in the idEntry widget. Retrieved ids are placed in the
        GoIdListbox widget after the widget has been cleared of previous entries.
        """ 
        id = self.idEntry.get()

        xrefs = self.getXref(self.filename, id)

        # delete previous entries
        self.GoIDListbox.delete(1, tk.END)

        for i in range(len(xrefs)):
            self.GoIDListbox.insert(i+1, xrefs[i])

    def fillParent(self, *args):
        """
        Method using the getParent method to retrieve parent GoIds from the 
        given GoId in the idEntry widget. Retrieved ids are placed in the
        GoIdListbox widget after the widget has been cleared of previous entries.
        """
        id = self.idEntry.get()

        parents = self.getParent(self.filename, id)

        # delete previous entries
        self.GoIDListbox.delete(1, tk.END)

        for i in range(len(parents)):
            self.GoIDListbox.insert(i+1, parents[i])

    def fillEntry(self, *args):
        """
        Method searching for the entry matching a GoId in the GoIDListbox. 
        The entry is then inserted into the EntryTextbox.
        """
        idx = self.GoIDListbox.curselection()

        GoID = ''.join(self.GoIDListbox.get(idx, idx))

        print(GoID)

        entry = self.getEntry(self.filename, GoID)

        # delete previous entries
        self.EntryTextbox.delete('1.0', tk.END)

        print(entry)

        for i in range(len(entry)):
            self.EntryTextbox.insert(f'{i+1}.0', entry[i])

    def getEntry(self, filename = '', id = ''):
        ''' 
        Function to retreive a GO entry based on 
        id.
        '''
        if not re.match(r'GO:[0-9]{7}', id):
            print(f'{id} in not a valid GO Id.')
            pass

        # if expression if given, convert it to compiled regex
        id_reg = re.compile(f'id: {id}')
        empty = re.compile(r'^$')

        res = []
        found = False

        infile = gzip.open(filename, 'rt')

        for line in infile:
            if re.search(id_reg, line):
                found = True

            if found:
                res.append(line)

                if re.search(empty, line):
                    break

        infile.close()

        return(res)

    def getParent(self, filename = '', id = ''):
        """
        Method finding parent GoIds for a given GoId.
        """
        if not re.match(r'GO:[0-9]{7}', id):
            print(f'{id} in not a valid GO Id.')
            pass

        id_reg = re.compile(f'^id: {id}')
        par_reg = re.compile(r'^is_a: .+')
        par_id_reg = re.compile(r'GO:[0-9]{7}')
        empty = re.compile(r'^$')

        res = []
        found = False

        infile = gzip.open(filename, 'rt')

        for line in infile:
            if re.search(id_reg, line):
                found = True

            if found:
                if re.search(par_reg, line):
                    print(line)
                    res.append(re.search(par_id_reg, line).group())

                if re.search(empty, line):
                    break

        infile.close()

        return(res)

    def getXref(self, filename = '', id = ''):
        """
        Method extracting GoIds belonging to a certain Xref id.
        """
        if not re.match(r'\S+:\S+', id):
            print(f'{id} is not a valid Xref string.')
            pass

        xref_reg = re.compile(f'^xref: {id}')
        id_reg = re.compile(r'^id: ')
        end_reg = re.compile(r'^id: (?!GO:[0-9]{7})')
        go_id_reg = re.compile(r'GO:[0-9]{7}')

        res = []

        infile = gzip.open(filename, 'rt')

        for line in infile:
            if re.search(end_reg, line):
                break

            if re.search(id_reg, line):
                go_id = re.search(go_id_reg, line).group()

            if re.search(xref_reg, line):
                res.append(go_id)

        infile.close()

        if res:
            return(res)
        else:
            print('No Xref found.')
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description = 'Utility functions for working with GeneOntology data')
    parser.add_argument('-i','--infile',
        help = 'Gene ontology file in .gz (gzip) format to be parsed.',
        type = str)
    # parser.add_argument('-d','--id',
    #     help = '''Gene ontology identifier of form GO:xxxxxxx (x being numbers)''')
    # parser.add_argument('-c', '--command',
    #     help = 'Command to be executed. One of getEntry, getParent, getXref.',
    #     required = True)

    args = vars(parser.parse_args())

    # argument checks
    if args['infile']:
        if not os.path.isfile(args['infile']):
            print(f'File {args["infile"]} not found.')
            sys.exit(0)

    # if args['command']:
    #     if args['command'] not in ['getEntry', 'getParent', 'getXref']:
    #         print(f'Error: {args["command"]} is not a valid Command.')
    #         sys.exit(0)

    # if args['command'] in ['getEntry', 'getParent']:
    #     if not re.match(r'GO:[0-9]{7}$', args['id']):
    #         print(f'Error: {args["id"]} is not a valid GO Id.')
    #         sys.exit(0)

    #     if args['command'] == 'getEntry':
    #         res = getEntry(filename = args['infile'], id = args['id'])

    # elif args['command'] in ['getXref']:
    #     if not re.match(r'[a-z]+:[:A-Z:]+_[0-9]+', args['id']):
    #         print(f'Error: {args["id"]} is not a valid external identifier.')
    #         sys.exit(0)

    root = tk.Tk()

    GoParse = GoParserGui(root, args['infile'])

    GoParse.mainLoop()


        
