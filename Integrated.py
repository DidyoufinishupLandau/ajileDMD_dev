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

class DMD_Pico:
    _dmd: object
    _pico: object

    def __init__(self,Pico_COM: str):
        self._pico = pico.RPPico(Pico_COM)
        self._dmd = dmd.DMD()
    
    # Sets the repetition of the DMD's sequence: 0(=infinity)
    def Set_repetition(self,rep:int=1) -> None:
        self._dmd.set_main_repetition(rep)
