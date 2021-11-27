#!/usr/bin/python3

import os
import sys
import argparse
import re

def getN(filename = ''):
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

def getSequence(filename = '', id = ''):
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
        if not args['id']:
            print(f'Error no id provided, necessary for command getSequence.')
            sys.exit(0)

        if not re.match(id_pat, args['id']):
            print(f'Error: {args["id"]} is not a valid GO Id.')
            sys.exit(0)

        res = getSequence(filename = args['infile'], id = args['id'])

    elif args['command'] in ['grepSeq']:
        if not args['id']:
            print(f'Error no id provided, necessary for command getSequence.')
            sys.exit(0)

        if not re.match(alt_id_pat, args['id']):
            print(f'Error: {args["id"]} is not a valid regular expression.')
            sys.exit(0)

        res = grepSeq(filename = args['infile'], pattern = args['id'])

    elif args['command'] == 'getN':
        if args['id']:
            print('Warning: id given but not used in command "getN".')

        res = getN(filename = args['infile'])

    for key, value in res.items():
        print(key, '\n', value)

    print(args)