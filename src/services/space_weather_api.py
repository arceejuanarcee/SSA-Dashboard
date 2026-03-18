import requests

NOAA_KP_NOW = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
NOAA_KP_FORECAST = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json"


def get_kp_index():
    try:
        res = requests.get(NOAA_KP_NOW, timeout=5)
        data = res.json()
        latest = data[-1]
        kp = float(latest[1])

        return {
            "kp": kp,
            "status": classify_kp(kp)
        }

    except:
        return {"kp": "N/A", "status": "Unavailable"}


def get_kp_forecast():
    try:
        res = requests.get(NOAA_KP_FORECAST, timeout=5)
        data = res.json()

        times = []
        values = []

        for row in data[1:15]:  # next ~14 points
            times.append(row[0])
            values.append(float(row[1]))

        return times, values

    except:
        return [], []


def classify_kp(kp):
    if kp == "N/A":
        return "Unavailable"

    if kp < 4:
        return "Quiet"
    elif kp < 5:
        return "Active"
    elif kp < 6:
        return "G1"
    elif kp < 7:
        return "G2"
    elif kp < 8:
        return "G3"
    elif kp < 9:
        return "G4"
    else:
        return "G5"