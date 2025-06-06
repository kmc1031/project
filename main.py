import datetime  # 시간 정보
import webbrowser  # url open
import time  # 시간 정보
import customtkinter as ctk

from manage_crops import add_crop
from manage_weather import get_weather
from config import add_db

crops = {}

ctk.set_appearance_mode("Dark")  # 다크 모드 설정 (System, Light, Dark)
ctk.set_default_color_theme("dark-blue")  # 테마 설정 (blue, dark-blue, green)

root = ctk.CTk()
root.geometry("800x600")
root.title("정미숙 진로상담선생님")
title = ctk.CTkLabel(root, text="garden.py", font=("Arial", 20))
title.pack(pady=20)  # pady: 위아래 여백


def on_click_0():
    url = "https://www.nongsaro.go.kr/portal/ps/psb/psbl/workScheduleLst.ps?menuId=PS00087"
    webbrowser.open(url)


button0 = ctk.CTkButton(root, text="0. 농사로 홈페이지 바로가기", command=on_click_0)
button0.pack(pady=10)


def add_crop_and_close(name_entry, manager_entry, input_win):
    global crops  # 전역 변수 사용
    if not name_entry.get() or not manager_entry.get():
        print("작물 이름과 담당자를 모두 입력해야 합니다.")
        ctk.CTkMessageBox.show_error(
            "오류", "작물 이름과 담당자를 모두 입력해야 합니다."
        )
        return
    # 작물 이름과 담당자 가져오기
    global crops
    from manage_crops import add_crop  # 모듈에서 함수 가져오기

    if not isinstance(crops, dict):
        crops = {}
    # 작물 이름과 담당자 입력
    # crops 딕셔너리에 추가
    add_crop(crops, name_entry.get(), manager_entry.get())
    # print(f"{name_entry.get()} 추가 완료! 담당자: {manager_entry.get()}")
    # 입력 필드 초기화
    name_entry.delete(0, ctk.END)
    manager_entry.delete(0, ctk.END)
    print(f"{name_entry.get()} 추가 완료! 담당자: {manager_entry.get()}")

    input_win.destroy()  # 입력 창 닫기


def on_click_1():
    input_win = ctk.CTkToplevel(root)
    input_win.attributes("-topmost", True)
    input_win.geometry("400x200")
    input_win.title("작물 추가")
    label = ctk.CTkLabel(input_win, text="작물 이름과 담당자를 입력하세요")
    label.pack(pady=10)
    name_entry = ctk.CTkEntry(input_win, placeholder_text="작물 이름")
    name_entry.pack(pady=5)
    manager_entry = ctk.CTkEntry(input_win, placeholder_text="담당자 이름")
    manager_entry.pack(pady=5)
    add_button = ctk.CTkButton(
        input_win,
        text="추가",
        command=lambda: add_crop_and_close(name_entry, manager_entry, input_win),
    )
    add_button.pack(pady=10)


button1 = ctk.CTkButton(root, text="1. 작물 추가", command=on_click_1)
button1.pack(pady=10)


def add_db_and_close(
    name_entry, sowing_entry, harvest_entry, water_cycle_entry, input_win
):
    if (
        not name_entry.get()
        or not sowing_entry.get()
        or not harvest_entry.get()
        or not water_cycle_entry.get()
    ):
        print("모든 필드를 입력해야 합니다.")
        ctk.CTkMessageBox.show_error("오류", "모든 필드를 입력해야 합니다.")
        return

    # 작물 정보 가져오기
    name = name_entry.get()
    sowing = sowing_entry.get()
    harvest = harvest_entry.get()
    water_cycle = int(water_cycle_entry.get())
    # DB에 추가
    add_db(name, sowing, harvest, water_cycle)
    # print(f"{name} 추가 완료! 파종: {sowing}, 수확: {harvest}, 급수 주기: {water_cycle}일")
    # 입력 필드 초기화
    name_entry.delete(0, ctk.END)
    sowing_entry.delete(0, ctk.END)
    harvest_entry.delete(0, ctk.END)
    water_cycle_entry.delete(0, ctk.END)

    input_win.destroy()  # 입력 창 닫기


def on_click_2():
    input_win = ctk.CTkToplevel(root)
    input_win.attributes("-topmost", True)
    input_win.geometry("400x200")
    input_win.title("DB 추가")
    label = ctk.CTkLabel(input_win, text="작물 정보 입력")
    label.pack(pady=10)
    name_label = ctk.CTkLabel(input_win, text="작물 이름:")
    name_label.pack(pady=5)
    name_entry = ctk.CTkEntry(input_win, placeholder_text="작물 이름")
    name_entry.pack(pady=5)
    sowing_label = ctk.CTkLabel(input_win, text="파종 시기:")
    sowing_label.pack(pady=5)
    sowing_entry = ctk.CTkEntry(input_win, placeholder_text="파종 시기")
    sowing_entry.pack(pady=5)
    harvest_label = ctk.CTkLabel(input_win, text="수확일:")
    harvest_label.pack(pady=5)
    harvest_entry = ctk.CTkEntry(input_win, placeholder_text="수확일")
    harvest_entry.pack(pady=5)
    water_cycle_label = ctk.CTkLabel(input_win, text="급수 주기 (일):")
    water_cycle_label.pack(pady=5)
    water_cycle_entry = ctk.CTkEntry(input_win, placeholder_text="급수 주기")
    water_cycle_entry.pack(pady=5)
    add_button = ctk.CTkButton(
        input_win,
        text="추가",
        command=lambda: add_db_and_close(
            name_entry,
            sowing_entry,
            harvest_entry,
            water_cycle_entry,
            input_win,
        ),
    )
    add_button.pack(pady=10)


