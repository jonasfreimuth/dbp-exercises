#!/usr/bin/python3

import os
import sys
import argparse
import re

def getN(filename = ''):
    pass

def getSequence(filename = '', seqid = ''):
    pass

def grepSeq(filename = '', pat = ''):
    pass

if __name__ == '__main__':

    infile_format = 'fasta'
    cmd_opts = ['getN', 'getSequence', 'grepSeq']
    id_pat = r'[A-Za-z0-9_]'
    aa_seq_pat  = r'[A-Zi\-]+'

    parser = argparse.ArgumentParser(description = """ """)
    parser.add_argument('-i', '--infile',
        help = f'Speciefies path to input file in {infile_format} format.',
        type = str,
        required = True)
    parser.add_argument('-d','--id',
        help = '''Identifier of either a sequence id if the command is "getSequence"
        or a regular expression to match a amino acid patterns, if the command is "grepSeq''',
        type = str)
    parser.add_argument('-c', '--command',
        help = f'Command to be executed. One of {cmd_opts}.',
        required = True)

    args = vars(parser.parse_args())

    res = ''

    # argument checks - infile exists
    if not os.path.isfile(args['infile']):
        print(f'File {args["infile"]} not found.')
        sys.exit(0)  

    # check infile type
    if not re.search(infile_format, args['infile']):        
        print(f'File {args["infile"]} not a {infile_format} file.')
        sys.exit(0)  

    # check commands
    if args['command']:
        if args['command'] not in cmd_opts:
            print(f'Error: {args["command"]} is not a valid Command.')
            sys.exit(0)

    # check what function to use
    if args['command'] in ['getSequence']:
        if not args['id']:
            print('Error ID required for command "getSequence".')
            sys.exit(0)
        if not re.match(id_pat, args['id']):
            print(f'Error: {args["id"]} is not a valid fasta Sequence ID.')
            sys.exit(0)

        else:
        #     res = getEntry(filename = args['infile'], id = args['id'])
            res = getSequence(filename=args['infile'], seqid=args['id'])

    elif args['command'] in ['grepSeq']:
        if not args['id']:
            print('Error regex pattern required for command "grepSeq".')
            sys.exit(0)
        if not re.match(aa_seq_pat, args['id']):
            print(f'Error: {args["id"]} is not a valid external sequence regular expression.')
            sys.exit(0)
        else:
            res = grepSeq(filename= args['infile'], pat = args['id'])

    elif args['command'] in ['getN']:
        if args['id']:
            print('Warning no id will be used for this command.')

        pass


    print(args)
    
    if res:
        print(res)