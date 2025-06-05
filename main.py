import datetime # 시간 정보
import webbrowser # url open
import time # 시간 정보
import customtkinter as ctk

from manage_crops import add_crop
from manage_weather import get_weather
from config import add_db

crops={}

ctk.set_appearance_mode("Dark")  # 다크 모드 설정 (System, Light, Dark)
ctk.set_default_color_theme("dark-blue")  # 테마 설정 (blue, dark-blue, green)

root = ctk.CTk()
root.geometry("800x600")
root.title("정미숙 진로상담선생님")
label = ctk.CTkLabel(root, text="garden.py", font=("Arial", 20))
label.pack(pady=20) # pady: 위아래 여백

def on_click_0():
    url='https://www.nongsaro.go.kr/portal/ps/psb/psbl/workScheduleLst.ps?menuId=PS00087'
    webbrowser.open(url)

button0 = ctk.CTkButton(root, text="0. 농사로 홈페이지 바로가기", command=on_click_0)
button0.pack(pady=10)

def on_click_1():
    url='https://www.nongsaro.go.kr/portal/ps/psb/psbl/workScheduleLst.ps?menuId=PS00087'
    webbrowser.open(url)

button1 = ctk.CTkButton(root, text="0. 농사로 홈페이지 바로가기", command=on_click_1)
button1.pack(pady=10)
root.mainloop()

# -----------------------------
# 급수 알림
# -----------------------------
def check_watering():
    today = datetime.date.today()
    for name, info in crops.items():
        last_watered = info['급수일']
        delta = (today - last_watered).days
        if delta >= info['급수주기']:
            print(f"[급수 알림] {name}에 물 줄 시간입니다! (담당자: {info['담당자']})")
            crops[name]['급수일'] = today


# -----------------------------
# 프로그램 메뉴
# -----------------------------

def main():
    # schedule.every().day.at("08:00").do(check_watering)

    while True:
        print("\n[텃밭 관리 프로그램]")
        print("0. 농사로 작물 정보 바로가기")
        print("1. 작물 추가")
        print("2. DB 추가")
        print("3. 현재 등록된 작물 보기")
        print("4. 날씨 확인")
        print("5. 수동 알림 체크")
        print("6. 종료")

        choice = input("선택하세요: ")

        if choice == '0':
            url='https://www.nongsaro.go.kr/portal/ps/psb/psbl/workScheduleLst.ps?menuId=PS00087'
            webbrowser.open(url)

        elif choice == '1': # 작물 현황에 작물 추가
            name = input("작물 이름 입력: ")
            manager = input("담당자 이름 입력: ")
            add_crop(crops, name, manager)

        elif choice == '2': #crop, sowing, harvest, water_cycle 받아서 DB를 추가 
            name = input("작물 이름 입력: ")
            sowing = input("파종 시기 입력: ")
            harvest = input("수확일 입력:")
            water_cycle = int(input("급수 주기: "))
            add_db(name, sowing, harvest, water_cycle)

            
        elif choice == '3':
            for crop, info in crops.items():
                print(f"{crop} - 담당자: {info['담당자']}, 파종: {info['파종일']}, 수확: {info['수확일']}, 사진 수: {len(info['사진'])}")

        elif choice == '4':
            get_weather()

        elif choice == '5':
            check_watering()

        elif choice == '6':
            print("프로그램 종료.")
            break

        else:
            print("잘못된 입력입니다.")

        time.sleep(1)

if __name__ == "__main__":
    main()
