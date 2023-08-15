import re
from tkinter import *
from tkinter import ttk
import os
import winsound
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as md

# def replace_last(string, delimiter, replacement):
#     start, _, end = string.rpartition(delimiter)
#     return start + replacement + end

# for count, filename in enumerate(os.listdir('Audio\sentences')):
#     dst = filename.replace(' q-', '_q-')
#     src = f"Audio\sentences/{filename}"
#     dst = f"Audio\sentences/{dst}"
#     os.rename(src, dst)

# for count, filename in enumerate(os.listdir('Audio\sentences')):
#     if count % 2 == 0:
#         sentence = filename.removesuffix('.wav').rstrip('fm').replace('_q_', '?').replace('_',' ').rstrip(' ')
#         print(f'"{sentence}",')

import pandas as pd

data = {
  "Students": ["Ray", "John", "Mole", "Smith", "Jay", "Milli", "Tom", "Rick"],
  "Subjects": ["Maths", "Economics", "Science", "Maths", "Statistics", "Statistics", "Statistics", "Computers"],
  "Success" : [100, 50, 25, 50, 100, 50, 25, 50],
  "Date" : ["2023-07-16 12:17:50.772165", "2023-07-18 10:59:52.955963", "2023-07-18 11:02:16.626525", "2023-07-18 11:05:41.217347", "2023-07-18 11:10:40.471263", "2023-08-05 10:02:12.737530", "2023-08-05 10:11:14.005579", "2023-08-05 10:15:52.131655"]
}

#load data into a DataFrame object:
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = df['Date'].dt.date
date = datetime(year=2023, month=7, day=16).date()
dates = df['Date'][0]
n_data = df[df['Date'] == date]
print(n_data.iloc[0]['Subjects'])

