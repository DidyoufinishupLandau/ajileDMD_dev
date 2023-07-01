# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 14:48:15 2022

@author: Peter
"""

import configparser

import dmd_control
import basis_generation



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


#save the indices of the hadamard patterns to file
def write_basis_indices_to_file(filename, basis_indices):
    basis_index_file = open(filename, 'w')
    for index in basis_indices:
        basis_index_file.write(str(index)+'\n')
    basis_index_file.close()
    
    
def main():

    percent_compression, basis_params, basis_indices_filename = get_config_parameters()

    #get basis patterns. default hadamard
    basis_patterns, basis_indices = basis_generation.generate_bases(
        basis_type=basis_params["basis_type"], 
        basis_size=basis_params["basis_size"],
        percent_compression=percent_compression
        )
    
    write_basis_indices_to_file(basis_indices_filename, basis_indices)
    
    if basis_params["sensing_area"] is not basis_params["basis_size"]:
        basis_patterns = basis_generation.pp_enlarge_patterns(basis_patterns, basis_params["sensing_area"])
    
    dmd_control.run_dmd(basis_patterns, (basis_params["top_left_x"], basis_params["top_left_y"]))

    


if __name__ == "__main__":
    main()
