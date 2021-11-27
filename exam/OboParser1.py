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

def getGOStats(filenames, *args):
    return({'getGOStats':', '.join(filenames)})

def getECInfo(filenames, *args):
    return({'getGOStats':', '.join(filenames)})  

if __name__ == '__main__':

    cmd_opts = ['getGOStats', 'getECInfo']
    namespace_pat = r'[a-z_]+'
    go_id_pat = r'GO:[0-9]{7}$'
    xref_id_pat = r'[a-zA-Z]+:\S+'

    parser = argparse.ArgumentParser(
        description = 'Utility functions for multiple gene ontology obo files.')
    parser.add_argument('-i','--infiles',
        help = 'A number of gzipped input files to work with.', default = '',
        required = True, nargs = '+')
    parser.add_argument('-c','--command',
        help = f'Command to be executed on the obo files. One of {cmd_opts}', default = '',
        required = True, nargs = '+')

    args = vars(parser.parse_args())
    print(args)

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
        [print('\t' + ident + '\n\t\t' + entry) for ident, entry in result.items()]


