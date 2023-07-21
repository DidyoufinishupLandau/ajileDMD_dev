# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1  2023

Initially it was created to test main function, but
    later it became a script to install needed packages

@author: Alex Kedziora
"""

import sys
import subprocess

# implement pip as a subprocess:
"""subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'opencv-python'])"""
#subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
#'pyserial'])
#subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
#'ipykernel'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'matplotlib'])
"""
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'configdict'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'scipy'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'numpy'])"""