button2 = ctk.CTkButton(root, text="2. DB 추가", command=on_click_2)
button2.pack(pady=10)


def on_click_3():
    win = ctk.CTkToplevel(root)
    win.attributes("-topmost", True)
    win.geometry("600x400")
    win.title("현재 등록된 작물")
    label = ctk.CTkLabel(win, text="현재 등록된 작물 목록")
    label.pack(pady=10)
    crops_list = ctk.CTkScrollableFrame(win, width=500, height=300)
    crops_list.pack(pady=10, padx=10, fill="both", expand=True)
    crops_list.configure(
        fg_color="transparent",  # 투명 배경
        scrollbar_button_color="gray",  # 스크롤바 버튼 색상
        scrollbar_button_hover_color="lightgray",  # 스크롤바 버튼 호버 색상
        scrollbar_fg_color="gray",  # 스크롤바 배경 색상
        label_text_color="white",  # 레이블 텍스트 색상
        label_fg_color="transparent",  # 레이블 배경 색상
        label_text="작물 목록",  # 레이블 텍스트
        label_font=("Arial", 14),  # 레이블 폰트
        label_anchor="w",  # 레이블 앵커 위치
    )
    for crop, info in crops.items():
        crop_info = f"{crop} - 담당자: {info['담당자']}, 파종: {info['파종일']}, 수확: {info['수확일']}"
        crop_label = ctk.CTkLabel(crops_list, text=crop_info, anchor="w")
        crop_label.pack(pady=5, padx=10, fill="x")


button3 = ctk.CTkButton(root, text="3. 현재 등록된 작물 보기", command=on_click_3)
button3.pack(pady=10)


def on_click_4():
    win = ctk.CTkToplevel(root)
    win.attributes("-topmost", True)
    win.geometry("400x300")
    win.title("날씨 정보")
    label = ctk.CTkLabel(win, text="현재 날씨 정보")
    label.pack(pady=10)
    # 날씨 정보 가져오기
    from manage_weather import get_weather  # 모듈에서 함수 가져오기

    # 날씨 정보를 가져와서 출력
    # get_weather 함수는 날씨 정보를 문자열로 반환
    # 만약 오류가 발생하면 -1을 반환
    weather_info = get_weather()
    if weather_info != -1:
        print("\n[현재 날씨 정보]")
        print(weather_info)


button4 = ctk.CTkButton(root, text="4. 날씨 확인", command=on_click_4)
button4.pack(pady=10)


# -----------------------------
# 급수 알림
# -----------------------------
def check_watering():
    today = datetime.date.today()
    for name, info in crops.items():
        last_watered = info["급수일"]
        delta = (today - last_watered).days
        if delta >= info["급수주기"]:
            yield (f"[급수 알림] {name}에 물 줄 시간입니다! (담당자: {info['담당자']})")
            crops[name]["급수일"] = today


def on_click_5():
    win = ctk.CTkToplevel(root)
    win.attributes("-topmost", True)
    win.geometry("400x200")
    win.title("수동 알림 체크")
    label = ctk.CTkLabel(win, text="수동 알림 체크")
    label.pack(pady=10)
    # 수동 알림 체크
    watering_info = list(check_watering())
    for info in watering_info:
        info_label = ctk.CTkLabel(win, text=info)
        info_label.pack(pady=5)
    if not watering_info:
        no_info_label = ctk.CTkLabel(win, text="현재 급수 알림이 없습니다.")
        no_info_label.pack(pady=5)


button5 = ctk.CTkButton(root, text="5. 수동 알림 체크", command=on_click_5)
button5.pack(pady=10)


def on_click_6_yes(win_tmp):
    print("프로그램을 종료합니다.")
    win_tmp.destroy()  # 창 닫기
    root.quit()  # tkinter GUI 종료


def on_click_6():
    win_tmp = ctk.CTkToplevel(root)
    win_tmp.attributes("-topmost", True)
    win_tmp.geometry("300x200")
    win_tmp.title("종료 확인")
    label = ctk.CTkLabel(win_tmp, text="프로그램을 종료하시겠습니까?")
    label.pack(pady=20)
    yes_button = ctk.CTkButton(
        win_tmp, text="예", command=lambda: on_click_6_yes(win_tmp)
    )
    yes_button.pack(pady=5)
    no_button = ctk.CTkButton(win_tmp, text="아니오", command=win_tmp.destroy)
    no_button.pack(pady=5)


button6 = ctk.CTkButton(root, text="6. 종료", command=on_click_6)
button6.pack(pady=10)
# -----------------------------
# tkinter GUI 실행
# -----------------------------

root.mainloop()


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

        if choice == "0":
            url = "https://www.nongsaro.go.kr/portal/ps/psb/psbl/workScheduleLst.ps?menuId=PS00087"
            webbrowser.open(url)

        elif choice == "1":  # 작물 현황에 작물 추가
            name = input("작물 이름 입력: ")
            manager = input("담당자 이름 입력: ")
            add_crop(crops, name, manager)

        elif choice == "2":  # crop, sowing, harvest, water_cycle 받아서 DB를 추가
            name = input("작물 이름 입력: ")
            sowing = input("파종 시기 입력: ")
            harvest = input("수확일 입력:")
            water_cycle = int(input("급수 주기: "))
            add_db(name, sowing, harvest, water_cycle)

        elif choice == "3":
            for crop, info in crops.items():
                print(
                    f"{crop} - 담당자: {info['담당자']}, 파종: {info['파종일']}, 수확: {info['수확일']}"
                )

        elif choice == "4":
            get_weather()

        elif choice == "5":
            check_watering()

        elif choice == "6":
            print("프로그램 종료.")
            break

        else:
            print("잘못된 입력입니다.")

        time.sleep(1)


if __name__ == "__main__":
    main()
