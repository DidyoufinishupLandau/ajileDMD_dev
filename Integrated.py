# -*- coding: utf-8 -*-
# -*- python=3.8.x
"""
Created on 08/08/2023

This file creates a class that combines DMD and Pico into one

@author: Alex Kedziora
"""

import SerialReader as pico
import DMDinterface as dmd
import pattern_generator as pg
import Plotter
import time

class DMD_Pico:
    global _dmd
    global _pico

    def __init__(self,Pico_COM: str):
        self._pico = pico.RPPico(Pico_COM)
        self._dmd = dmd.DMD()
    
    # Sets the repetition of the DMD's sequence: 0(=infinity)
    #def Set_repetition(self,rep:int=1) -> None:
    #    self._dmd.set_main_repetition(rep)

    # delay in us 
    def Set_delay(self, delay:int)-> None:
        self._pico.Delay(delay)

    # Shows all patterns available on PC
    def Show_patterns(self):
        self._dmd.show_patterns()
    
    # Add pattern to the project (frameTime doesn't matter when trigger is on)
    def Add_pattern(self,patternID : int, frameTime : int = 1) -> None:
        self._dmd.add_image_to_seq(patternID, frameTime)

    # Create project; repetition of the DMD's sequence: 0(=infinity)
    def Create_project(self, rep: int=1):
        self._pico.Number_of_images(self._dmd.create_project(rep))

    # Starts triggering and data taking (data is not sent to PC)
    def Run_trigger(self):
        self._dmd.run_trigger()
        self._pico.Start()

    # Starts triggering and data taking (data is sent to PC when operation is finished)
    def Run(self) -> list:
        self.Run_trigger()
        return self._pico.Get_data()
        
    def Save_data(self, data:list, file_name:str) -> None:
        pico.save_data(data, file_name)

    def Run_Save(self, file_name:str) -> None:
        self.Save_data(self.Run(), file_name)

    def Create_plot(data_name:str, pixel_size:int, image_name:str):
        Plotter.create_plot(data_name, pixel_size, image_name)


obj = DMD_Pico("COM7")
obj.Show_patterns()
obj.Add_pattern(7)
obj.Create_project()
print("Started")
start = time.time()
## Works till this moment
obj.Run_Save("Data_test_57_57")
end = time.time()
print(end - start)