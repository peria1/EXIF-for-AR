# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 08:35:43 2020

@author: Bill
"""
# import PIL
# # import PIL.ExifTags
# import PIL.Image
import glob
import piexif
import piexif.helper

import tkinter as tk
from tkinter.filedialog import FileDialog
# import tkinter.filedialog

from PIL import ImageTk,Image  

class Application(tk.Frame):
    def __init__(self):
        
    #         root = tk.Tk()
    # root.focus_force()
    # root.withdraw() # we don't want a full GUI, so keep the root window 
    #                 #  from appearing
    # pathname = tk.filedialog.askdirectory(title=title, initialdir = initialdir)
    # return pathname
        input_directory = 'C:/Users/peria/Desktop/work/Brent Lab/git-repo/EXIF-for-AR'

        # input_directory = tkinter.filedialog.askdirectory()
        dir_to_process = input_directory + '/' + '*.jpg'
        self.image_iter = iter(sorted(glob.glob(dir_to_process)))
        
        self.root = tk.Tk()
        pad=3 # Why? 
        geom=("{0}x{1}+0+0".format(
            self.root.winfo_screenwidth()-pad, \
                self.root.winfo_screenheight()-pad))
        self.root.geometry(geom)
        
        tk.Frame.__init__(self, self.root)
        
        self.iuc = piexif.ExifIFD.UserComment 
        
        self.create_widgets()

    def create_widgets(self):
        self.root.bind('<Return>', self.parse)
        self.grid()
 
        self.current_comment = ''
        self.entry = tk.Entry(self, width=80, font='Calibri 14')
        self.entry.insert(0, self.current_comment)
        
        self.canvas = tk.Canvas(self,  width=1024, height=768)
        self.load_new_image()

        self.submit = tk.Button(self, text="Submit")
        self.submit.bind('<Button-1>', self.parse)

        self.canvas.grid()
        self.entry.grid()
        self.submit.grid()

    def parse(self, event):
        # print("You clicked?")
        new_comment = self.entry.get()
        user_comment = piexif.helper.UserComment.dump(new_comment)
        self.exif_dict["Exif"][self.iuc] = user_comment
        piexif.insert(piexif.dump(self.exif_dict), self.current_file)
        
        self.entry.insert(0, '')
        self.load_new_image()

    def load_new_image(self):
        try:
            self.current_file = next(self.image_iter)
            self.img = ImageTk.PhotoImage(Image.open(self.current_file)) 
            self.exif_dict = piexif.load(self.current_file) 
            try:
                comm_obj = self.exif_dict["Exif"][self.iuc]
                self.current_comment = piexif.helper.UserComment.load(comm_obj)
                self.entry.delete(0, tk.END)
                self.entry.insert(0, self.current_comment)
            except KeyError:
                print('No Comment')
                self.current_comment = ''
            self.canvas.create_image(400, 400,\
                                      image=self.img) 
        except StopIteration:
            self.root.destroy()
            print('No more files')
            
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

