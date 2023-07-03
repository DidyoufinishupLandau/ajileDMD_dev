# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 09:42:55 2022

@author: Peter
-----
Edited 03/07/2023: AK

np.random -> random : there were 2 args given and np.random accepts at most 1
"""
from __future__ import annotations
from scipy.linalg import hadamard
import numpy as np
import random ## previously np.random was used but it was incorrect due to given arguments (2 were given)

## Changes = to : to fix the error (not valid for 3.8 but works for 3.10)
BasisTuple: tuple[list, list] 
Indices: list | None


def generate_bases(basis_type: str = "hadamard",
                   basis_size: int = 128,
                   percent_compression: float = 100,
                   indices: Indices = None) -> BasisTuple:
    """Function to select what type of basis to use and return."""
    if basis_type == "hadamard":
        basis_patterns, basis_indices = hadamard_bases(basis_size, percent_compression, indices)
    elif basis_type == "raster":
        basis_patterns, basis_indices = raster_bases(basis_size, percent_compression, indices)
    elif basis_type == "random single pixel":
        basis_patterns, basis_indices = random_single_on(basis_size, percent_compression, indices)
    elif basis_type == "random 50 percent":
        basis_patterns, basis_indices = random_50_percent(basis_size, percent_compression, indices)
    elif basis_type == "right side":
        basis_patterns, basis_indices = one_side(basis_size, percent_compression, "right")
    elif basis_type == "left side":
        basis_patterns, basis_indices = one_side(basis_size, percent_compression, "left")
    else:
        basis_patterns, basis_indices = hadamard_bases(basis_size, percent_compression, indices)
    return basis_patterns, basis_indices


def hadamard_bases(size: int,
                   percent_sample: float = 100,
                   indices: Indices = None) -> BasisTuple:
    """Generate Hadamard basis using scipy.linalg."""
    hadamard_pattern = hadamard(size ** 2)

    if indices is None:
        number_samples = int((size ** 2) * 0.01 * percent_sample)
        basis_indices = random.sample(np.arange((size ** 2)).tolist(), number_samples)
    else:
        basis_indices = indices

    hadamard_basis_patterns = []
    for index in basis_indices:
        basis_pattern = hadamard_pattern[:, index].reshape(size, size)
        basis_pattern = np.where(basis_pattern < 0, 0, basis_pattern)
        hadamard_basis_patterns.append(basis_pattern)

    return hadamard_basis_patterns, basis_indices


def raster_bases(size: int, percent_sample: float = 100, indices: Indices = None) -> BasisTuple:
    """Generate a raster basis - point by point"""
    if indices is None:
        number_samples: int = int((size ** 2) * 0.01 * percent_sample)
        basis_indices = np.arange(number_samples)
    else:
        basis_indices = indices

    raster_basis_patterns: list[np.ndarray] = []
    for index in basis_indices:
        pattern = np.zeros(size ** 2)
        pattern[index] = 1
        pattern = pattern.reshape(size, size)
        raster_basis_patterns.append(pattern)
    return raster_basis_patterns, basis_indices


def random_single_on(size: int, percent_sample: float = 100, indices: Indices = None) -> BasisTuple:
    """Random raster."""
    if indices is None:
        number_samples: int = int((size ** 2) * 0.01 * percent_sample)
        basis_indices = random.sample(np.arange((size ** 2)).tolist(), number_samples)
    else:
        basis_indices = indices

    raster_basis_patterns: list[np.ndarray] = []
    for index in basis_indices:
        pattern = np.zeros(size ** 2)
        pattern[index] = 1
        pattern = pattern.reshape(size, size)
        raster_basis_patterns.append(pattern)

    return raster_basis_patterns, basis_indices


def random_50_percent(size: int, percent_sample: float = 100, seed=None) -> BasisTuple:
    """Turn on 50% of the points, and keep 50% off"""
    number_samples: int = int((size ** 2) * 0.01 * percent_sample)
    if seed is None:
        seed = np.random.randint(0, 10000)
    else:
        seed = seed[0]
    np.random.seed(seed)
    index: list[int] = []
    basis_patterns: list[np.ndarray] = []
    for i in range(number_samples):
        pattern = np.zeros(size ** 2)
        pattern[:int(size ** 2 / 2)] = 1

        np.random.shuffle(pattern)
        pattern = pattern.reshape(size, size)
        basis_patterns.append(pattern)
        index.append(i)

    return basis_patterns, index


def one_side(size: int, percent_sample: float = 100, side : str = "left") -> BasisTuple:
    """Flip all mirrors to one side """
    number_samples: int = int((size ** 2) * 0.01 * percent_sample)

    index: list[int] = []
    basis_patterns: list[np.ndarray] = []
    for i in range(number_samples):
        if(side == "left"):
            pattern = np.ones(size ** 2)
        else:
            pattern = np.zeros(size ** 2)

        pattern = pattern.reshape(size, size)
        basis_patterns.append(pattern)
        index.append(i)

    return basis_patterns, index


######


def embed_pattern(patterns: list[np.ndarray], top_left: tuple[int, int],
                  height: int, width: int) -> list[np.ndarray]:
    """Embed the pattern within a larger image, to fit it on to the DMD"""
    board_images = []
    for pattern in patterns:
        # Create a patter of the size of the device
        bp = np.zeros(shape=(height, width, 1), dtype=np.uint8)
        # Replace the active area with the pattern and scale up
        bp[top_left[0]:pattern.shape[0] + top_left[0],
            top_left[1]:pattern.shape[1] + top_left[1], 0] = pattern * 255
        # Append to list
        board_images.append(bp)
    return board_images


def enlarge_pattern(pattern: np.ndarray, image_size: int) -> np.ndarray:
    """Scale the image up, integer multiples preferred"""
    # Determine size
    p_size = pattern.shape[0]
    # Determine scale
    scale = image_size // p_size
    # Create output array
    out_array = np.zeros(np.array(pattern.shape) * scale)
    # Iterate over each point in pattern, and repeat grid
    for (i, p) in enumerate(pattern):
        rs = np.reshape(np.repeat(np.repeat(p, scale), scale), (p_size * scale, scale)).T
        out_array[i * scale:(i + 1) * scale, :] = rs
    return out_array
