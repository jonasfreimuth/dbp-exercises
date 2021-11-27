#!/usr/bin/python3

import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk
import sys
import os

# add location of DGWidgets
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../teachers/dgroth/DGPyWidgets/'))

import DGStatusBar as dgsbar

class GuiBaseClass():
    def __init__(self, root):
        self.root = root
        self.root.option_add('*tearOff', False)
        self.sbar = dgsbar.DGStatusBar(root)
        self.about_string = 'Base Gui App \nby Jonas \n2021'
        self.askOnExit = tk.BooleanVar()
        self.askOnExit.set(1)

        # menu construction
        self.menu = dict()
        self.menubar = tk.Menu(root)
        
        menu_file = tk.Menu(self.menubar)

        menu_file.add_separator()
        menu_file.add_command(label = 'Exit', command = lambda: self.Exit(ask = self.askOnExit.get()))
        
        menu_opts = tk.Menu(menu_file)
        menu_opts.add_checkbutton(label = 'Ask on Exit', variable = self.askOnExit)

        menu_file.insert_cascade(1, menu = menu_opts, label = 'Options')

        self.menubar.add_cascade(menu = menu_file, label = 'File')

        menu_help = tk.Menu(self.menubar)

        menu_help.add_command(label = 'About', command = lambda: self.About())

        self.menubar.add_cascade(menu = menu_help, label = 'Help')

        self.menu['menubar'] = self.menubar
        self.menu['File'] = menu_file
        self.menu['Help'] = menu_help


        # adding a base frame
        self.base_frame = ttk.Frame(self.root)
        self.base_frame.pack(fill = 'both', expand = True)
                
        self.root.config(menu = self.menubar)

    def mainLoop(self):
        ''' 
        Initialises main loop of app if called.
        '''
        self.root.mainloop()

    def getBaseFrame(self):
        ''' Returns frame of object. '''
        return(self.base_frame)

    def getMenu(self, rootname, name):
        '''
        Returns submenu of rootname with label 'name' for modification.
        If no menu with label 'name' is found it will create one before the last entry of 
        rootname.
        '''
        if name in self.menu.keys():
            return(self.menu[name])
        else:
            last_root_index = self.menu[rootname].index('end')
            self.menu[name] = tk.Menu(self.menu[rootname])
            self.menu[rootname].insert_cascade(last_root_index, menu = self.menu[name], label = name)
            return(self.menu[name])

    def Exit(self, ask = True):
        ''' 
        Wrapper around root.destroy(). If ask = True (default), the user
        will be presented with a messagebox and the option not to quit.
        '''
        if ask == True:
            exit = tk.messagebox.askyesno('Exit', message='Do you want to exit the application?')
        else:
            exit = True

        if exit:
            self.root.destroy()

    def About(self):
        '''
        Display about string in messagebox.
        '''
        tk.messagebox.showinfo(title = 'About', message = self.about_string)

    def addStatusBar(self):
        '''
        Display status bar at the bottom of the root window.
        '''
        self.sbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.sbar.progress(0)
        self.root.update()

    def setStatusBarMessage(self, message):
        '''
        Change the status bar message.
        '''
        self.sbar.set(message)
        self.root.update()

    def setStatusBarProgValue(self, value):
        '''
        Change the status bar progress. value should be between 0 and 100.
        '''
        self.sbar.progress(value)
        self.root.update   

    def testStatusBar(self):
        """
        Test method to let the progressbar do something.
        """
        self.setStatusBarMessage('Starting...')

        self.root.after(500)

        self.setStatusBarMessage('Finding Holes...')
        self.setStatusBarProgValue(20)

        self.root.after(2000)

        self.setStatusBarMessage('Closing Holes...')
        self.setStatusBarProgValue(50)

        self.root.after(3000)

        self.setStatusBarMessage('Dang, missed one')
        self.setStatusBarProgValue(45)

        self.root.after(500)

        self.setStatusBarMessage('Ok done, let\' have a beer!')
        self.setStatusBarProgValue(50)

        self.root.after(1000)

        self.setStatusBarMessage('That\'s a nice days work done!')
        self.setStatusBarProgValue(100)

if __name__ == "__main__":
    root = tk.Tk()
    b_app = GuiBaseClass(root)

    b_app_base_frame = b_app.getBaseFrame()

    label1 = ttk.Label(b_app_base_frame, text = 'Your ad here.')
    label1.pack()

    menu_edit = b_app.getMenu('menubar', 'Edit')
    menu_edit.add_command(label = 'Copy', command = lambda: print('Copy'))

    menu_file = b_app.getMenu('menubar', 'File')
    menu_file.insert_command(index = 1, label = 'Test me', command = lambda: print('Hello there!'))
    
    menu_edit = b_app.getMenu('menubar', 'File')
    menu_file.insert_command(index = 1, label = 'Run Progbar', command = lambda: b_app.testStatusBar())

    b_app.addStatusBar()

    b_app.mainLoop()