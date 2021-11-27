#!/usr/env/python3

import ast
import csv
import sqlite3
import argparse
import re

class SqlUtils():
    """
    Class implementing various SQLite methods.
    """
    def row2list(self, row, quote = '\"', sep = '\t'):
        """
        Method forconverting a row read from a table file into a list.
        Defaults are for tab separated files.
        """
        # get rid of trailing new line (would also remove leading new line,
        # but we also don't want those)
        row = row.strip('\n')

        # split into list along occurrences of sep
        row = row.split(sep)

        # remove quotation characters around entries
        row = [x.strip(quote) for x in row]

        return(row)

    def scrub(self, string):
        """
        Method scrubbing out potentially malicous characters from
        SQLite parameters.
        """
        return(re.sub(r'[\"\']', '', string))


    def dataType(self, string):
        """
        Method allowing type parsing from a string containing only the value whose type is
        queried. 
        Answer adapted from user 'the wolf' on 
        https://stackoverflow.com/questions/10261141/determine-type-of-value-from-a-string-in-python
        """

        string = string.strip()
        if len(string) == 0: 
            raise ValueError('Unable to determine type of empty string.')

        try:
            t = ast.literal_eval(string)

        except ValueError:
            return 'TEXT'

        except SyntaxError:
            return 'TEXT'

        else:
            if type(t) in [int, float, bool]:
                if t in set((True,False)):
                    return 'TEXT'

                if type(t) is int:
                    return 'INT'

                if type(t) is float:
                    return 'REAL'

            else:
                return 'TEXT' 

    def csv2sqlite3(self, csvfile, sqlite3file, tablename, delim = ',', quote = '\"'):
        """
        Method for reading a table from a text file into a specified SQLite db.
        """
        # sanitize tablename
        tablename = self.scrub(tablename)

        with open(csvfile) as infile:
            # get column names
            header_raw = next(infile)
            header = self.row2list(header_raw, sep = delim, quote = quote)

            # get column types
            row_1_raw = next(infile)
            row_1 = self.row2list(row_1_raw, sep = delim, quote = quote)

            types = [None] * len(row_1)

            for i in range(len(row_1)):
                types[i] = self.dataType(row_1[i])

        print(header)
        print(row_1)
        print(types)

        # create string for create table command
        create_tab = f'CREATE TABLE {tablename} ('

        # add columns to command
        for i in range(len(header)):
            col_comm = f'{self.scrub(header[i])} {self.scrub(types[i])}'
            if not i == len(header) - 1:
                col_comm = col_comm + ', '
            create_tab = create_tab + col_comm

        create_tab = create_tab + ');'

        print(create_tab)

        db = sqlite3.connect(sqlite3file)
        cur = db.cursor()

        # execute table creation
        cur.execute(create_tab)

        # create insert template
        header_string = self.scrub(','.join(header))
        insert = f'INSERT INTO {tablename} ({header_string}) VALUES ('

        # read in rest of table and add into SQLite table
        with open(csvfile) as infile:
            # skip first line
            next(infile)
            for row in infile:
                row = self.row2list(row)

                # workaround: quote all elements in row
                row  = [f'"{x}"' for x in row]

                # CAUTION NO SCRUBBING HERE
                row_string = ', '.join(row)
                
                cmd_string = insert + row_string + ')'

                print(cmd_string)

                cur.execute(cmd_string)

        db.commit()

        db.close()
        

if __name__ == "__main__":
    # import tkinter.filedialog as tkfile
    # SQLUtils.csv2sqlite3(csvfile = '../../../')
    parser = argparse.ArgumentParser(
        description = 'Utility functions for working with SQLite databases')
    parser.add_argument('-i', '--infile',
        help = 'Data file in any tabular format to be parsed. (Make sure separator and quotes are set appropriat to file type.)',
        required = True,
        type = str)
    parser.add_argument('-n', '--tablename',
        help = 'Name to be given to table in data base.',
        required = True
    )
    parser.add_argument('-d','--database',
        help = '''Give file name for SQLite database this table will be added to (will create new one if nonexistent).''',
        required = True,
        type = str)
    parser.add_argument('-q', '--quotechar',
        help = 'Specify character used for quoting entries. (Currently unused)',
        default = '\"',
        type = str,
        required = False)
    parser.add_argument('-s', '--separator',
        help = 'Specify character used for separating entries. When supplying special characters, use double escapes (i.e. \\\\t)',
        default = '\t',
        required = False)
            
    args = vars(parser.parse_args())

    util = SqlUtils()
    print(args['separator'])
    util.csv2sqlite3(csvfile = args['infile'], sqlite3file = args['database'], tablename = args['tablename'], delim = args['separator'], quote = args['quotechar'])



