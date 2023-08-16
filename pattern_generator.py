# -*- coding: utf-8 -*-
# -*- python=3.8.x
"""
Created on 06/07/2023

Another method of creating images (patterns).
The goal is to create a full-size image with small data size.

@author: Alex Kedziora
"""
import collections
from functools import partial
import cv2
import numpy as np
import pickle
from typing import List, Dict, Callable

# Define image sizes
ajile_conf = collections.namedtuple("ajile_conf", "DMD_IMAGE_HEIGHT_MAX DMD_IMAGE_WIDTH_MAX")
aj = ajile_conf(1140, 912)


def save_image(image: np.array, file_name: str):
    """Saves an array as a pickle file in the given relative path"""
    with open("./patterns/" + file_name + ".pickle", "wb") as handle:
        pickle.dump(image, handle, protocol=pickle.HIGHEST_PROTOCOL)


def save_image_list(image: List[np.array], file_name: str):
    """Saves an array as a pickle file in the given relative path"""
    with open("./patterns/lists/" + file_name + ".pickle", "wb") as handle:
        pickle.dump(image, handle, protocol=pickle.HIGHEST_PROTOCOL)


def one_side(side: str = "left") -> np.array:
    """Flip all mirrors to one side """
    if side == "left":
        np_image = np.ones(shape=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX, 1), dtype=np.uint8) * 255
    else:
        np_image = np.zeros(shape=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX, 1), dtype=np.uint8)

    return np_image


def horizontal_50_50() -> np.array:
    """Flip first row of mirrors to left, second row to right..."""
    np_image = np.zeros(shape=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX, 1), dtype=np.uint8)
    for im in np_image:
        im[::2] = 255
    return np_image


def vertical_50_50() -> np.array:
    """Flip first column of mirrors to left, second column to right..."""
    np_image = np.ones(shape=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX, 1), dtype=np.uint8) * 255
    np_image[::2] = np_image[::2] * 0
    return np_image


def checkers() -> np.array:
    # First pixel is 255, second 0, third 255....
    np_image = np.zeros(shape=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX, 1), dtype=np.uint8)
    for i in range(len(np_image)):
        for j in range(len(np_image[i])):
            if (i + j) % 2 == 0:
                np_image[i][j] = 255
    return np_image


def random_50_50() -> np.array:
    # Generate numbers from 0 to 1 sorted as an array (then multiply by 255)
    np_image = np.random.randint(2, size=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX, 1), dtype=np.uint8) * 255
    return np_image


def random_1() -> np.array:
    np_image = np.zeros(shape=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX, 1), dtype=np.uint8)
    a = np.random.randint(0, aj.DMD_IMAGE_HEIGHT_MAX)
    b = np.random.randint(0, aj.DMD_IMAGE_WIDTH_MAX)
    np_image[a][b] = 255
    return np_image


def list_a_a(a: int) -> list[np.array]:
    # Divide DMD into squares of A x A pixels
    # Create arrays of only one square on
    # 1140*912/a^2 images in total => ~ 1140*912/a^2 kB of data
    images: list = []
    np_image: np.array
    for col in range(int(aj.DMD_IMAGE_WIDTH_MAX / a)):
        for wid in range(int(aj.DMD_IMAGE_HEIGHT_MAX / a)):
            np_image = np.zeros(shape=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX, 1), dtype=np.uint8)
            cv2.rectangle(np_image, (wid * a, col * a), ((wid + 1) * a - 1, (col + 1) * a - 1), 255)
            images.append(np_image)
    return images


named_patterns: Dict[str, Callable] = {
    "one_side_left": partial(one_side, side="left"),
    "one_side_right": partial(one_side, side="right"),
    "horizontal_50_50": horizontal_50_50,
    "vertical_50_50": vertical_50_50,
    "checkers": checkers,
    "random_50_50": random_50_50,
    "random_1": random_1}
