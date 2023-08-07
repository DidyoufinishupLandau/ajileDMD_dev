# -*- coding: utf-8 -*-
# -*- python=3.8.x
"""
Created on 06/07/2023

New version of compressive sensing.
The goal is to create real-time implementation and seq creation.
DMD is supposed to load once and run in a loop so user can create a sequence.

@author: Alex Kedziora
"""

import ajiledriver as aj
from new_dmd_control import DMDdriver
import os
import numpy as np
import pickle
import pattern_generator as pg
import sys
import SerialReader as sr


def load_list_images() -> list:
    # Loads file NAMES present in ./patterns
    # All paterns should be created before hand using pattern_generator.py
    patterns = []
    for file in os.listdir("./patterns"):
        # Check whether file is in pickle format or not
        if file.endswith(".pickle"):
            patterns.append(file)
    return patterns

def load_list_images_list() -> list:
    # Loads file NAMES present in ./patterns
    # All paterns should be created before hand using pattern_generator.py
    patterns = []
    for file in os.listdir("./patterns/lists"):
        # Check whether file is in pickle format or not
        if file.endswith(".pickle"):
            patterns.append(file)
    return patterns

def add_image_to_seq(npImage : np.array, imageID : int) -> None:
    # Add image to the main sequence (currently selected sequence) 
    time: int = input("Time of the frame (ms): ")
    dmd.add_sub_sequence(npImage, imageID, int(time))

def print_list(patterns : list) -> None:
    # Prints all items in the lsit 
    os.system('cls')
    print("The list of patterns available:")
    for i in range(len(patterns)):
        print(str(i) + " : " + patterns[i])

def switch_menu() -> int:
    # Basic menu to create a sequence and to run the project
    # Return 0 if works, -1 if exit (or non-exisiting option is given)
    # switch-case not defined in py3.8, available in py3.10
    imageID = 0
    image = np.array
    images: list[np.array]

    print("Options:")
    print("0: Generate new patterns")
    print("1: Create new main sequence")
    print("2: Create subsequences")
    print("3: Run")
    print("4: Clean the sequence")
    print("5: Exit")
    print("6: Add list")
    print("7: Set triggers and run")
    print("8: Multiple with OFF image")
    option = input("Select option: ")


    # Create new sequence (not needed if only one main sequence is loaded)
    if(option == "1"):
        dmd.create_project()
        dmd.create_main_sequence(5)
        print("The main sequence ID is: " + dmd.main_sequence_ID)
        return 0
    
    elif(option == "0"):
        pg.create_all_patterns()
        return 0
    
    # Create subsequence (main option to create a list of patterns to display)
    elif(option == "2"):
        patterns = load_list_images()
        continue_loop = True
        while(continue_loop):
            os.system('cls')
            inp = input("Add another sequence [y/n]: ")
            if(inp == "y"):
                imageID += 1
                print_list(patterns)
                pattID = int
                pattID = input("Select ID of the patterns to add it to the main sequence: ")
                image = pickle.load(open("./patterns/" + patterns[int(pattID)], 'rb'))
                add_image_to_seq(image,imageID)
                _rp.Number_of_images(imageID)
            else:
                continue_loop = False
        return 0

    # Run the project (loads the created pattern and runs it)
    elif(option == "3"):
        dmd.stop_projecting()
        # Load the defined project, and wait for completion
        dmd.start_projecting(10)
        input("Press Enter to stop the sequence")
        dmd.stop_projecting()
        return 0

    # Clean the sequence (need to write the code)
    elif(option == "4"):
        return -1
    
    # Exit
    elif(option == "5"):
        return -1
    
    # Add list
    elif(option == "6"):
        patterns = load_list_images_list()
        continue_loop = True
        os.system('cls')

        print_list(patterns)
        pattID = int
        pattID = input("Select ID of the patterns to add it to the main sequence: ")
        images = pickle.load(open("./patterns/lists/" + patterns[int(pattID)], 'rb'))
        freq: int = int(input("Frame time of each sequence: "))
        dmd.add_sub_sequence_list(images, freq)
        _rp.Number_of_images(len(images))
        return 0
    
    elif(option == "7"):
        dmd.my_trigger()
        dmd.run_example()
        _rp.Start()
        return 0
    
    elif(option == "8"):
        patterns = load_list_images_list()
        continue_loop = True
        os.system('cls')

        # Off should be right side - left side is for testing (aims to PD)
        offImage = pickle.load(open("./patterns/" + "right_side.pickle", 'rb'))

        print_list(patterns)
        pattID = int
        pattID = input("Select ID of the patterns to add it to the main sequence: ")
        images = pickle.load(open("./patterns/lists/" + patterns[int(pattID)], 'rb'))
        freq: int = int(input("Frame time of each sequence: "))
        dmd.multiple_patterns_sequence(images, offImage, int(freq))
        return 0
    
    elif(option == "9"):
        print("Saving")
        sr.save_data(_rp.Get_data(), "PicoTest")
        print("Data Saved")
        return 0

    elif(option =="10"):
        print(_rp.Test())
        _rp.Info()
        return 0
    # Non-existing option given = exit
    return -1

def main():
    dmd.create_project()

    repSeq: int = input("Repetition count of the main sequence (0 means infinity): ")

    dmd.create_main_sequence(int(repSeq)) # 0 means infinity
    print("Project and initial sequence are created")

    option = 0
    continue_loop = True

    while(continue_loop):
        option = switch_menu()
        if(option == -1):
            continue_loop = False
            return



if __name__ == "__main__":
    global dmd
    global _rp
    #_rp = sr.RPPico("COM7")
    #_rp.Reset()
    #dmd = DMDdriver()
    main()

