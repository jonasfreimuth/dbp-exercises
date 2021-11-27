#!/usr/bin/python3

import os
import sys
import argparse
import re

def getN(filename = ''):
    pass

def getSequence(filename = '', id = ''):
    pass

def grepSeq(filename = '', pattern = ''):
    pass

if __name__ == '__main__':

    infile_format = 'fasta'
    cmd_opts = ['getN', 'getSequence', 'grepSeq']
    id_pat = r'\S+'
    alt_id_pat  = r'[A-Za-z_]+'

    parser = argparse.ArgumentParser(description = """
    Fasta utilities.
    """)
    parser.add_argument('-i', '--infile',
        help = f'Speciefies path to input file in {infile_format} format.',
        type = str)
    parser.add_argument('-d','--id',
        help = '''Sequence identifier or regular expression pattern for amino acid sequence.''',
        type = str)
    parser.add_argument('-c', '--command',
        help = f'Command to be executed. One of {cmd_opts}.',
        required = True)

    args = vars(parser.parse_args())

    # argument checks - infile exists
    if not os.path.isfile(args['infile']):
        print(f'File {args["infile"]} not found.')
        sys.exit(0)    

    if args['command']:
        if args['command'] not in cmd_opts:
            print(f'Error: {args["command"]} is not a valid Command.')
            sys.exit(0)

    if args['command'] in ['getSequence']:
        if not re.match(id_pat, args['id']):
            print(f'Error: {args["id"]} is not a valid GO Id.')
            sys.exit(0)

        res = getSequence(filename = args['infile'], id = args['id'])

    elif args['command'] in ['grepSeq']:
        if not re.match(alt_id_pat, args['id']):
            print(f'Error: {args["id"]} is not a valid regular expression.')
            sys.exit(0)

        res = grepSeq(filename = args['infile'], pattern = args['id'])

    elif args['command'] == 'getN':
        if args['id']:
            print('Warning: id given but not used in command "getN".')

        res = getN(filename = args['infile'])

    print(args)