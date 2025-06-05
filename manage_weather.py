import requests
import datetime
import time
import json
from config import API_KEY, CITY_NAME, nx,ny

# -----------------------------
# 간단 날씨 조회 (OpenWeather API 사용 예정)
# -----------------------------

def get_weather():
    date = (datetime.today() - time.timedelta(hours=1))
    base_date = date.strftime("%Y%m%d") # 발표 일자
    base_time = date.strftime("%H00") # 발표 시간
    url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst?serviceKey={API_KEY}&numOfRows=12&pageNo=1&dataType=json&base_date={base_date}&base_time={base_time}&nx={nx}&ny={ny}"
    try:
        response = requests.get(url)
        data = json.loads(response.text)
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        print(f"현재 {CITY_NAME} 날씨: {weather}, 온도: {temp}°C")
    except Exception as e:
        print("날씨 정보를 불러올 수 없습니다:", e)