import requests
from datetime import datetime
from collections import defaultdict


def safe_json(url):
    try:
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            return []

        return r.json()
    except:
        return []


def get_kp_history_and_forecast():
    hist_url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
    forecast_url = "https://services.swpc.noaa.gov/json/planetary_k_index_3d.json"

    hist = safe_json(hist_url)
    forecast = safe_json(forecast_url)

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

    if not data:
        return [], []

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


def get_kp_index():
    data = get_kp_history_and_forecast()

    if not data:
        return {"kp": "N/A", "status": "No Data"}

    latest = data[-1][1]

    if latest < 3:
        status = "Quiet"
    elif latest < 5:
        status = "Unsettled"
    elif latest < 7:
        status = "Storm"
    else:
        status = "Severe Storm"

    return {"kp": latest, "status": status}