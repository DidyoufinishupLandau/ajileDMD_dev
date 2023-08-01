# -*- coding: utf-8 -*-
# -*- python=3.8.x
"""
Created on 17/07/2023

Reads data from Raspberry Pi Pico

@author: Alex Kedziora
"""

import serial
import time
import csv
import sys

"""
class ArduinoUNO:
    ser: serial.Serial

    def __init__(self,COM:str):
        self.ser = serial.Serial(COM, 9600, timeout=2) # MAX 115200

    def Read(self):
        return self.ser.readline() # Read the data (looks for terminating character '/r/n')

    def Write(self, text: str= ""):
        self.ser.write(text)
"""
class RPPico:
    ser: serial.Serial
    _NO_IMAGES: int

    def __init__(self,COM:str):
        self.ser = serial.Serial(COM, 115200, timeout=2) # MAX 115200

    def Read(self):
        return self.ser.readline() # Read the data (looks for terminating character '/r/n')

    def Write(self, text: str= ""):
        self.ser.write(text)
    
    ## COMMANDS
    def Led_on(self):
        self.ser.write(b"LED_ON\n")
    def Led_off(self):
        self.ser.write(b"LED_OFF\n")
    def Number_of_images(self, no: int):
        self._NO_IMAGES = no
        text = "N_"+ str(no) + "\n"
        self.ser.write(bytes(text, "utf-8"))
    def Delay(self, d: int):
        # delay in us
        text = "D_"+ str(d) + "\n"
        self.ser.write(bytes(text, "utf-8"))
    def Start(self):
        self.ser.write(b"S_TRUE\n")
    def Info(self):
        self.ser.write(b"INFO\n")
        # There are 3 values to be printed
        for i in range(3):
            print(str(self.Read()).replace("\\r\\n",""))
    def Get_data(self) -> list:
        li: list = []
        self.ser.write(b"GD\n")
        for i in range(self._NO_IMAGES):
            li.append(self.Read())
        return li
    def Test(self) -> str:
        self.ser.write(b"TEST\n")
        return self.Read()


    

def save_data(li : list, file_name: str):
    with open(file_name+'.csv', 'w') as f:
    # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow([str(i).replace("b","").replace("\\r","").replace("\\n","").replace("'","") for i in li])


def main():
    data: list = []
    rp = RPPico("COM7")
    start = time.time()
    con = True
    i = 0
    rp.Number_of_images(100)
    d: str =""
    while(con):
        d = rp.Test()
        print(d)
        if(len(d) != 0):
            con = False
            print(d)

    print(data)
    """
    while(con ):
        text = ar.Read()
        end = time.time()
        if(len(text) != 0):
            data.append(text)
        if(end-start > 20):
            con = False
    save_data(data)
    """

