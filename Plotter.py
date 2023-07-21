# -*- coding: utf-8 -*-
# -*- python=3.8.x
"""
Created on 21/07/2023

Heatmap plotter
Data is saved in csv file and is not ready for heatmap
    it needs to be segregated: i.e. using 19x19 pixels we need 1140/19 rows and 912/19 columns

@author: Alex Kedziora
"""

import numpy as np
import matplotlib.pyplot as plt
import csv 
from collections import deque

def heat_map(z : np.array):
    plt.imshow( z )
    plt.show()

def subtract(data):
    d1 = data[0::2]
    d2 = data[1::2]
    data: list = []
    for i in range(len(d2)):
        data.append(d2[i]-d1[i])

    return data

def separate_data(data: list, pixels_size : int) -> np.array:
    columns = int(912 / pixels_size)
    rows = int(1140 / pixels_size)
    array_row: list = []

    data_array = np.zeros((rows,columns))
    for r in range(rows):
        array_row.clear()
        for c in range(columns):
            data_array[r][c]  = float(data[rows*c + r])

    return data_array

def load_csv(path:str) -> list:
    with open(path, newline='') as f:
        reader = csv.reader(f)
        temp = list(reader)
    data : list = []
    for item in temp:
        data.append(float(item[0]))
    return data

data = load_csv("data_38_38.csv")
subtracted_data = subtract(data)
sorted = (separate_data(subtracted_data, 38))
heat_map(sorted)