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

import os
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import sqlite3

import phonebook_main
import phonebook_gui

def center_window (self, w, h): # pass in the tkinter frame (master) reference, the w, and h
    # get user's screen width and height
    screen_width = self.master.winfo_screenwidth ()
    screen_height = self.master.winfo_screenheight ()
    # calculate x and y coordinates to paint the app in the center of the user's screen
    x = int ((screen_width / 2) - (w / 2))
    y = int ((screen_height / 2) - (h / 2))

    centerGeo = self.master.geometry ("{} x {} + {} + {}".format (w, h, x, y))
    return centerGeo

# Catches if the user clicks on the window upper right 'X' to ensure they want to close the program
def ask_quit (self):
    if messagebox.askokcancel ("Exit program", "Okay to exit application?"):
        # Closes app
        self.master.destroy ()
        os._exit (0)

#==============================================================================
def create_db (self):
    connection = sqlite3.connect ("db_phonebook.db")
    with connection:
        cursor = connection.cursor ()
        cursor.execute ("CREATE TABLE if not exists tbl_phonebook( \
            ID INTEGER PRIMARY KEY AUTOINCREMENT, \
            col_fname TEXT, \
            col_lname TEXT, \
            col_fullname TEXT, \
            col_phone TEXT, \
            col_email TEXT \
            );")
        connection.commit ()
    connection.close ()
    first_run (self)

def first_run (self):
    connection = sqlite3.connect ("db_phonebook.db")
    with connection:
        cursor = connection.cursor ()
        cursor, count = count_records (cursor)
        if count < 1:
            cursor.execute ("""INSERT INTO tbl_phonebook (col_fname, col_lname, col_fullname, col_phone, col_email) VALUES (?, ?, ?, ?, ?)""", ("John", "Doe", "John Doe", "111-111-1111", "jdoe@email.com"))
            connection.commit ()
    connection.close ()

def count_records (cursor):
    count = ""
    cursor.execute ("""SELECT COUNT(*) FROM tbl_phonebook""")
    count = cursor.fetchone ()[0]
    return cursor, count

# Selects an item in ListBox
def onSelect (self, event):
    # Calling the event is the self.lstList1 widget
    varList = event.widget
    select = varList.curselection ()[0]
    value = varList.get (select)
    connection = sqlite3.connect ("db_phonebook.db")
    with connection:
        cursor = connection.cursor ()
        cursor.execute ("""SELECT col_fname, col_lname, col_phone, col_email FROM tbl_phonebook WHERE col_fullname = (?)""", [value])
        varBody = cursor.fetchall ()
        for data in varBody:
            self.txt_fname.delete (0, END)
            self.txt_fname.insert (0, data [0])
            self.txt_lname.delete (0, END)
            self.txt_lname.insert (0, data [1])
            self.txt_phone.delete (0, END)
            self.txt_phone.insert (0, data [2])
            self.txt_email.delete (0, END)
            self.txt_email.insert (0, data [3])

def addToList (self):
    var_fname = self.txt_fname.get ()
    var_lname = self.txt_lname.get ()
    
    # Normalizes data to keep it consistent in the database
    var_fname = var_fname.strip () # Removes blank spaces before and after the user's entry
    var_lname = var_lname.strip () # Ensures the first character in each word is capitalized
    var_fname = var_fname.title ()
    var_lname = var_lname.title ()
    var_fullname = ("{} {}".format (var_fname, var_lname)) # Combines the normalized names into a full name
    print ("var_fullname: {}".format (var_fullname))
    var_phone = self.txt_phone.get ().strip ()
    var_email = self.txt_email.get ().strip ()

    if not "@" or not "." in var_email:
        print ("Incorrect email format! Please double check your entry.")
    
    if (len (var_fname) > 0) and (len (var_lname) > 0) and (len (var_phone) > 0) and (len (var_email) > 0):
        connection = sqlite3.connect ("db_phonebook.db")
        with connection:
            cursor = connection.cursor ()
            # Checks the db for existance of the fullname, if so the app alerts the user and disregards request
            cursor.execute ("""SELECT COUNT (col_fullname) FROM tbl_phonebook WHERE col_fullname = '{}'""".format (var_fullname))
            count = cursor.fetchone ()[0]
            chkName = count

            if chkName == 0:
                # If chkName is 0 there is no existance of the fullname and we can add new data
                print ("chkName: {}".format (chkName))
                cursor.execute ("""INSERT INTO tbl_phonebook (col_fname, col_lname, col_fullname, col_phone, col_email) VALUES (?, ?, ?, ?, ?)""", (var_fname, var_lname, var_fullname, var_phone, var_email))
                self.lstList1.insert (END, var_fullname) # Updates listbox with the new fullname
                onClear (self) # Calls the function to clear all of the textboxes

            else:
                messagebox.showerror ("Missing Text Error", "Please ensure that there is data in all four fields.")

