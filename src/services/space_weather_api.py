import requests
from datetime import datetime
from collections import defaultdict


def get_kp_history_and_forecast():
    hist_url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
    forecast_url = "https://services.swpc.noaa.gov/json/planetary_k_index_3d.json"

    hist = requests.get(hist_url, timeout=10).json()
    forecast = requests.get(forecast_url, timeout=10).json()

    combined = []

    for row in hist[-200:]:
        try:
            combined.append((row["time_tag"], float(row["kp_index"])))
        except:
            continue

    for row in forecast:
        try:
            combined.append((row["time_tag"], float(row["kp_index"])))
        except:
            continue

    return combined


def get_daily_kp():
    data = get_kp_history_and_forecast()

    daily = defaultdict(list)

    for t, v in data:
        try:
            dt = datetime.fromisoformat(t.replace("Z", ""))
            day = dt.strftime("%b %d")
            daily[day].append(v)
        except:
            continue

    days = list(daily.keys())
    values = [sum(v)/len(v) for v in daily.values()]

    return days, values