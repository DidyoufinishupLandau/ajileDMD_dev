# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1  2023

@author: Alex Kedziora
"""

import sys
import subprocess

# implement conda as a subprocess:

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'configdict'])