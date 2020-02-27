# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 14:57:10 2020

@author: Bill
"""
import PIL
import PIL.ExifTags
import PIL.Image
import piexif
#import matplotlib

filename = 'C:/Users/Peria/Desktop/Mary-Meyer-Full-Bodied-Monkey-Puppet.jpg'
filename = 'C:/Users/Peria/Desktop/New Folder/pipette_tip_box_19.jpg'
img = PIL.Image.open(filename)
#image = PIL.Image.open('C:/Users/Peria/Desktop/New Folder/pipette_tip_box_19.jpg')

exif_initial = img._getexif()


exif = \
{
    PIL.ExifTags.TAGS[k]: v
    for k, v in exif_initial.items()
    if k in PIL.ExifTags.TAGS
}
# =============================================================================
#  PIL.ExifTags seems to be a dictionary of all or at least a lot of EXIF tags. 
#    I am not sure why they are indexed with integers.
# =============================================================================
# from puppet picture, these are the tags (of 254 total) that 
# seem relevant
# 270: 'ImageDescription',
# 306: 'DateTime',
# 315: 'Artist',
# 37510: 'UserComment',
# 40092: 'XPComment', 