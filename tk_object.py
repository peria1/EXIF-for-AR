# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 08:35:43 2020

@author: Bill
"""
# import PIL
# # import PIL.ExifTags
# import PIL.Image
import piexif
import piexif.helper

import tkinter as tk
from PIL import ImageTk,Image  

class Application(tk.Frame):
    def __init__(self):
        
        
        self.root = tk.Tk()
        self.root.geometry("1024x768")

        tk.Frame.__init__(self, self.root)
        self.create_widgets()

    def create_widgets(self):
        self.root.bind('<Return>', self.parse)
        self.grid()
        
        self.img = ImageTk.PhotoImage(Image.open("puppet2.jpg")) 
        self.canvas = tk.Canvas(self)
        self.canvas.create_image(20, 20, image=self.img) 
        self.canvas.grid()

        self.entry = tk.Entry(self)
        self.entry.grid()

        self.submit = tk.Button(self, text="Submit")
        self.submit.bind('<Button-1>', self.parse)
        self.submit.grid()

    def parse(self, event):
        print("You clicked?")

    def start(self):
        self.root.mainloop()

if __name__=="__main__":
    Application().start()

# iuc = piexif.ExifIFD.UserComment # the index o of UserComment, i.e. 37510
# exif_dict = piexif.load(filename) # part binary still

# def submit(text):
#     new_comment = text
#     user_comment = piexif.helper.UserComment.dump(new_comment)
#     exif_dict["Exif"][iuc] = user_comment
#     piexif.insert(piexif.dump(exif_dict), filename)


# axbox = plt.axes([0.1, 0.05, 1, 0.5])
# comm_obj = exif_dict["Exif"][piexif.ExifIFD.UserComment]
# current_comment = piexif.helper.UserComment.load(comm_obj)
# text_box = TextBox(axbox,'', initial= current_comment)
# text_box.on_submit(submit)

