###############################################################################
# Python Ver:   3.12.1
#
# Author:       Meg Lee
#
# Purpose:      Demo of a Phonebook Application written in Python.          #               Demonstration of OOP, Tkinter GUI module, using Tkinter Parent
#               and Child relationships.
#
# Tested OS:    This code was written and tested to work with Windows 11.
###############################################################################

from tkinter import *
import tkinter as tk
from tkinter import messagebox

import phonebook_gui
import phonebook_func

class ParentWindow (Frame):
    def __init__ (self, master, *args, **kwargs):
        Frame.__init__ (self, master, *args, **kwargs)

        # Defines the master frame configuration
        self.master = master
        self.master.minsize (500, 300) # (Height, Width)
        self.master.maxsize (500, 300)

        # CenterWindow method will center the app on the user's screen
        phonebook_func.center_window (self, 500, 300)
        self.master.title ("The Tkinter Phonebook Demo")
        self.master.configure (bg = "#F0F0F0")

        # Protocol method is a tkinter built-in method to catch
        # if the user clicks the upper corner, "X" on Windows OS.
        # Separate window appears asking the user if they want to quit.
        self.master.protocol ("WM_DELETE_WINDOW", lambda: phonebook_func.ask_quit (self))
        arg = self.master

        # Load in the GUI widgets from a seperate module
        phonebook_gui.load_gui (self)

        # Instantiates the Tkinter menu dropdown object
        # This menu appears at the top of the app window
        menubar = Menu (self.master)
        filemenu = Menu (menubar, tearoff = 0)
        filemenu.add_separator ()
        filemenu.add_command (label = "Exit", underline = 1, accelerator = "Ctrl+Q", command = lambda: phonebook_func.ask_quit (self))
        menubar.add_cascade (label = "File", underline = 0, menu = filemenu)
        helpmenu = Menu (menubar, tearoff = 0) # defines the specific drop down column
        helpmenu.add_separator ()
        helpmenu.add_command (label = "How to use this program")
        helpmenu.add_separator ()
        helpmenu.add_command (label = "About This Phonebook Demo") # add_command is a child menubar item of the add_cascade parent item
        menubar.add_cascade (label = "Help", menu = helpmenu) # add_cascade is a parent menubar item (visible heading)

        self.master.config (menu = menubar, borderwidth = "1")


if __name__ == "__main__":
    root = tk.TK ()
    App = ParentWindow (root)
    root.mainloop ()