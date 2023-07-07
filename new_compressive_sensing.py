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
from new_dmd_control import DMD
import os
import numpy as np

global IMAGE_ID

def load_list_images() -> list:
    patterns = []
    os.chdir("./patterns/")
    for file in os.listdir():
        # Check whether file is in text format or not
        if file.endswith(".pickle"):
            patterns.append(file)
    return patterns

def add_image_to_seq(npImage : np.array):
    IMAGE_ID += 1
    dmd.add_sub_sequence(npImage, IMAGE_ID)

def print_list(patterns : list):
    os.system('cls')
    print("The list of patterns available:")
    for i in range(len(patterns)):
        print(i + " : " + patterns[i])

def switch_menu() -> int:
    # switch-case not defined in py3.8, available in py3.10
    print("Options:")
    print("1: Create new main sequence")
    print("2: Create subsequences")
    print("3: Exit")
    option = input("Select option: ")

    if(option == "1"):
        dmd.create_project()
        dmd.create_main_sequence(5)
        print("The main sequence ID is: " + dmd.main_sequence_ID)
        return 0

    elif(option == "2"):
        patterns = load_list_images()
        continue_loop = True
        while(continue_loop):
            inp = input("Add another sequence [y/n]: ")
            if(inp == "y"):
                print_list(patterns)
                pattID = int
                pattID = input("Select ID of the patterns to add it to the main sequence: ")
                add_image_to_seq(patterns[pattID])
            else:
                continue_loop = False
        return 0

    elif(option == "3"):
        return -1

    return -1

def main():
    print(load_list_images())
    dmd.create_project()
    dmd.create_main_sequence(5)
    print("Project and initial sequence are created")
    option = 0
    continue_loop = True
    while(continue_loop):
        #os.system('cls')
        option = switch_menu()
        if(option == -1):
            continue_loop = False
            return



if __name__ == "__main__":
    global dmd
    IMAGE_ID = 0
    #dmd = DMD()
    main()
