# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 08:35:43 2020

@author: Bill
"""
import glob
import piexif
import piexif.helper
import platform as platf
import tkinter as tk
from tkinter import filedialog, simpledialog

from PIL import ImageTk,Image  

class EXIF_Editor(tk.Frame):
    def __init__(self):
        # Hocus pocus...bring Tk to life...
        self.root = tk.Tk() 
        top = tk.Toplevel(self.root)
        top.withdraw()  # ...in secret....
        
        #  ...but do not use root for a temporary window, i.e. 
        #       the one in which the user picks a diresctory. In
        #       other words, I need parent=top, not parent=root, for
        #       the directory picker. 
        input_directory = \
            filedialog.askdirectory(parent=top, \
                                            title='Choose folder')
        
        # ARGH! piexif can only deal with jpeg and tiff. 
        bad_img_types = ['png','gif']
        for t in bad_img_types:
            if glob.glob(input_directory + '/*.'+ t):
                print('You have some',t,'images...')
                print('Please convert them to jpeg.')

        
        img_types = ['jpg', 'tif']
        images_to_process = []
        for t in img_types:
            images_to_process.append(glob.glob(input_directory + '/*.'+ t))        
        # Smash the list of lists into a plain old list. 
        images_to_process = \
            [item for il in images_to_process for item in il]
        self.image_list = sorted(images_to_process) 
        # Make an iterable out of all the image pathnames to use
        #  when processing individual images. 
        self.image_iter = self.get_image_list_iter()
       
        #
        #  Let user enter anything that applies to all images in folder.
        top = tk.Toplevel(self.root)
        top.withdraw()
        universal_comment = \
            simpledialog.askstring('Universal Comment',\
                                   'Enter any text that applies to all images in this folder',\
                                       parent=top)
        self.universal_comment = None
        if len(universal_comment) > 0:
            self.universal_comment = universal_comment
    

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
 
        self.label = tk.Label(self.root, text='')
 
        self.current_comment = ''
        self.entry = tk.Entry(self, width=80, font='Calibri 14')
        self.entry.insert(0, self.current_comment)
        
        self.canvas = tk.Canvas(self,  width=1024, height=768)
        self.load_new_image()

        self.submit = tk.Button(self, text="Submit")
        self.submit.bind('<Button-1>', self.parse)
 
        self.label.grid()
        self.canvas.grid()
        self.entry.grid()
        self.submit.grid()
        
    def get_image_list_iter(self):
        return(iter(self.image_list))
        
        
    def parse(self, event):
        # what the user typed, plain text
        full_comment = self.entry.get() 
        # if self.universal_comment:
        #     full_comment = self.universal_comment + ': ' + new_comment
        # else:
        #     full_comment = new_comment
            
        # full comment, dumped to binary
        full_comment_dump = piexif.helper.UserComment.dump(full_comment)
        
        # binary dump put into EXIF  in RAM
        self.exif_dict["Exif"][self.iuc] = full_comment_dump
        
        # modified EXIF written to disk
        piexif.insert(piexif.dump(self.exif_dict), self.current_file)
        
        # zap the user-typed text, and move on to next
        # self.entry.insert(0, '')
        self.load_new_image()

    def load_new_image(self):
        try:
            self.current_file = next(self.image_iter)
            # self.label.text = self.current_file.split(self.get_slash())[-1]
            self.img = ImageTk.PhotoImage(Image.open(self.current_file)) 
            self.exif_dict = piexif.load(self.current_file) 
            try:
                comm_obj = self.exif_dict["Exif"][self.iuc]
                pre_existing_comment = piexif.helper.UserComment.load(comm_obj)
            except KeyError:
                print('No Comment')
                pre_existing_comment = ''
            self.entry.delete(0, tk.END)
            
            existing_comment = None
            if self.universal_comment:
                existing_comment = \
                    self.universal_comment + ': ' + pre_existing_comment
            else:
                existing_comment = pre_existing_comment

            self.entry.insert(0, existing_comment)
 
               
            self.canvas.create_image(400, 400,\
                                      image=self.img) 
        except StopIteration:
            self.root.destroy()
            print('No more files')
            
    def start(self):
        self.root.mainloop()
 
    def get_slash(self): # OMG I hate computers sometimes. 
        if platf.system() == 'Windows':
            slash = '\\' 
        else:
            slash = '/'
        return slash

class Notepad(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.text = tk.Text(self, wrap="word")
        self.vsb = tk.Scrollbar(self, orient="vertical", comman=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
    
if __name__=="__main__":
    EXIF_Editor().start()

