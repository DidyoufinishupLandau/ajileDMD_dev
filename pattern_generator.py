# -*- coding: utf-8 -*-
# -*- python=3.8.x
"""
Created on 06/07/2023

Another method of creating images (patterns).
The goal is to create a full-size image with small data size.

@author: Alex Kedziora
"""

from __future__ import annotations ## fixes "images: list[]" issue with list[]
import cv2
import numpy as np
import pickle
import ajiledriver as aj

def save_image(image : np.array, file_name : str):
    """Saves an array as a pickle file in the given relative path"""
    with open("./patterns/"+ file_name +".pickle","wb") as handle:
        pickle.dump(image, handle, protocol=pickle.HIGHEST_PROTOCOL)

def save_image_list(image : list(np.array), file_name : str):
    """Saves an array as a pickle file in the given relative path"""
    with open("./patterns/lists/"+ file_name +".pickle","wb") as handle:
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

def random_50_50() -> np.array:
    # Generate numbers from 0 to 1 sorted as an array (then multiply by 255)
    npImage = np.random.randint(2,size=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX,1), dtype=np.uint8)*255
    return npImage

def random_1() -> np.array:
    npImage = np.zeros(shape=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX, 1), dtype=np.uint8)
    a = np.random.randint(0, aj.DMD_IMAGE_HEIGHT_MAX)
    b = np.random.randint(0, aj.DMD_IMAGE_WIDTH_MAX)
    npImage[a][b] = 255
    return npImage


"""
Definitions of list of images
DMD has size 1140 x 912 (height (rows) x width (columns)) which factorize to 2*2*3*5*19 x 2*2*2*2*3*19
"""

def list_a_a(a:int) -> list[np.array]:
    # Divide DMD into squares of a x a pixels
    # Create arrays of only one square on
    # 1140*912/a^2 images in total => ~ 1140*912/a^2 kB of data
    images: list = []
    npImage: np.array
    for col in range(int(aj.DMD_IMAGE_WIDTH_MAX/a)):
        for wid in range(int(aj.DMD_IMAGE_HEIGHT_MAX/a)):
            npImage = np.zeros(shape=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX, 1), dtype=np.uint8) 
            cv2.rectangle(npImage,(wid*a,col*a),((wid+1)*a-1,(col+1)*a-1),255)
            images.append(npImage)
    return images


def test_list() -> list[np.array]:
    li: list = []
    for i in range(100):
        li.append(one_side("right"))
        li.append(one_side("left"))
    return li
"""
def list_1_1() -> list[np.array]:
    # Divide DMD into squares of 1x1 pixels
    # Create arrays of only one square on
    # 1039680 images in total => ~ 1039 GB of data
    a = 1
    return list_a_a(a)

def list_2_2() -> list[np.array]:
    # Divide DMD into squares of 2x2 pixels
    # Create arrays of only one square on
    # 259920 images in total => ~259 GB of data
    a = 2
    return list_a_a(a)

def list_3_3() -> list[np.array]:
    # Divide DMD into squares of 3x3 pixels
    # Create arrays of only one square on
    # 115520 images in total => ~115 GB of data
    a = 3
    return list_a_a(a)

def list_4_4() -> list[np.array]:
    # Divide DMD into squares of 4x4 pixels
    # Create arrays of only one square on
    # 64980 images in total => ~64.9 GB of data
    a = 4
    return list_a_a(a)

def list_6_6() -> list[np.array]:
    # Divide DMD into squares of 6x6 pixels
    # Create arrays of only one square on
    # 28880 images in total => ~28.8 GB of data
    a = 6
    return list_a_a(a)

def list_12_12() -> list[np.array]:
    # Divide DMD into squares of 12x12 pixels
    # Create arrays of only one square on
    # 7220 images in total => ~7.2 GB of data
    a = 12
    return list_a_a(a)
"""
def list_19_19() -> list[np.array]:
    # Divide DMD into squares of 19x19 pixels
    # Create arrays of only one square on
    # 2880 images in total => ~2.88 GB of data
    a = 19
    return list_a_a(a)

def list_38_38() -> list[np.array]:
    # Divide DMD into squares of 38x38 pixels
    # Create arrays of only one square on
    # 720 images in total => ~0.72 GB of data
    a = 19*2
    return list_a_a(a)

def list_57_57() -> list[np.array]:
    # Divide DMD into squares of 57x57 pixels
    # Create arrays of only one square on
    # 320 images in total => ~0.32 GB of data
    a = 19*3
    return list_a_a(a)

def list_76_76() -> list[np.array]:
    # Divide DMD into squares of 76x76 pixels
    # Create arrays of only one square on
    # 180 images in total => ~0.18 GB of data
    a = 19*4
    return list_a_a(a)

def list_114_114() -> list[np.array]:
    # Divide DMD into squares of 114x114 pixels
    # Create arrays of only one square on
    # 80 images in total => ~0.08 GB of data
    a = 19*6
    return list_a_a(a)

def create_all_patterns():
    """Create and save all defined patterns"""
    save_image(one_side(),"left_side")
    save_image(one_side("right"),"right_side")
    save_image(horizontal_50_50(),"horizontal_50_50")
    save_image(vertical_50_50(),"vertical_50_50")
    save_image(checkers(),"checkers")
    save_image(random_50_50(), "random_50_50")

    save_image_list(test_list(), "test_list")
    #save_image_list(list_19_19(), "19_19")
    #save_image_list(list_38_38(), "38_38")
    #save_image_list(list_57_57(), "57_57")
    #save_image_list(list_76_76(), "76_76")
    #save_image_list(list_114_114(), "114_114")

create_all_patterns()