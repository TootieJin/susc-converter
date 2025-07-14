import os
import sys
from susc import sus, usc
from tkinter import filedialog


path = filedialog.askopenfilename(filetypes=[("譜面ファイル", "*.usc"), ("譜面ファイル", "*.sus")])

if path == "":
    sys.exit()

dir = os.path.dirname(path)
filename = os.path.basename(path).split(".")[0]

try:
    if path.endswith(".usc"):

        print("uscをsusに変換します。\n", flush=True)
        with open(path) as f:
            print("uscデータを変換しています...", end="", flush=True)
            score = usc.load(f)
            print(" \033[32mOK\033[0m", flush=True)
            
        print("フェード無し用のガイド中継点を追加しています...", end="", flush=True)
        score.add_point_without_fade()
        print(" \033[32mOK\033[0m", flush=True)
        
        print("重なっているノーツを修正しています...", end="", flush=True)
        score.shift()
        print(" \033[32mOK\033[0m", flush=True)
        
        print("susファイルを出力しています...", end="", flush=True)
        sus.export(f"{dir}/{filename}.sus", score)
        print(" \033[32mOK\033[0m", flush=True)
        
        print("\n変換が終了しました。")
        print("保存先：", f"{dir}/{filename}.sus")
        
    elif path.endswith(".sus"):
        
        print("susをuscに変換します。\n", flush=True)
        with open(path) as f:
            print("susデータを変換しています...", end="", flush=True)
            score = sus.load(f)
            print(" \033[32mOK\033[0m", flush=True)
        
        print("uscファイルを出力しています...", end="", flush=True)
        usc.export(f"{dir}/{filename}.usc", score)
        print(" \033[32mOK\033[0m", flush=True)
    
        print("\n変換が終了しました。")
        print("保存先：", f"{dir}/{filename}.usc")
    
except Exception as e:
    print("\nエラーが発生しました。")
    print("エラー内容：", e)
    
finally:
    input("\nEnterキーでウィンドウを閉じます...")