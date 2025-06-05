from config import crop_db
import datetime


def add_crop(crops, name, manager):
    if name in crop_db:

        sowing = crop_db[name]["파종"]
        harvest = crop_db[name]["수확"]
        water_cycle = crop_db[name]["급수주기"]
        crops[name] = {
            "담당자": manager,
            "파종일": sowing,
            "수확일": harvest,
            "급수주기": water_cycle,
            "급수일": datetime.date.today()
        }
        print(f"{name} 추가 완료! 담당자: {manager}")
    else:
        print("등록되지 않은 작물입니다. DB에 추가하세요.")
