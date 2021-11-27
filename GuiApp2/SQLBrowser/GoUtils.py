#!/usr/env/python3

import gzip
import re
import sys
import argparse
import os.path

class GoUtils():
    """
    Class facilityting work with Gene Ontology files. 
    """
    def __init__(self, filename):
        self.filename = filename

    def gonames(self, outfile = '', colnames = ('GoId', 'GoName', 'GoNamespace'),
                overwrite = False):

        if outfile:
            if not overwrite and os.path.isfile(outfile):
                msg = (f'Action won\'t complete as {outfile} exists and overwriting is disabled.\n' +
                        '\tEnable by providing \"-w\" option.')

                raise FileExistsError(msg)

        infile = gzip.open(self.filename, 'rt')

        if outfile:
            outfile = open(outfile, 'w')

        id_pat = re.compile(r'^id: (GO:[0-9]{7})')
        name_pat = re.compile(r'^name: (.+)')
        nmspace_pat = re.compile(r'^namespace: (.+)')
        # stop_pat = re.compile(r'^id: negatively_regulates')
       
        if outfile:
            # write colnames
            # ensure colnames are quoted
            outfile.write('\t'.join(['\"' + x + '\"' for x in colnames]) + '\n')

        for line in infile:
            ent_id = re.search(id_pat, line)
            ent_name = re.search(name_pat, line)
            ent_nmspace = re.search(nmspace_pat, line)

            if ent_id:
                id_val = ent_id.group(1)
            
            elif ent_name:
                name_val = ent_name.group(1)

            elif ent_nmspace:
                namespace_val = ent_nmspace.group(1)

                val_list = [id_val, name_val, namespace_val]

                if outfile:
                    outfile.write('\t'.join(['\"' + x + '\"' for x in val_list]) + '\n')
                
                else:
                    print('\t'.join(val_list))

        infile.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description = 'Utility functions for working with GeneOntology data')
    parser.add_argument('-i','--infile',
        help = 'Gene ontology file in .gz (gzip) format to be parsed.',
        type = str)
    parser.add_argument('-o','--outfile',
        help = '''Specifiy output file for parsed GO file, in .tab (tab delimited table) format.
                Whether existing an existing file of that name will be overwritten is determined by
                the -w option. 
                If no file is given, output will be printed.''',
        required = False,
        type = str)
    parser.add_argument('-w', '--overwrite',
        help = 'When given, an existing output file will be overwritten.',
        action = 'store_true')

    args = vars(parser.parse_args())

    util = GoUtils(args['infile'])

    util.gonames(outfile = args['outfile'], overwrite = args['overwrite'])
