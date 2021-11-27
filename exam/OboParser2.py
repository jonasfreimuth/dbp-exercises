#!/usr/bin/python3

import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog as tkfile
import tkinter.ttk as ttk
import gzip
import sys
import os
import re
import argparse

# add location of GuiBaseClass
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../GuiApp2/'))

from GuiBaseClass import GuiBaseClass

def getGOStats(filenames, *args):

    # term_pat = re.compile(r'^[Term]')
    end_pat = re.compile(r'^$')
    namespace_line_pat = re.compile(r'^namespace: ')
    obs_line_pat = re.compile(r'^is_obsolete:')

    namespace_pat = re.compile(r'(?<=^namespace: )[a-z_]+')

    res = []

    for filename in filenames:
        # extract date from filename
        date = re.search(r'[0-9]+-[0-9]+-[0-9]+(?=.gz$)', filename).group()

        infile = gzip.open(filename, 'rt')

        nmspc = ''

        is_obs = False
        nmspc_count = {}

        for line in infile:
            if re.search(namespace_line_pat, line):
                nmspc = re.search(namespace_pat, line).group()

                is_obs = False

                if not nmspc in nmspc_count.keys():
                    nmspc_count[nmspc] = {'actual':0, 'obsolete':0}

            if re.search(obs_line_pat, line):
                is_obs = True

            if re.search(end_pat, line):

                if not nmspc:
                    continue

                if is_obs:
                    nmspc_count[nmspc]['obsolete'] += 1
                else:                    
                    nmspc_count[nmspc]['actual'] += 1            
        
        infile.close()
        

        print(nmspc_count)

        for nmspc in nmspc_count.keys():
            for key in nmspc_count[nmspc].keys():
                line = '\t'.join([str(date), str(nmspc_count[nmspc][key]), nmspc, key]) + '\n'
                res.append(line)

    return(res)

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
        [print(entry) for entry in result]


