# -*- coding: utf-8 -*-
# -*- python=3.8.x
"""
Created on Tue Mar  8 14:48:15 2022

@author: Patrick Parkinson
----
Edited 04/07/2023 - AK

Changed config path since relative path didn't work (why?)
"""

import configparser
from dmd_control import DMD
import basis_generation
from typing import TypedDict
import pickle
import pickletools
from datetime import datetime

class ConfigDict(TypedDict):
    basis_type: str
    basis_size: int
    sensing_area: int
    top_left_x: int
    top_left_y: int
    compression: float
    file_handling: int


# grabs the parameters for the program from config file 'config.ini'
def get_config_parameters():
    config = configparser.ConfigParser()
    ## Works with full path
    config.read(r"C:\Users\Alex\Documents\PSI_intern\OneDrive_1_6-20-2023\Software\DMD---PSI\config.ini")
    return ConfigDict(basis_type=config.get('pattern', 'basis_type'),
                      basis_size=config.getint("pattern", "basis_size"),
                      sensing_area=config.getint("pattern", "sensing_area"),
                      top_left_x=config.getint("pattern", "top_left_x"),
                      top_left_y=config.getint("pattern", "top_left_y"),
                      compression=config.getint("compression", "compression_percent"),
                      file_handling=config.getint("file handling", "basis_indices_filename"))


def create_pattern_images():
    config_params = get_config_parameters()
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    basis_patterns, basis_indices = basis_generation.generate_bases(
        basis_type="left side",
        basis_size=config_params["basis_size"],
        percent_compression=config_params['compression']
    )

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    # Rescale if required
    if config_params["sensing_area"] is not config_params["basis_size"]:
        basis_patterns = [basis_generation.enlarge_pattern(b, config_params["sensing_area"]) for b in basis_patterns]

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    board_images = basis_generation.embed_pattern(patterns=basis_patterns,
                                                  top_left=(config_params['top_left_x'], config_params['top_left_y']),
                                                  height=1140,
                                                  width=912)
    
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    print(len(board_images))
    print(len(board_images[0]))
    #with open("./patterns/left_side.pickle","wb") as handle:
    #    pickle.dump(board_images, handle, protocol=pickle.HIGHEST_PROTOCOL)


def pre_main():
    create_pattern_images()
    #board_images = pickle.load(open("left_side.p","rb"))
    # Insert images
    dmd.insert_images(board_images)
    #dmd.create_sequence()
    print("pattern2")
    basis_patterns, basis_indices = basis_generation.generate_bases(
        basis_type="right side",
        basis_size=config_params["basis_size"],
        percent_compression=config_params['compression']
    )
    # Rescale if required
    if config_params["sensing_area"] is not config_params["basis_size"]:
        basis_patterns = [basis_generation.enlarge_pattern(b, config_params["sensing_area"]) for b in basis_patterns]
        
    # create dmd images
    board_images = basis_generation.embed_pattern(patterns=basis_patterns,
                                                  top_left=(config_params['top_left_x'], config_params['top_left_y']),
                                                  height=dmd.HEIGHT,
                                                  width=dmd.WIDTH)
    # Insert images
    dmd.insert_images(board_images)
    #dmd.create_sequence()
    basis_patterns, basis_indices = basis_generation.generate_bases(
        basis_type="left side",
        basis_size=config_params["basis_size"],
        percent_compression=config_params['compression']
    )
    # Rescale if required
    if config_params["sensing_area"] is not config_params["basis_size"]:
        basis_patterns = [basis_generation.enlarge_pattern(b, config_params["sensing_area"]) for b in basis_patterns]

    # Get components attached to device
    #dmd.create_project()
    # Add trigger
    #dmd.create_trigger_rules(controller_index=0)
    # create dmd images
    board_images = basis_generation.embed_pattern(patterns=basis_patterns,
                                                  top_left=(config_params['top_left_x'], config_params['top_left_y']),
                                                  height=dmd.HEIGHT,
                                                  width=dmd.WIDTH)
    # Insert images
    dmd.insert_images(board_images)
    print("pattern3")
    basis_patterns, basis_indices = basis_generation.generate_bases(
        basis_type="random 50 percent",
        basis_size=config_params["basis_size"],
        percent_compression=config_params['compression']
    )
    # Rescale if required
    if config_params["sensing_area"] is not config_params["basis_size"]:
        basis_patterns = [basis_generation.enlarge_pattern(b, config_params["sensing_area"]) for b in basis_patterns]

    # Get components attached to device
    #dmd.create_project()
    # Add trigger
    #dmd.create_trigger_rules(controller_index=0)
    # create dmd images
    board_images = basis_generation.embed_pattern(patterns=basis_patterns,
                                                  top_left=(config_params['top_left_x'], config_params['top_left_y']),
                                                  height=dmd.HEIGHT,
                                                  width=dmd.WIDTH)
    # Insert images
    dmd.insert_images(board_images)
    print("pattern3end")

    dmd.create_sequence()
    

def main():
    pre_main()
    # Associate frames with sequence
    # Stop any currently running sequence
    dmd.stop_projecting()
    # Load the defined project, and wait for completion
    dmd.start_projecting()
    input("Press Enter to stop the sequence")
    dmd.stop_projecting()


if __name__ == "__main__":
    global dmd
    dmd = DMD()
    main()
