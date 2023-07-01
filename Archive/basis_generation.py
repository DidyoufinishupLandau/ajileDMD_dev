# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 09:42:55 2022

@author: Peter
"""
from random import sample

from scipy.linalg import hadamard
from skimage.transform import rescale
import numpy as np
#import cv2


def generate_bases(*, basis_type="hadamard", basis_size=128, percent_compression=100, indices=None):
    if basis_type == "hadamard":
        basis_patterns, basis_indices = hadamard_bases(basis_size, percent_compression, indices)
    elif basis_type == "raster":
        basis_patterns, basis_indices = raster_bases(basis_size, percent_compression, indices)
    elif basis_type == "random single pixel":
        basis_patterns, basis_indices = random_single_on(basis_size, percent_compression, indices)
    elif basis_type == "random 50 percent":
        basis_patterns, basis_indices = random_50_percent(basis_size, percent_compression, indices)
    else:
        basis_patterns, basis_indices = hadamard_bases(basis_size, percent_compression, indices)

    return basis_patterns, basis_indices


#generates a set of hadamard basis patterns, but using a quicker algorithm
def hadamard_bases(size, percent_sample, indices):
    hadamard_pattern = hadamard(size**2)

    if indices is None:
        number_samples = int((size**2)*0.01*percent_sample)
        basis_indices = sample(np.arange((size**2)).tolist(), number_samples)
    else:
        basis_indices = indices

    hadamard_basis_patterns = []
    for index in basis_indices:
        basis_pattern = hadamard_pattern[:, index].reshape(size, size)
        basis_pattern = np.where(basis_pattern < 0, 0, basis_pattern)
        hadamard_basis_patterns.append(basis_pattern)

    return hadamard_basis_patterns, basis_indices


def raster_bases(size, percent_sample, indices = None):
    if indices is None:
        number_samples = int((size**2)*0.01*percent_sample)
        basis_indices = np.arange(number_samples)
    else:
        basis_indices = indices

    raster_basis_patterns = []
    for index in basis_indices:
        pattern = np.zeros(size**2)
        pattern[index] = 1
        pattern = pattern.reshape(size, size)
        raster_basis_patterns.append(pattern)

    return raster_basis_patterns, basis_indices


def random_single_on(size, percent_sample, indices = None):
    if indices is None:
        number_samples = int((size**2)*0.01*percent_sample)
        basis_indices = sample(np.arange((size**2)).tolist(), number_samples)
    else:
        basis_indices = indices
    
    raster_basis_patterns = []
    for index in basis_indices:
        pattern = np.zeros(size**2)
        pattern[index] = 1
        pattern = pattern.reshape(size, size)
        raster_basis_patterns.append(pattern)

    return raster_basis_patterns, basis_indices


def random_50_percent(size, percent_sample, seeds = None):
    
    number_samples = int((size**2)*0.01*percent_sample)
    create_seed = False
    if seeds is None:
        seeds = []
        create_seed = True
        
    basis_patterns = []
    if create_seed:
        seed = np.random.randint(0, 10000)
    else:
        seed = seeds[0]
    np.random.seed(seed)
    
    for i in range(number_samples):
        pattern = np.zeros(size**2)
        pattern[:int(size**2 / 2)] = 1   
        
        
        np.random.shuffle(pattern)
        pattern = pattern.reshape(size, size)
        basis_patterns.append(pattern)
        seeds.append(seed)

    return basis_patterns, seeds



#enlarge the hadamard pattern by an integer amount so it covers a larger area.
def enlarge_patterns(patterns, image_size):

    enlargement_factor = image_size/patterns[0].shape[0]
    #print(enlargement_factor)
    enlarged_patterns = []
    #size = patterns[0].shape[0]
    j=1
    for pattern in patterns:
        """
        enlarged_pattern = np.zeros((enlargement_factor*size, enlargement_factor*size))
        for i in range(size):
            for j in range(size):
                if pattern[i,j] != 0:
                    for k in range(enlargement_factor):
                        for l in range(enlargement_factor):
                            enlarged_pattern[i*enlargement_factor + k, j*enlargement_factor + l] = 1
                            
        enlarged_patterns.append(enlarged_pattern)
        enlarged_pattern = None      
        """
        """
        enlarged_patterns.append(
            cv2.resize(pattern, (image_size, image_size), interpolation=cv2.INTER_NEAREST)
            )
        """
        enlarged_patterns.append(rescale(pattern, enlargement_factor, multichannel=False))
        print(j)
        j+=1
    return enlarged_patterns





def pp_enlarge_patterns(patterns, image_size):
    scale = image_size//patterns[0].shape[0]
    p_size = patterns[0].shape[0]
    print(scale)
    enlarged_patterns = []
    print(len(patterns))
    j=1
    for pattern in patterns:
        out_array = np.zeros(np.array(pattern.shape)*scale)
        for (i,p) in enumerate(pattern):
            rs=np.reshape(np.repeat(np.repeat(p,scale),scale),(p_size*scale,scale)).T
            out_array[i*scale:(i+1)*scale,:] = rs
        enlarged_patterns.append(out_array)
        print(j)
        j += 1
    return enlarged_patterns
























