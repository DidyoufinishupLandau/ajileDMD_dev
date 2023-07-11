# -*- coding: utf-8 -*-
# -*- python=3.8.x
"""
Created on 10/07/2023

This file represents a simple interface to control DMD
it has all needed functionalities taken from the different files

The purpose of this file is to provide details about the software,
all functions must be commented well

This class is supposed to be access using:  exec(open('file.py').read())

@author: Alex Kedziora
"""

import ajiledriver as aj
from new_dmd_control import DMDdriver
import new_compressive_sensing as cs
import pattern_generator as pg
import os
import numpy as np
import configparser
import json
import pickle


class DMD:
    __dmd = DMDdriver()
    __IMAGE_ID = 1 # Increment when image is added to a sequence
    __patterns: list = []

    __loaded_patterns: list = [] ## List(str)
    __patterns_count: list = [] ## List(int)
    __frame_time: int = 1 # (ms)
    __main_rep: int = 1 # repetition count of the main sequence

    def __init__(self) -> None:
        #__dmd = DMDdriver()
        #pg.create_all_patterns()
        __patterns = self.__load_list_images()



    ## ----  Private  ---- ##

    def __load_list_images() -> list:
        # Loads file NAMES present in ./patterns
        # All paterns should be created before hand using pattern_generator.py
        patterns = []
        for file in os.listdir("./patterns"):
            # Check whether file is in pickle format or not
            if file.endswith(".pickle"):
                patterns.append(file)
        return patterns
    
    def __get_config_parameters() -> dict:
        config = configparser.ConfigParser()
        config.read("running_pattern.ini")
        pattern_param = {
            "patterns": config.get("pattern", "patterns"),
            "frames_count": config.get("pattern", "frames_count"),
            "frame_time": config.getint("pattern", "frame_time"),
            "main_seq_rep": config.getint("pattern", "main_seq_rep"),
            }

        return pattern_param

    def __print_list(patterns : list) -> None:
        # Prints all items in the lsit 
        #os.system('cls')
        print("The list of patterns available:")
        for i in range(len(patterns)):
            print(str(i) + " : " + patterns[i])



    ## ----  Public  ---- ##

    def load_saved_ini(self) -> None:
        cp = self.__get_config_parameters()
        self.__loaded_patterns = json.loads(cp["patterns"])
        self.__patterns_count = json.loads(cp["frames_count"])
        self.__frame_time  = cp["frame_time"]
        self.__main_rep = cp["main_seq_rep"]

    def add_image_to_seq(self, npImage : np.array, frameTime : int = 10) -> None:
        # Add image to the main sequence (currently selected sequence) 
        self.__dmd.add_sub_sequence(npImage, self.__IMAGE_ID, frameTime)
        self.__IMAGE_ID += 1

    def add_image_to_seq(self, patternName : str, frameTime : int = 10) -> None:
            image : np.array
            image = pickle.load(open("./patterns/" + patternName + ".pickle", 'rb'))
            self.add_image_to_seq(image,frameTime)


    def set_frame_time(self, time : int) -> None:
        self.__frame_time = time
    
    def create_patterns() -> None:
        pg.create_all_patterns()

    def set_main_repetition(self, repetition : int) -> None:
        self.__main_rep = repetition

    def show_patterns(self) -> None:
        self.__print_list(self.__patterns)
    
    ## I think I should load everything here
    # use loaded_patterns to create an image, and in add_image just put it into loaded_patterns list
    def create_project(self) -> None:
        self.__dmd.create_project()
        self.__dmd.create_main_sequence(self.__main_rep)

    def run(self) -> None:
        self.__dmd.start_projecting()

    def stop(self) -> None:
        self.__dmd.stop_projecting()
    
