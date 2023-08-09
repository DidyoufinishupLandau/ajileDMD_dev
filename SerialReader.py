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
    ser: serial.Serial()
    _NO_IMAGES: int

    def __init__(self, COM:str):
        self.ser = serial.Serial(COM, 128000, xonxoff=True) # MAX 128000

    def Read(self):
        ser_bytes = self.ser.readline()
        return str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8")) # Read the data (looks for terminating character '/r/n')

    def Write(self, text: str= ""):
        self.ser.write(text)
    
    ## COMMANDS
    def Led_on(self):
        self.ser.write(b"LED_ON\n")
        
    def Led_off(self):
        self.ser.write(b"LED_OFF\n")

    def Number_of_images(self, no: int):
        self._NO_IMAGES = no
        text = "_N_"+ str(no) + "\n"
        self.ser.write(bytes(text, "utf-8"))

    def Delay(self, d: int):
        # delay in us
        text = "_D_"+ str(d) + "\n"
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
        self.ser.write(b"_GD_\n")
        i=0
        time.sleep(0.001)

        while(True):
            text = self.Read()
            if("END" in text):
                return li
            else:
                li.append(text)

    def Reset(self):
        self.ser.write(b"RESTART\n")
        
    def Test(self) -> str:
        self.ser.write(b"TEST\n")
        return self.Read()
    
    # Check if is ready to acquire the data
    def Is_Ready(self) -> bool:
        self.ser.write(b"_DR_\n")
        ret = self.Read()
        if("READY" in ret):
            return True
        else:
            return False



    

def save_data(li : list, file_name: str):
    with open(".\\data\\"+file_name+'.csv', 'w') as f:
    # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow([str(i).replace("b","").replace("\\r","").replace("\\n","").replace("'","") for i in li])
