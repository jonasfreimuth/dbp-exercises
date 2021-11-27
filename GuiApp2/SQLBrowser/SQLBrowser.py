#/usr/bin/python3

import sys
import os
import argparse
import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tkfile

# add parent directory to module search path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))

from GuiBaseClass import GuiBaseClass

class SQLBrowser(GuiBaseClass):
    def __init__(self, root, filename = ''):
        """
        Initialize new Instance of SQLBrowser.
        """
        super().__init__(root)
        
        self.base_frame = self.getBaseFrame()
        self.filename = ''
        self.db_filename = filename
        self.addStatusBar()
        self.about_string = 'SQLBrowser App \nby Jonas \n2021'

        # add menu entries
        menu_file = self.getMenu('menubar', 'File')
        menu_file.insert_command(1, label = 'Open table...', command = self.fileOpen)
        menu_file.insert_command(2, label = 'Open Database...', command = self.fileOpenDatabase)

        # add widgets
        self.base_window = ttk.PanedWindow(self.base_frame, orient = 'vertical')
        self.base_window.pack(fill = 'both', expand = True)

        self.nav_cmd_window = ttk.PanedWindow(self.base_window, orient = 'horizontal')
        self.base_window.add(self.nav_cmd_window, w = 2)

        self.treeview_browser = ttk.Treeview(self.nav_cmd_window)
        self.nav_cmd_window.add(self.treeview_browser)

        self.command_text = tk.Text(self.nav_cmd_window)
        self.nav_cmd_window.add(self.command_text)

        button_execute = ttk.Button(self.base_window, text = 'Execute', command = self.executeCommands)
        self.base_window.add(button_execute, w = 1) 

        self.spread_frame = ttk.Frame(self.base_window)      
        self.base_window.add(self.spread_frame, w = 4)

        # add scrollbars
        self.vscrollbar1 = ttk.Scrollbar(self.spread_frame, orient = 'vertical')
        self.hscrollbar1 = ttk.Scrollbar(self.spread_frame, orient = 'horizontal')
        
        self.vscrollbar1.pack(side = 'right', fill = 'y')
        self.hscrollbar1.pack(side = 'bottom', fill = 'x')

        self.treeview_spreadsheet = ttk.Treeview(self.spread_frame,
         xscrollcommand = self.hscrollbar1.set,
         yscrollcommand = self.vscrollbar1.set)
        self.treeview_spreadsheet.pack(fill = 'both', expand = True)
        
        # configure scrollbars
        self.vscrollbar1.config(command = self.treeview_spreadsheet.yview)
        self.hscrollbar1.config(command = self.treeview_spreadsheet.xview)

        # add event bindings
        self.treeview_browser.bind('<<TreeviewSelect>>', self.loadTable)

        # configure spreadsheet treeview
        self.treeview_spreadsheet.column('#0', width = 0, stretch = False)

        # configure browser treeview
        # self.treeview_browser['columns'] = ('Name',)
        self.treeview_browser.heading('#0', text = 'Table Name', anchor = 'w')
        # self.treeview_browser.column('#0', width = 0, stretch = False)

        # if database is given, open it right away
        if self.db_filename:
            self.fileOpenDatabase(filename = self.db_filename)

    def fileOpen(self, filename = ''):
        """
        Opens file provided in file Dialog and display contents in spreadsheet widget.
        """ 
        if not filename:
            self.filename = tkfile.askopenfilename(initialdir = os.getcwd())

        if self.filename:
            # clean out treeview_spreadsheet
            for row in self.treeview_spreadsheet.get_children():
                self.treeview_spreadsheet.delete(row)

            # opening code adapted from DGTableView.py by Detlef Groth
            infile = open(self.filename, "r")

            i = 0

            for line in infile:
                line = line.strip('\n')
                cells = line.split("\t")
                cells = [c.strip('\"') for c in cells]

                if i == 0:
                    for j in range(1, len(cells) + 1):
                        if j == 1:
                            l = ["col" + str(j)]

                        else:
                            l.append("col" + str(j))

                    self.treeview_spreadsheet.configure(columns = l)

                    for j in range(1, len(cells) + 1):
                        col = "col" + str(j)
                        self.treeview_spreadsheet.heading(col, text = cells[j - 1])

                    i = i + 1

                else:
                    self.treeview_spreadsheet.insert("", 'end', values = cells)

    def fileOpenDatabase(self, *args, filename = ''):
        """
        Opens a database file provided in file dialog and displays tables in treeview_browser widget.
        """
        if not filename:
            self.db_filename = tkfile.askopenfilename(initialdir = os.getcwd())

        if self.db_filename:
            db = sqlite3.connect(self.db_filename)
            
            # get tablenames from database
            query = """select name from sqlite_master 
                    where type = 'table' and name not like 'sqlite_%'
                    order by 1"""

            curs = db.execute(query)
            table_names = [''.join(table) for table in curs.fetchall()] 
            
            for i in range(len(table_names)):
                self.treeview_browser.insert('', i, text = table_names[i])

            db.close()

    def loadTable(self, *args, tablename = ''):
        """ 
        Load table based on currently selected table name in treview_browser into 
        treeview spreadsheet. 
        """
        if not tablename:
            item_id = self.treeview_browser.focus()

            if not item_id:
                pass

            tablename = self.treeview_browser.item(item_id, option = 'text')
            
        # clean out treeview_spreadsheet
        for row in self.treeview_spreadsheet.get_children():
            self.treeview_spreadsheet.delete(row)

        query = f"""select * from {tablename}"""

        db = sqlite3.connect(self.db_filename)

        curs = db.execute(query)

        table_headers = [x[0] for x in curs.description]
        table_contents = curs.fetchall()

        db.close()
        
        # get headings into widget
        col_names = ['col' + str(i) for i in range(1, len(table_headers) + 1)]
        self.treeview_spreadsheet.configure(columns = col_names)

        for i in range(len(table_headers)):
            self.treeview_spreadsheet.heading(col_names[i], text = table_headers[i])

        for i in range(len(table_contents)):
            self.treeview_spreadsheet.insert('', 'end', values = table_contents[i])

    def executeCommands(self, *args, db_filename = ''):
        """
        Execute the commands in the text widgets in SQL.
        """
        command = self.command_text.get('1.0', tk.END)

        print(command)

        db = sqlite3.connect(self.db_filename)

        cur = db.execute(command)

        print(cur.fetchall()[0:10])

if __name__ == "__main__":   

    infile_format = 'sqlite3'

    parser = argparse.ArgumentParser(description = """SqlBrowser.py by Jonas. Graphic user interface for 
                                                    browsing sqlite databases.""")
    parser.add_argument('-i', '--infile',
        help = f'Speciefies path to input file in {infile_format} format.',
        type = str)        

    args = vars(parser.parse_args())

    # argument checks - infile exists
    if args['infile']:
        if not os.path.isfile(args['infile']):
            print(f'File {args["infile"]} not found.')
            sys.exit(0) 

    root = tk.Tk()
    browser = SQLBrowser(root, args['infile'])

    root.mainloop()