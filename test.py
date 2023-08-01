import re
from tkinter import *
from tkinter import ttk
import os
import winsound
from datetime import datetime

# for count, filename in enumerate(os.listdir('Audio\words')):
#     dst = filename.lstrip("1234568790_")
#     dst = dst.removeprefix("margo_heston__")
#     src = f"Audio\words/{filename}"
#     dst = f"Audio\words/{dst}"
#     os.rename(src, dst)

for count, filename in enumerate(os.listdir('Audio\words')):
    if count % 2 == 0:
        print(filename.split("-")[0])
