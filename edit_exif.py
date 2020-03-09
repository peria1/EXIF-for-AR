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
        bad_img_types = ['png','gif','webp','psd','raw','arw','cr2','nrw',\
                         'k25','bmp','dib','ind','indd','indt','jp2','j2k',\
                             'jpf','jpx','jpm','mj2','heif','heic']
        for t in bad_img_types:
            if glob.glob(input_directory + '/*.'+ t):
                print('You have some',t,'images...')
                print('Please convert them to jpeg.')
                print()

        
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

    def create_widgets(self):   # TODO add s quit button, and gracefully exit
        self.root.bind('<Return>', self.parse)
        self.grid(columnspan=2)
        
        font = 'Calibri 14'
 
        self.labtext = tk.StringVar()
        self.label = tk.Label(self.root, textvariable=self.labtext, \
                              font=font, anchor=tk.N)
 
        self.current_comment = ''
        self.entry = tk.Entry(self, width=80, font=font)
        self.entry.insert(0, self.current_comment)
        
        self.canvas = tk.Canvas(self,  width=1024, height=768)
        self.load_new_image()

        self.prev = tk.Button(self, text='Prev')
        self.prev.bind('<Button-1>', self.prev_image)


        self.erase = tk.Button(self, text='Erase all comments')
        self.erase.bind('<Button-1>', self.erase_all)
        
        self.enough = tk.Button(self, text="Enough, already!")
        self.enough.bind('<Button-1>', self.byebye)
 
        self.label.grid(row=0,columnspan=2)
        self.canvas.grid(row=1,column=0, columnspan=2)
        self.entry.grid(row=2,columnspan=2)
        self.enough.grid(row=3,column=0)
        self.erase.grid(row=3,column=1)
        
        
    def get_image_list_iter(self):
        return(iter(self.image_list))
                
    def parse(self, event):
        # what the user typed, plain text
        full_comment = self.entry.get() 
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
            self.labtext.set(self.current_file.split(self.get_slash())[-1])

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
            print('No more files')
            self.byebye(None)
            
    def erase_all(self, event):
        top = tk.Toplevel(self.root)
        top.withdraw()
        must_be_yes = \
            simpledialog.askstring('Whoa, there!',\
                                   'Are you sure you want to erase all comments?',\
                                       parent=top)

        if must_be_yes == 'yes':
            imglist = self.get_image_list_iter()
            for img in imglist:
                self.exif_dict = piexif.load(img)
                blank_dump = piexif.helper.UserComment.dump('')
                self.exif_dict["Exif"][self.iuc] = blank_dump
                piexif.insert(piexif.dump(self.exif_dict), img)
            self.byebye(event)

    def byebye(self, event):
        self.root.destroy()
    
    def start(self):
        self.root.mainloop()
 
    def get_slash(self): # OMG I hate computers sometimes. 
        if platf.system() == 'Windows':
            slash = '\\' 
        else:
            slash = '/'
        return slash

    def prev_image(self, event):
        pass

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

