#!/usr/bin/python3

import os
import sys
import argparse
import re

if __name__ == '__main__':

    infile_format = ''
    cmd_opts = []
    id_pat = r''
    alt_id_pat  = r''

    parser = argparse.ArgumentParser(description = """ """)
    parser.add_argument('-i', '--infile',
        help = f'Speciefies path to input file in {infile_format} format.',
        type = str)
    parser.add_argument('-d','--id',
        help = '''Identifier XXX''',
        type = str)
    parser.add_argument('-c', '--command',
        help = f'Command to be executed. One of {cmd_opts}.',
        required = True)
    parser.add_argument('-o', '--option',
        help = 'Set option XXX',
        action = 'store true')

    args = vars(parser.parse_args())

    # argument checks - infile exists
    if not os.path.isfile(args['infile']):
        print(f'File {args["infile"]} not found.')
        sys.exit(0)    

    if args['command']:
        if args['command'] not in cmd_opts:
            print(f'Error: {args["command"]} is not a valid Command.')
            sys.exit(0)

    if args['command'] in ['XXX']:
        if not re.match(id_pat, args['id']):
            print(f'Error: {args["id"]} is not a valid GO Id.')
            sys.exit(0)

        # if args['command'] == 'getEntry':
        #     res = getEntry(filename = args['infile'], id = args['id'])

    elif args['command'] in ['XXX']:
        if not re.match(alt_id_pat, args['id']):
            print(f'Error: {args["id"]} is not a valid external identifier.')
            sys.exit(0)

    print(args)