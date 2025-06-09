import datetime
import pickle
import customtkinter as ctk


def add_crop(name, manager):
    with open("datas/db.pkl", "rb") as f:
        crop_db = pickle.load(f)

    with open("datas/crops.pkl", "rb") as f:
        crops = pickle.load(f)

    if name in crop_db:
        sowing = crop_db[name]["파종"]
        harvest = crop_db[name]["수확"]
        water_cycle = crop_db[name]["급수주기"]
        crops[name] = {
            "담당자": manager,
            "파종일": sowing,
            "수확일": harvest,
            "급수주기": water_cycle,
            "급수일": datetime.date.today(),
        }

        with open("datas/crops.pkl", "wb") as f:
            pickle.dump(crops, f)
        print(f"{name} 추가 완료! 담당자: {manager}")

    else:
        print("등록되지 않은 작물입니다. DB에 추가하세요.")
