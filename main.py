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

        print("uscをsusに変換します。\n")
        with open(path) as f:
            print("uscデータを変換しています...", end="")
            score = usc.load(f)
            print(" \033[32mOK\033[0m")
            
        print("フェード無し用のガイド中継点を追加しています...", end="")
        score.add_point_without_fade()
        print(" \033[32mOK\033[0m")
        
        print("重なっているノーツを修正しています...", end="")
        score.shift()
        print(" \033[32mOK\033[0m")
        
        print("susファイルを出力しています...", end="")
        sus.export(f"{dir}/{filename}.sus", score)
        print(" \033[32mOK\033[0m")
        
        print("\n変換が終了しました。")
        print("保存先：", f"{dir}/{filename}.sus")
        
    elif path.endswith(".sus"):
        
        print("susをuscに変換します。\n")
        with open(path) as f:
            print("susデータを変換しています...", end="")
            score = sus.load(f)
            print(" \033[32mOK\033[0m")
        
        print("uscファイルを出力しています...", end="")
        usc.export(f"{dir}/{filename}.usc", score)
        print(" \033[32mOK\033[0m")
    
        print("\n変換が終了しました。")
        print("保存先：", f"{dir}/{filename}.usc")
    
except Exception as e:
    print("\nエラーが発生しました。")
    print("エラー内容：", e)
    
finally:
    input("\nEnterキーでウィンドウを閉じます...")