# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 14:57:10 2020

@author: Bill
"""
import PIL
# import PIL.ExifTags
import PIL.Image
import piexif
import piexif.helper
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox

filename = './Puppet2.jpg'
# filename = './pipette_tip_box_17.jpg'
img = PIL.Image.open(filename)

exif_initial = img._getexif()


# exif = \
# {
#     PIL.ExifTags.TAGS[k]: v
#     for k, v in exif_initial.items()
#     if k in PIL.ExifTags.TAGS
# }
# # =============================================================================
#  PIL.ExifTags seems to be a dictionary of all or at least a lot of EXIF tags. 
#    I am not sure why they are indexed with integers.
# ============================================================================
# from puppet picture, these are the tags (of 254 total) that 
# seem relevant
# 270: 'ImageDescription',
# 306: 'DateTime',
# 315: 'Artist',
# 37510: 'UserComment',
# 40092: 'XPComment', 

iuc = piexif.ExifIFD.UserComment # the index o of UserComment, i.e. 37510
exif_dict = piexif.load(filename) # part binary still
text_comment = "What a fooking mess"
user_comment = piexif.helper.UserComment.dump(text_comment)
exif_dict["Exif"][iuc] = user_comment
exif_bytes = piexif.dump(exif_dict)

user_comment_chk = piexif.helper.UserComment.load(exif_dict["Exif"][iuc])


def submit(text):
    curr_comment = piexif.helper.UserComment.load(exif_dict["Exif"][iuc])
    new_comment = curr_comment + text
    user_comment = piexif.helper.UserComment.dump(new_comment)
    exif_dict["Exif"][iuc] = user_comment



axbox = plt.axes([0.1, 0.05, 0.8, 0.075])
text_box = TextBox(axbox, 'Evaluate', initial='enter your comments')
text_box.on_submit(submit)