def onDelete (self):
    var_select = self.lstList1.get (self.lstList1.curselection()) # Listbox's selected value
    connection = sqlite3.connect ("db_phonebook.db")
    with connection:
        cursor = connection.cursor()
        # Checks count to ensure this entry is not the last record in the db
        # Cannot delete the last record or the app will throw an error
        cursor.execute ("""SELECT COUNT (*) FROM tbl_phonebook""")
        count = cursor.fetchone ()[0]

        if count > 1:
            confirm = messagebox.askokcancel ("Delete Confirmation", "All information associated with, ({}) \nwill be permenatly deleted from the database. \n\nProceed with the deletion request?".format (var_select))

            if confirm:
                connection = sqlite3.connect ("db_phonebook.db")
                with connection:
                    cursor = connection.cursor ()
                    cursor.execute ("""DELETE FROM tbl_phonebook WHERE col_fullname = '{}'""".format (var_select))
                onDeleted (self)
                connection.commit ()

        else:
            confirm = messagebox.showerror ("Last Record Error", "({}) is the last record in the database and cannot be deleted at this time. \n\nPlease add another record first then attempt to delete again ({}).".format (var_select, var_select))
        
    connection.close ()

def onDeleted (self):
    # Clears the text in these textboxes
    self.txt_fname.delete (0, END)
    self.txt_lname.delete (0, END)
    self.txt_phone.delete (0, END)
    self.txt_email.delete (0, END)

    # onRefresh (self) update the listbox with the changes
    try:
        index = self.lstList1.curselection ()[0]
        self.lstList1.delete (index)

    except IndexError:
        pass

def onClear (self):
    # Clears the text in these textboxes
    self.txt_fname.delete (0, END)
    self.txt_lname.delete (0, END)
    self.txt_phone.delete (0, END)
    self.txt_email.delete (0, END)

def onRefresh (self):
    # Populate the listbox, coinciding with the db
    self.lstList1.delete (0, END)
    connection = sqlite3.connect ("db_phonebook.db")
    with connection:
        cursor = connection.cursor ()
        cursor.execute ("""SELECT COUNT (*) FROM tbl_phonebook""")
        count = cursor.fetchone ()[0]
        i = 0

        while i < count:
            cursor.execute ("""SELECT col_fullname FROM tbl_phonebook""")
            varList = cursor.fetchall ()[i]
            for item in varList:
                self.lstList1.insert (0, str (item))
                i = i + 1

    connection.close ()

def onUpdate (self):
    try:
        var_select = self.lstList1.curselection ()[0] # Index of the list selection
        var_value = self.lstList1.get (var_select) # List selection's text value
    except:
        messagebox.showinfo ("Missing selection", "No name was selected from the list box. \nCancelling the Update request.")
        return
    
    # The user will only be allowed to update changes for phone and email
    # For name changes, the user will need to delete the entire record and start over.
    var_phone = self.txt_phone.get ().strip () # Normalizes the data to maintain db integrity
    var_email = self.txt_email.get ().strip ()
    if (len (var_phone) > 0) and (len (var_email) > 0):
        connection = sqlite3.connect ("db_phonebook.db")
        with connection:
            cursor = connection.cursor ()
            # Count records to see if the user's changes are already in
            # the db (no changes are needed)
            cursor.execute ("""SELECT COUNT (col_phone) FROM tbl_phonebook WHERE col_phone = '{}'""".format (var_phone))
            count = cursor.fetchone ()[0]
            print (count)
            cursor.execute ("""SELECT COUNT (col_email) FROM tbl_phonebook WHERE col_email = '{}'""".format (var_email))
            count2 = cursor.fetchone ()[0]
            print (count2)

            # If proposed changes are not already in the db, proceed
            if count == 0 or count2 == 0:
                response = messagebox.askokcancel ("Update Request", "The following changes ({}) and ({}) will be implemented for ({}). \n\nProceed with the update request?".format (var_phone, var_email, var_value))
                print (response)
                if response:
                    with connection:
                        cursor = connection.cursor ()
                        cursor.execute ("""UPDATE tbl_phonebook SET col_phone = '{0}, col_email = '{1}' WHERE col_fullname = '{2}'""".format (var_phone, var_email, var_value))
                        onClear (self)
                        connection.commit ()
                else:
                    messagebox.showinfo ("Cancel request", "No changes have been made to ({}).".format (var_value))
            else:
                messagebox.showinfo ("No changes detected", "Both ({}) and ({}) \nalready exist in the database for this name. \n\nYour update request has been cancelled.".format (var_phone, var_email))
            onClear (self)
        connection.close ()
    else:
        messagebox.showerror ("Missing information", "Please select a name from the list. \nThen edit the phone or email information.")
    onClear (self)

if __name__ == "__main__":
    pass