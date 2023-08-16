# -*- coding: utf-8 -*-
# -*- python=3.8.x
"""
Created on 08/08/2023

This file creates an interface between images, sequences, and pythonic interpretations of these
that can be fed into the DMD_driver.

"""

import numpy as np
from typing import List, Union
from DMD_driver import DMD_driver
from matplotlib import pyplot as plt
import pattern_generator as pg


class dmd_image:
    _dmd_driver: Union[DMD_driver, None] = None
    _height: int = 0
    _width: int = 0
    _image: np.array

    def __init__(self, dmd_driver: DMD_driver, image: Union[np.array, str, None] = None):
        if dmd_driver is not None:
            self._dmd_driver = dmd_driver
            self._height = dmd_driver.HEIGHT
            self._width = dmd_driver.WIDTH
        else:
            # Use default values
            self._height = pg.aj.DMD_IMAGE_HEIGHT_MAX
            self._width = pg.aj.DMD_IMAGE_WIDTH_MAX
            self._dmd_driver = None

        if image is not None:
            if type(image) is str:
                if image in pg.named_patterns.keys():
                    self.image = pg.named_patterns[image]()
                else:
                    KeyError(f"Pattern {image} not found")
            elif type(image) is np.array:
                self.image = image
            else:
                raise ValueError("Image is not of the correct type")
        else:
            self._image = np.zeros((self._height, self._width), dtype=np.uint8)

    @property
    def image(self) -> np.array:
        return self._image

    @image.setter
    def image(self, image: np.array) -> None:
        if image.shape == (self._height, self._width):
            self._image = image
        else:
            raise ValueError("Image is not of the correct size")

    def plot(self) -> None:
        # Plot image using matplotlib
        plt.imshow(self._image, cmap='gray', vmin=0, vmax=255)

    def project(self) -> None:
        """Show the image on the dmd, as a single image infinite time"""
        if self._dmd_driver is None:
            raise RuntimeError("DMD driver not set")
        # Stop any existing projection
        self._dmd_driver.stop_projecting()
        # Create new project
        self._dmd_driver.create_project("single_image")
        # Create sequence
        self._dmd_driver.create_main_sequence(1)
        # Add image to the project
        self._dmd_driver.add_sub_sequence(self._image, 1)
        # Run the project
        self._dmd_driver.start_projecting()


class dmd_sequence:
    """A sequence - a holder of lists of images and frame times"""
    _dmd_driver: DMD_driver = None
    _images: List[dmd_image] = []
    _frame_times: List[int] = []
    _repetitions: int = 0

    def __init__(self, dmd_driver: DMD_driver):
        self._dmd_driver = dmd_driver

    def add_image(self, image: Union[dmd_image, np.array], frame_time: int) -> "dmd_sequence":
        if type(image) is dmd_image:
            self._images.append(image)
        else:
            # Create new dmd image
            self._images.append(dmd_image(self._dmd_driver, image))
        # Add frame time
        self._frame_times.append(frame_time)
        return self

    def upload_and_run(self) -> None:
        """Upload the sequence as a new project"""
        self._dmd_driver.stop_projecting()
        # Create new project
        self._dmd_driver.create_project("sequence")
        # Create sequence
        self._dmd_driver.create_main_sequence(1)
        # Add image to the project
        for i, frame in enumerate(self._images, start=1):
            self._dmd_driver.add_sub_sequence(frame.image, i)
        # Run the project
        self._dmd_driver.start_projecting()

    def __getitem__(self, item):
        return self._images[item]

    def __len__(self):
        return len(self._images)

    def __iter__(self):
        return iter(self._images)
