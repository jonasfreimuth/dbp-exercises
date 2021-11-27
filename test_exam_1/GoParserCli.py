#!/usr/env/python3

import gzip
import re
import sys
import argparse
import os.path

# class OboParse_1:
#     def __init__(self, infile):
#         pass

def getEntry (filename = '', id = ''):
    ''' Function to retreive a obo entry based on 
    id.
    '''
    # if expression if given, convert it to compiled regex
    id_reg = re.compile(f'id: {id}')
    empty = re.compile(r'^$')

    res = ''
    found = False

    infile = gzip.open(filename, 'rt')

    for line in infile:
        if re.search(id_reg, line):
            found = True

        if found:
            res = res+line

            if re.search(empty, line):
                break

    infile.close()

    return(res)

def getXref(filename = '', id = ''):
    pass

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

        if args['command'] == 'getEntry':
            res = getEntry(filename = args['infile'], id = args['id'])

    elif args['command'] in ['getXref']:
        if not re.match(r'[a-z]+:[:A-Z:]+_[0-9]+', args['id']):
            print(f'Error: {args["id"]} is not a valid external identifier.')
            sys.exit(0)

    print(res)
        
