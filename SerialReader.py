# -*- coding: utf-8 -*-
# -*- python=3.8.x
"""
Created on 17/07/2023

Reads data from Arduino

@author: Alex Kedziora
"""

import serial
import time
import csv

class ArduinoUNO:
    ser: serial.Serial

    def __init__(self,COM:str):
        self.ser = serial.Serial(COM, 115200, timeout=2) # MAX 115200

    def Read(self):
        return self.ser.readline() # Read the data (looks for terminating character '/r/n')
    

def save_data(li : list):
    with open('dataTEST6.csv', 'w') as f:
    # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow([str(i).replace("b","").replace("\\r","").replace("\\n","").replace("'","").replace("\\xca",",") for i in li])

def main():
    data: list = []
    ar = ArduinoUNO("COM3")
    start = time.time()
    con = True
    i = 0
    while(con ):
        text = ar.Read()
        end = time.time()
        if(len(text) != 0):
            data.append(text)
        if(end-start > 20):
            con = False
    save_data(data)

main()