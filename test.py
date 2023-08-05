import re
from tkinter import *
from tkinter import ttk
import os
import winsound
from datetime import datetime

def replace_last(string, delimiter, replacement):
    start, _, end = string.rpartition(delimiter)
    return start + replacement + end

for count, filename in enumerate(os.listdir('Audio\sentences')):
    dst = filename.replace(' q-', '_q-')
    src = f"Audio\sentences/{filename}"
    dst = f"Audio\sentences/{dst}"
    os.rename(src, dst)

for count, filename in enumerate(os.listdir('Audio\sentences')):
    if count % 2 == 0:
        sentence = filename.removesuffix('.wav').rstrip('fm').replace('_q_', '?').replace('_',' ').rstrip(' ')
        print(f'"{sentence}",')
