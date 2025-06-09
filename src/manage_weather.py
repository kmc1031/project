import requests
import urllib.parse
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

from bisect import bisect_left
from config import API_KEY, NX, NY, TIME_LIST

# -----------------------------
# 간단 날씨 조회 (기상청 API 사용 예정)
# -----------------------------


def get_weather():
    # 2) 서비스키 URL 인코딩 (guide 요구사항) :contentReference[oaicite:1]{index=1}
    encoded_key = urllib.parse.quote_plus(API_KEY)

    # 3) 최신 발표시각 계산
    def get_latest_base(dt):
        slots = [2, 5, 8, 11, 14, 17, 20, 23]
        hour = dt.hour
        candidates = [h for h in slots if h <= hour]
        if not candidates:
            base_date = (dt - timedelta(days=1)).strftime("%Y%m%d")
            base_time = "2300"
        else:
            h = max(candidates)
            base_date = dt.strftime("%Y%m%d")
            base_time = f"{h:02d}00"
        return base_date, base_time

    now = datetime.now()  # Asia/Seoul 로컬타임
    base_date, base_time = get_latest_base(now)

    # 4) API 호출 (serviceKey는 이미 URL에 포함)
    base_url = (
        "http://apis.data.go.kr/1360000/"
        "VilageFcstInfoService_2.0/getVilageFcst"
        f"?serviceKey={encoded_key}"
    )
    params = {
        "pageNo": "1",
        "numOfRows": "1000",
        "dataType": "JSON",  # JSON 요청
        "base_date": base_date,
        "base_time": base_time,
        "NX": NX,
        "NY": NY,
    }

    resp = requests.get(base_url, params=params)
    resp.raise_for_status()

    # 5) 응답 파싱: JSON 우선, 실패 시 XML
    try:
        result = resp.json()
        items = result["response"]["body"]["items"]["item"]
    except ValueError:
        # JSON 디코드 실패하면 XML로 파싱
        root = ET.fromstring(resp.text)
        # <item> 요소들을 모두 모아서 dict 형태로 처리
        items = []
        for item_el in root.findall(".//item"):
            it = {child.tag: child.text for child in item_el}
            items.append(it)

    # 6) ‘강수형태(PTY)’ 항목에서 비(0 이외) 수집
    rain_times = []
    for it in items:
        if it.get("category") == "PTY" and it.get("fcstValue") not in (None, "0"):
            dt_str = it["fcstDate"] + it["fcstTime"]
            rain_times.append(datetime.strptime(dt_str, "%Y%m%d%H%M"))

    # 7) 결과 출력
    if not rain_times:
        print("향후 일주일 내에 비 예보는 없습니다.")
    else:
        print("향후 일주일 내 비 예보 시점:")
        for t in sorted(set(rain_times)):
            print("  -", t.strftime("%Y-%m-%d %H:%M"))
