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
import numpy as np
from typing import Dict, Callable
from skimage import transform

# Define image sizes
ajile_conf = collections.namedtuple("ajile_conf", "DMD_IMAGE_HEIGHT_MAX DMD_IMAGE_WIDTH_MAX")
aj = ajile_conf(1140, 912)


def one_side(side: str = "left") -> np.array:
    """Flip all mirrors to one side """
    if side == "left":
        np_image = np.ones(
            shape=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX, 1),
            dtype=np.uint8) * 255
    else:
        np_image = np.zeros(
            shape=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX, 1),
            dtype=np.uint8)

    return np_image


def horizontal_50_50() -> np.array:
    """Flip first row of mirrors to left, second row to right..."""
    np_image = np.zeros(
        shape=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX, 1),
        dtype=np.uint8)
    # Flip every second row
    for im in np_image:
        im[::2] = 255
    return np_image


def vertical_50_50() -> np.array:
    """Flip first column of mirrors to left, second column to right..."""
    np_image = np.ones(
        shape=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX, 1),
        dtype=np.uint8) * 255
    # Flip every second column
    np_image[::2] = np_image[::2] * 0
    return np_image


def checkers() -> np.array:
    # First pixel is 255, second 0, third 255....
    np_image = np.zeros(
        shape=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX, 1),
        dtype=np.uint8)
    # Iterate over each column
    for i in range(len(np_image)):
        # Iterate over each row
        for j in range(len(np_image[i])):
            if (i + j) % 2 == 0:
                np_image[i][j] = 255

    return np_image


def random_50_50() -> np.array:
    # Generate numbers from 0 to 1 sorted as an array (then multiply by 255)
    np_image = np.random.randint(2,
                                 size=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX, 1),
                                 dtype=np.uint8) * 255
    return np_image


def random_1() -> np.array:
    np_image = np.zeros(
        shape=(aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX, 1),
        dtype=np.uint8)
    # Generate random coordinates
    a = np.random.randint(0, aj.DMD_IMAGE_HEIGHT_MAX)
    b = np.random.randint(0, aj.DMD_IMAGE_WIDTH_MAX)
    # Set one pixel to 255
    np_image[a][b] = 255
    return np_image


def rescale(input_image: np.array) -> np.array:
    """Use the skimage transform module to rescale the provided image to the size given by ajile_conf"""
    # First, quantize input image to either 0 or 255
    input_image = np.where(input_image > 127, 255, 0)
    # Then, resize the image
    rs = transform.resize(input_image, (aj.DMD_IMAGE_HEIGHT_MAX, aj.DMD_IMAGE_WIDTH_MAX), order=0, anti_aliasing=False)
    # Finally, quantize the image again and return
    return np.where(rs > 127, 255, 0)


# Dictionary of patterns
named_patterns: Dict[str, Callable] = {
    "one_side_left": partial(one_side, side="left"),
    "one_side_right": partial(one_side, side="right"),
    "horizontal_50_50": horizontal_50_50,
    "vertical_50_50": vertical_50_50,
    "checkers": checkers,
    "random_50_50": random_50_50,
    "random_1": random_1}
