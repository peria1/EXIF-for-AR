# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 06:27:20 2020
https://stackoverflow.com/questions/36315156/how-do-i-run-multiple-tkinter-windows-simultaneously-in-python

The only changes I will make here are comments/notes to help me understand this. 

@author: Bill
"""

# import Tkinter as tk
import tkinter as tk

class Notepad(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.text = tk.Text(self, wrap="word")
        self.vsb = tk.Scrollbar(self, orient="vertical", comman=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)

def main():
    root = tk.Tk()
    Notepad(root).pack(fill="both", expand=True)
    for i in range(5):
        top = tk.Toplevel(root)
        # We can open as many windows having a new Toplevel parent
        #   as we want...
        Notepad(top).pack(fill="both", expand=True)

    #  ...and then tell root to poll them for user events. 
    root.mainloop()

if __name__ == "__main__":
    main()