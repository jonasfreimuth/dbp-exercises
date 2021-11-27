#!/usr/env/python3

import gzip
import re
import sys
import argparse
import os.path

# class OboParse_1:
#     def __init__(self, infile):
#         pass

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description = 'Utility functions for working with GeneOntology data')
    parser.add_argument('-i','--infile',
        help = 'Gene ontology file in .gz (gzip) format to be parsed.',
        type = str,
        required = True)
    parser.add_argument('-d','--id',
        help = '''Gene ontology identifier of form GO:xxxxxxx (x being numbers)''')
    parser.add_argument('-c', '--command',
        help = 'Command to be executed. One of getEntry, getParent, getXref.',
        required = True)

    args = vars(parser.parse_args())

    # argument checks
    if not os.path.isfile(args['infile']):
        print(f'File {args["infile"]} not found.')
        sys.exit(0)

    if args['command']:
        if args['command'] not in ['getEntry', 'getParent', 'getXref']:
            print(f'Error: {args["command"]} is not a valid Command.')
            sys.exit(0)

    if args['command'] in ['getEntry', 'getParent']:
        if not re.match(r'GO:[0-9]{7}$', args['id']):
            print(f'Error: {args["id"]} is not a valid GO Id.')
            sys.exit(0)

    elif args['command'] in ['getXref']:
        if not re.match(r'[a-z]+:[:A-Z:]+_[0-9]+', args['id']):
            print(f'Error: {args["id"]} is not a valid external identifier.')
            sys.exit(0)

    print('works')
        
