import pickle
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox


def remove_crops(win, choice_combo):
    if not choice_combo.get():
        CTkMessagebox(message="작물을 선택하여 주십시오", icon="warning", option_1="Ok")
    with open("./datas/crops.pkl", "rb") as f:
        crops = pickle.load(f)
    choice = choice_combo.get()
    del crops[choice]
    with open("./datas/crops.pkl", "wb") as f:
        pickle.dump(crops, f)
        f.truncate()
    choice_combo.set("작물 선택택")
    win.destroy()
