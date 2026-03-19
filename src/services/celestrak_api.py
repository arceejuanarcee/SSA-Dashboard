import requests
from collections import Counter
import streamlit as st

URLS = [
    "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=json",
    "https://celestrak.org/NORAD/elements/gp.php?GROUP=leo&FORMAT=json",
    "https://celestrak.org/NORAD/elements/active.txt"
]


def infer_country(name):
    name = name.upper()

    if "STARLINK" in name:
        return "US"
    if "ONEWEB" in name:
        return "UK"
    if "COSMOS" in name:
        return "RU"
    if "YAOGAN" in name or "BEIDOU" in name:
        return "CN"

    return "OTHER"


@st.cache_data(ttl=600)
def get_active_leo_by_country(limit=10):
    data = None
    last_error = None

    for url in URLS:
        try:
            resp = requests.get(url, timeout=8)

            if resp.status_code != 200:
                last_error = f"{url} failed ({resp.status_code})"
                continue

            if "json" in url:
                data = resp.json()

            else:
                # fallback parsing (TLE text)
                lines = resp.text.splitlines()
                data = []

                for i in range(0, len(lines), 3):
                    try:
                        name = lines[i].strip()
                        line2 = lines[i+2]
                        mm = float(line2[52:63])
                        data.append({
                            "OBJECT_NAME": name,
                            "MEAN_MOTION": mm
                        })
                    except:
                        continue

            if data:
                break

        except Exception as e:
            last_error = str(e)
            continue

    if not data:
        return [], [], f"All sources failed: {last_error}"

    countries = []

    for obj in data:
        try:
            mm = float(obj.get("MEAN_MOTION", 0))
            name = obj.get("OBJECT_NAME", "")

            if mm > 11:
                countries.append(infer_country(name))

        except:
            continue

    if not countries:
        return [], [], "No valid LEO data"

    counter = Counter(countries)
    top = counter.most_common(limit)

    labels = [c[0] for c in top]
    values = [c[1] for c in top]

    return labels, values, None