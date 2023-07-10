# -*- coding: utf-8 -*-
# -*- python=3.8.x
"""
Created on 06/07/2023

Another method of creating images (patterns).
The goal is to create a full-size image with small data size.

@author: Alex Kedziora
"""

#import cv2
import numpy as np
import pickle
import ajiledriver as aj

# create an image with ID 1
#cv2.rectangle(npImage, (0, 0), (100, 100), 255)


def save_image(image : np.array, file_name : str):
    """Saves an array as a pickle file in the given relative path"""
    with open("./patterns/"+ file_name +".pickle","wb") as handle:
        pickle.dump(image, handle, protocol=pickle.HIGHEST_PROTOCOL)

def one_side(side : str = "left") -> np.array:
    """Flip all mirrors to one side """
    if(side == "left"):
        npImage = np.ones(shape=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX, 1), dtype=np.uint8)*255
    else:
        npImage = np.zeros(shape=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX, 1), dtype=np.uint8)

    return npImage

def horizontal_50_50() -> np.array:
    """Flip first row of mirrors to left, second row to right..."""
    npImage = np.zeros(shape=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX, 1), dtype=np.uint8)
    # npImage[::][::2] = 255
    for im in npImage:
        im[::2] = 255
    return npImage

def vertical_50_50() -> np.array:
    """Flip first column of mirrors to left, second column to right..."""
    npImage = np.ones(shape=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX, 1), dtype=np.uint8)*255
    npImage[::2] = npImage[::2]*0
    return npImage
    
def checkers() -> np.array:
    # First pixel is 255, second 0, third 255....
    npImage = np.zeros(shape=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX, 1), dtype=np.uint8)
    for i in range(len(npImage)):
        for j in range(len(npImage[i])):
            if((i+j)%2 ==0):
                npImage[i][j] = 255
    return npImage

def create_all_patterns():
    """Create and save all defined patterns"""
    save_image(one_side(),"left_side")
    save_image(one_side("right"),"right_side")
    save_image(horizontal_50_50(),"horizontal_50_50")
    save_image(vertical_50_50(),"vertical_50_50")
    save_image(checkers(),"checkers")
