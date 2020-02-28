# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 07:36:19 2020

@author: Bill
"""
import tkinter as tk

root= tk.Tk()

# canvas1 = tk.Canvas(root, width = 800, height = 300)
canvas1 = tk.Canvas(root)
canvas1.pack()

entry1 = tk.Entry(root) 
canvas1.create_window(200, 140, window=entry1)
# canvas1.create_window(200, 140, 1000, 440) # not correct args
# 

def getSquareRoot ():  
    x1 = entry1.get()
    
    label1 = tk.Label(root, text= float(x1)**0.5)
    canvas1.create_window(200, 230, window=label1)
    
button1 = tk.Button(text='Get the Square Root', command=getSquareRoot)
canvas1.create_window(200, 180, window=button1)

root.mainloop()
