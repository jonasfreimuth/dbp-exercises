#!/usr/bin/python3

import GuiBaseClass as gb
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tkfile
import tkinter.colorchooser
import tkinter.messagebox
import os
import sys
import argparse
import random as rd
import datetime

class GuiLearner(gb.GuiBaseClass):
    def __init__(self, root, filename = ''):
        super().__init__(root)
        self.base_frame = self.getBaseFrame()
        self.filename = filename
        self.addStatusBar()
        self.about_string = 'GuiLearner App \nby Jonas \nUsing DGWidgets by Detlef Groth \n2021'
        self.entries = dict()
        self.left_selected = ''
        self.left_selected_idx = None
        self.bg = 'white'

        # add menu entries
        menu_file = self.getMenu('menubar', 'File')
        menu_file.insert_command(1, label = 'New File', command = lambda: self.fileNew())
        menu_file.insert_command(2, label = 'Open...', command = lambda: self.fileOpen())
        menu_file.insert_command(3, label = 'Save', command = lambda: self.fileSave())
        menu_file.insert_command(4, label = 'Save as...', command = lambda: self.fileSaveAs())

        menu_edit = self.getMenu('menubar', 'Edit')
        menu_edit.insert_command(1, label = 'Set txtbox color...', command = lambda: self.setBgColor())
        menu_edit.insert_command(2, label = 'Set text color...', command = lambda: self.setTxtColor())

        # add scrollbar
        self.vscrollbar1 = ttk.Scrollbar(self.base_frame, orient = 'vertical')
        self.hscrollbar1 = ttk.Scrollbar(self.base_frame, orient = 'horizontal')

        # add listboxes
        self.listbox_left = tk.Listbox(self.base_frame,
        # height = 50, width = 80,
         xscrollcommand = self.hscrollbar1.set,
         yscrollcommand = self.vscrollbar1.set)
        self.listbox_right = tk.Listbox(self.base_frame,
        # height = 50, width = 80,
         xscrollcommand = self.hscrollbar1.set,
         yscrollcommand = self.vscrollbar1.set)

        # connect scrollbars
        def yview_both(*args):
            self.listbox_left.yview(*args)
            self.listbox_right.yview(*args)

        def xview_both(*args):
                self.listbox_left.xview(*args)
                self.listbox_right.xview(*args)

        self.vscrollbar1.config(command = yview_both)
        self.hscrollbar1.config(command = xview_both)

        # add selection eventbindings
        self.listbox_left.bind('<<ListboxSelect>>', self.left_item_select)
        self.listbox_right.bind('<<ListboxSelect>>', self.right_item_select)

        # pack everything
        self.vscrollbar1.pack(side = 'right', anchor = 'w', fill = 'y')
        self.hscrollbar1.pack(side = 'bottom', anchor = 'n', fill = 'x')
        
        self.listbox_right.pack(side = 'right', fill = 'both', expand = True)
        self.listbox_left.pack(side = 'left', fill = 'both', expand = True)

        # if filename is given, load that file
        if filename:
            self.fileOpen(filename = filename)


    def fileNew(self):
        """
        Initialize a new file in the program.
        """
        pass

    def fileOpen(self, n_lines = 10, filename = ''):
        """
        Open a file dialog, save filename.
        """
        if not filename:
            self.filename = tkfile.askopenfilename(initialdir = os.getcwd())
            # self.filename = '../../../teachers/dgroth/data/deu2eng.tab'
            file = open(self.filename, 'r')

        else: 
            file = open(filename)

        # get number of lines
        lines = []
        for line in file:
            lines.append(line)

        file.close()

        # delete what was in listboxes previously
        self.listbox_left.delete(1, self.listbox_left.size())
        self.listbox_right.delete(1, self.listbox_right.size())

        file_length = len(lines)

        # generate random indices of lines
        rand_idcs = rd.sample(range(file_length), n_lines)

        for i in range(file_length):
            if i in rand_idcs:
                line = lines[i]
                line = line.split()
                self.entries[line[0]] = line[1]

        for key, value in self.entries.items():
            self.listbox_left.insert(rd.randint(0, n_lines - 1), key)
            self.listbox_right.insert(rd.randint(0, n_lines - 1), value)

        self.start_time = datetime.datetime.now()
        self.penal_seconds = 0

    def left_item_select(self, *args):
        """
        Handler for when a new item in left box is selected. 
        Changes colour of selection and displays message in progbar.
        """
        print(*args)

        # reset colouring of previous index
        if self.left_selected_idx:
            self.listbox_left.itemconfig(self.left_selected_idx, bg = self.bg)

        idx = self.listbox_left.curselection()

        print(f'left index: {idx}')

        if idx:
            # mark current selection
            self.listbox_left.itemconfig(idx, bg = 'blue')

            self.setStatusBarMessage('Now select the matching entry in the right window.')

            self.left_selected = self.listbox_left.get(idx)
            self.left_selected_idx = idx

    def right_item_select(self, *args):
        """
        Handler for when a new item in the right box is selected.
        Checks if an item is selected in the right box and if yes,
        whether both match. If they match, it then removes both entries.
        If no entries are left, it displays the time since a file was opened last.
        """
        print(*args)

        if self.left_selected:            
            idx = self.listbox_right.curselection()

            print(f'Right index {idx}')

            if idx:
                right_entry = ''.join(self.listbox_right.get(idx, idx))

                print(right_entry)
                print(self.entries[self.left_selected])

                if right_entry == self.entries[self.left_selected]:
                    self.setStatusBarMessage('Correct! Onto the next item!')

                    self.listbox_right.delete(idx, idx)
                    self.listbox_left.delete(self.left_selected_idx, self.left_selected_idx)

                    self.left_selected = ''
                    self.left_selected_idx = None
                
                else:
                    self.setStatusBarMessage('Wrong, dummy! You\'re getting docked 10s for that! Haha!')

                    self.penal_seconds += 10

                    # self.clearSelection()

                print(f'Entries remaining: {self.listbox_right.size()}')
        
        else:
            self.setStatusBarMessage('You need to select an item on the right first!')

        if self.listbox_right.size() == 0:
            
            tot_time = (datetime.datetime.now() - self.start_time).total_seconds()

            msg = f'You took {round(tot_time)}s to find all pairs.\nDo you want to try another round with the same language?' 

            answer = tk.messagebox.askyesnocancel(title = 'All Done!', message = msg)

            if answer == 'Yes':
                self.fileOpen()

            elif answer == 'No':
                self.Exit(ask = False)

            else:
                self.setStatusBarMessage('To start over, load a tab file with File -> Open...')

    def clearSelection(self):
        """
        Clear selection of both left and right listbox.
        """
        
        if self.left_selected_idx:
            self.listbox_left.itemconfig(self.left_selected_idx, bg = self.bg)

        self.left_selected = ''
        self.left_selected_idx = None

        self.root.after(1000)
        self.setStatusBarMessage('Start over, pick a word from the left.')

        
    def fileSave(self):
        """
        Save the current file to its path.
        """
        lines = self.listbox_left.get(1)

        file = open(self.filename, 'w')

        file.write(lines)

        file.close()

    def fileSaveAs(self):
        """
        Open a file dialog to save the file in a user specified path.
        """
        pass

    def setBgColor(self):
        """
        Open color chooser dialog set color of listbox_left.
        """
        color = tk.colorchooser.askcolor(title = 'Choose background color')[1]

        # make sure we didn't cancel and try to set the color to none
        if color:
            self.listbox_left.configure(bg = color)
            self.listbox_right.configure(bg = color)

            self.bg = color

    def setTxtColor(self):
        """
        Open color chooser dialog set color of text in listbox_left.
        """
        color = tk.colorchooser.askcolor(title = 'Choose text color')[1]

        # make sure we didn't cancel and try to set the color to none
        if color:
            self.listbox_left.configure(fg = color)    

if __name__ == "__main__":

    ap = argparse.ArgumentParser(description = 'Learning application with Gui')
    ap.add_argument('-i', '--infile',
        help = '''Start application with this file already loaded.
                 Should be a two clumn tab delimited file.''',
                 default = '')    

    args = vars(ap.parse_args())

    root = tk.Tk()
    learner = GuiLearner(root, args['infile'])
    root.title("Learner")

    # learner_base_frame = learner.getBaseFrame()

    # label_1 = ttk.Label(learner_base_frame, text = 'We\'re learning things!')
    # label_1.pack()

    menu_file = learner.getMenu('menubar', 'File')
    menu_file.insert_command(index = 1, label = 'Run Progbar', command = lambda: learner.testStatusBar())

    learner.mainLoop()