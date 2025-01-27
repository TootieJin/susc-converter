import os
import sys
from susc import sus, usc
from tkinter import filedialog


path = filedialog.askopenfilename(filetypes=[("譜面ファイル", "*.usc"), ("譜面ファイル", "*.sus")])

if path == "":
    sys.exit()

dir = os.path.dirname(path)
filename = os.path.basename(path).split(".")[0]

if path.endswith(".usc"):
    with open(path) as f:
        score = usc.load(f)
    score.shift()
    sus.export(f"{dir}/{filename}.sus", score)
elif path.endswith(".sus"):
    with open(path) as f:
        score = sus.load(f)