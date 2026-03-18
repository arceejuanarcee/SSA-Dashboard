import requests

NOAA_KP_URL = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"

def get_kp_index():
    try:
        response = requests.get(NOAA_KP_URL, timeout=5)
        data = response.json()

        latest = data[-1]
        kp = float(latest[1])

        return {
            "kp": kp,
            "status": classify_kp(kp)
        }

    except Exception:
        return {
            "kp": "N/A",
            "status": "Unavailable"
        }


def classify_kp(kp):
    if kp == "N/A":
        return "Unavailable"

    if kp < 4:
        return "Quiet"
    elif kp < 5:
        return "Active"
    elif kp < 6:
        return "Minor Storm (G1)"
    elif kp < 7:
        return "Moderate Storm (G2)"
    elif kp < 8:
        return "Strong Storm (G3)"
    elif kp < 9:
        return "Severe Storm (G4)"
    else:
        return "Extreme Storm (G5)"