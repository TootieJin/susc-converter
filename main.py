import os
import sys
from src import sus
from src import usc
from tkinter import filedialog


path = filedialog.askopenfilename(filetypes=[("譜面ファイル", "*.usc")])
if path == "":
    sys.exit()
    
dir = os.path.dirname(path)
file_name = os.path.basename(path).replace(".usc", "")

with open(path) as f:
    score = usc.load(f)

score.shift()

sus.export(f"{dir}/{file_name}.sus", score)