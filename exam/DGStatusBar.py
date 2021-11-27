# file StatusBar.py
import tkinter as tk
from tkinter import ttk
#' 
#' Links: [DGBaseGui](DGBaseGui.html) - [DGAutoScrollBar](DGAutoScrollbar.html) - 
#'  [DGBalloon](DGBalloon.html) -  [DGScrolled](DGScrolled.html) - [DGStatusBar](DGStatusBar.html) -
#'  [DGTableView](DGTableView.html) - [DGTreeView](DGTreeView.html)
#' 
#' ## NAME
#'  
#' `DGStatusBar` - widget to display status information 
#'
#' This widget provides a statusbar with Label for text message and a progressbar 
#' to display numerical progress.
#'
#' ## SYNOPSIS
#'
#' ```
#' import tkinter as tk
#' root = tk.Tk()
#' tk.Frame(root, width=200, height=100).pack()
#' status = DGStatusBar(root)
#' status.pack(side=tk.BOTTOM, fill=tk.X)
#' status.set("Connecting...")
#' status.progress(25)
#' root.mainloop()
#' ```
#' ## <a name="command">COMMAND</a>
#'
#' **DGStatusBar(master)**
#'
#' > *Arguments:*
#'
#' > - master: a parent widget or toplevel wherein `DGStatusBar` is initialized, 
#'     normally a tk.Frame or ttk.Frame widget or a Toplevel.
#'
#' > *Returns:* the statusbar widget.
#' 
#' ## METHODS

class DGStatusBar(tk.Frame):
    def __init__(self,master):
      tk.Frame.__init__(self, master)
      self.label = tk.Label(self, border=1, 
         relief='sunken', 
         anchor='w',width=50)
      self.label.pack(side='left',padx=4,pady=2,fill='x',expand=True)
      self.pb = ttk.Progressbar(self,
         length=60,mode='determinate')
      self.pb.configure(value=30)
      self.pb.pack(side='right',padx=4,pady=2)
      self.master=master

      #' **cmdName.set(format,?msg, ...?)**
      #'
      #' > Sets the message *format* into the label widget of the statusbar. Alternativly this can be a format string which will be filled with the text string given in the *msg* argument list.
      #'
      #' > *Arguments:* 
      #'  
      #' > - *format* - text message or format string.
      #'   - *msg* -  variable number of arguments used as arguments for the *format* string.
      #'
      #' > *Returns:* None

    def set(self, format, *args):
      self.label.config(text=format % args)
      self.master.update_idletasks()
      #'
      #' **cmdName.clear()**
      #'
      #' > Clears the tet message in the label subwidget.
      #'
      #' > *Arguments:* None
      #'
      #' > *Returns:* None
         
    def clear(self):
      self.label.config(text="")
      self.master.update_idletasks()
      #'
      #' **cmdName.progress(n)**
      #'
      #' > Sets the progress value in the progressbar subwidget.
      #'
      #' > *Arguments:* 
      #'  
      #' > - *n* - progress value between 0 and 100 to be displayed in the ttk.Progressbar subwidget.
      #'
      #' > *Returns:* None
         
    def progress(self,n):
      self.pb.configure(value=n)
      self.master.update_idletasks()


if __name__ == "__main__":
  import sys
  root = tk.Tk()
  root.title('DGApp')
  tk.Frame(root, width=200, height=100).pack()
  status = DGStatusBar(root)
  status.pack(side="bottom", fill="x")
  root.update()

  status.set("Connecting...")
  status.progress(25)
  #shot.shot('DGApp',root,'statusbar-python.png',ex=False)
  root.after(1000)
  status.set("Connected, logging in...")
  status.progress(50)
  root.after(1000)
  status.set("Login accepted...")
  status.progress(75)
  root.after(1000)
  status.clear()
  #sys.exit(0)
  root.mainloop()
#'  
#' ## <a name="example">Example</a>
#'
#' ```
#' import sys
#' import tkinter as tk
#' root = tk.Tk()
#' root.title('DGApp')
#' tk.Frame(root, width=200, height=100).pack()
#' status = DGStatusBar(root)
#' status.pack(side=tk.BOTTOM, fill=tk.X)
#' root.update()
#'
#' status.set("Connecting...")
#' status.progress(25)
#' root.after(1000)
#' status.set("Connected, logging in...")
#' status.progress(50)
#' root.after(1000)
#' status.set("Login accepted...")
#' status.progress(75)
#' root.after(1000)
#' status.clear()
#' root.mainloop()
#' ```  
#'  
#' ## <a name="authors">AUTHOR(S)</a>
#'
#' Detlef Groth, University of Potsdam, 2019-2020
#'
#' ## LICENSE
#'
#' MIT - License
#'  
