# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 16:14:59 2022

@author: Peter
"""

#read file from one photon detector
#read file from other single photon detector
#take difference

import configparser

import csv
import numpy as np
import matplotlib.pyplot as plt

import basis_generation


import radial
import k_space
from IAFNNESTA import IAFNNESTA

BASIS_FILEPATH = "basis_numbers_run15.txt"
DATA_FILEPATH = "photodiode_data_run15.txt"
ARRAY_FILEPATH = "run15_array.txt"


#grabs the parameters for the program from config file 'config.ini'
def get_config_parameters():
    config = configparser.ConfigParser()
    config.read("config.ini")
    basis_parameters = {
        "basis_type": config.get("pattern", "basis_type"),
        "basis_size": config.getint("pattern", "basis_size"),
        "sensing_area": config.getint("pattern", "sensing_area"),
        "top_left_x": config.getint("pattern", "top_left_x"),
        "top_left_y": config.getint("pattern", "top_left_y"),
        }

    return (
        config.getint("compression", "compression_percent"),
        basis_parameters,
        config.get("file handling", "basis_indices_filename"),
    )


#reads file of indexes of basis generated when creating patterns
def get_indices(indices_filename):
    indices = []
    with open(indices_filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            indices.append(int(row[0]))
    
    return indices


def read_data_file(data_filename):
    detector_1_data = []
    detector_2_data = []
    with open(data_filename, 'r') as file:
        csv_reader = csv.reader(file)
        i = 0
        for row in csv_reader:
            #print(row[0])
            #print(row[1])
            print(i)
            i+=1
            detector_1_data.append(float(row[0].strip()))
            detector_2_data.append(float(row[1].strip()))
            
    return detector_1_data, detector_2_data


def reconstruct_image(basis_patterns, basis_patterns_inv, pd1_data, pd2_data, sensing_area):
    inverse = False
    for basises, signals in zip((basis_patterns, basis_patterns_inv), (pd1_data, pd2_data)):
        #if inverse:
        #    continue
        reconstructed_image = np.zeros((sensing_area, sensing_area), dtype = float)
        
        for signal, pattern in zip(signals, basis_patterns):
            reconstructed_image = reconstructed_image + np.array(signal*pattern)
            #plt.imshow(reconstructed_image)
            #plt.colorbar()
            #plt.show()
        
        #normalisation
        reconstructed_image /= np.mean(reconstructed_image)
        
        #plt.imshow(reconstructed_image)
        #plt.colorbar()
        #plt.show()
        if not inverse:
            image_1 = reconstructed_image
        else:
            image_2 = reconstructed_image
            
        inverse = True
        
    difference_image = image_1 - image_2
    #normalise
    difference_image = difference_image/np.max(difference_image)
    
    #save_to_file
    file = open(ARRAY_FILEPATH, "wb")
    np.save(file, difference_image)
    file.close
    
    plt.imshow(difference_image)
    plt.colorbar()
    plt.show()
    
    return difference_image


def smooth(image, sensing_area):
    idx=radial.radial2D(20,(sensing_area, sensing_area))
    A=lambda x: k_space.k_space_sampling(x,(sensing_area, sensing_area),idx)
    At=lambda x: k_space.adjoint(x,(sensing_area, sensing_area),idx)
        
    tv=IAFNNESTA(A(image), A=A,At=At, L1w=1,L2w=1, H = 'tv')
    tv = tv.real
    
    #normalise
    tv = tv/np.max(tv)
    
    tv = tv.reshape((sensing_area, sensing_area))
    plt.imshow(image)
    plt.colorbar()
    plt.show()



def main():
    compression, basis_params, basis_indices_filename = get_config_parameters()
    indices = get_indices(BASIS_FILEPATH)
    pd1_data, pd2_data = read_data_file(DATA_FILEPATH)
    basis_patterns = basis_generation.generate_bases(
        basis_type=basis_params["basis_type"], percent_compression=compression,
        basis_size=basis_params["basis_size"],
        indices=indices
        )
    
    basis_patterns = basis_patterns[0]
        
    if basis_params["sensing_area"] is not basis_params["basis_size"]:
        basis_patterns = basis_generation.pp_enlarge_patterns(
            basis_patterns, 
            basis_params["sensing_area"]
            )

    
    #********enlarge bases*******
    basis_patterns_inv = []
    for pattern in basis_patterns:
        array_of_ones = np.ones((basis_params["sensing_area"],basis_params["sensing_area"]))
        basis_patterns_inv.append(array_of_ones - pattern)
        
    image = reconstruct_image(
        basis_patterns, 
        basis_patterns_inv,
        pd1_data,
        pd2_data,
        basis_params["sensing_area"]
        )
    
    smooth(image, basis_params["sensing_area"])
    

if __name__ == "__main__":
    main()