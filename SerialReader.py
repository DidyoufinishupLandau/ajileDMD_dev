# -*- coding: utf-8 -*-
# -*- python=3.8.x
"""
Created on 17/07/2023

Reads data from Arduino

@author: Alex Kedziora
"""

import serial

class ArduinoUNO:
    ser: serial

    def __init__(COM:str):
        ser = serial.Serial(COM, 115200, timeout=1)
