# -*- coding: utf-8 -*-
# -*- python=3.8.x
"""
Created on Tue Mar  8 14:48:15 2022

@author: Patrick Parkinson
----
Edited 04/07/2023 - AK

Changed config path since relative path didn't work (why?)
"""

import ajiledriver as aj
from dmd_control import DMD
import os
import numpy as np

global IMAGE_ID

def load_list_images() -> list:
    patterns = []
    os.chdir("./patterns/")
    for file in os.listdir():
        # Check whether file is in text format or not
        if file.endswith(".pickle"):
            patterns.append(file)
    return patterns

def add_image_to_seq(npImage : np.array):
    IMAGE_ID += 1
    myImage = aj.Image(IMAGE_ID)
    # load the NumPy image into the Image object and convert it to DMD 4500 format
    myImage.ReadFromMemory(npImage, 8, aj.ROW_MAJOR_ORDER, aj.DMD_4500_DEVICE_TYPE)

def create_pattern_images():
    a=0

def pre_main():
    create_pattern_images()
    #board_images = pickle.load(open("left_side.p","rb"))
    # Insert images
    dmd.insert_images(board_images)
   
    

def main():
    print(load_list_images())


if __name__ == "__main__":
    global dmd
    IMAGE_ID = 0
    dmd = DMD()
    main()
