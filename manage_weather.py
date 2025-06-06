import requests
import datetime
import time
import json
from bisect import bisect_left
from config import API_KEY, NX, NY, TIME_LIST

# -----------------------------
# 간단 날씨 조회 (기상청 API 사용 예정)
# -----------------------------


def get_weather():
    date = datetime.today() - time.timedelta(hours=3)
    base_date = date.strftime("%Y%m%d")  # 발표 일자
    base_time = TIME_LIST[bisect_left(TIME_LIST, date.strftime("%H00"))]  # 발표 시간
    url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?serviceKey={API_KEY}&numOfRows=14&pageNo=72&dataType=json&base_date={base_date}&base_time={base_time}&nx={NX}&ny={NY}"
    respons = requests.get(url)
    if respons.status_code != 200:
        print("날씨 정보를 불러오는 데 실패했습니다.")
        return -1
    data = json.loads(respons.text)
    if data["response"]["header"]["resultCode"] != "00":
        print("날씨 정보를 불러오는 데 실패했습니다.")
        return -1
