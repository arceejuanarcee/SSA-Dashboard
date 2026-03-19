import requests
from collections import Counter
import streamlit as st

URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=json"


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
    if "IRIDIUM" in name:
        return "US"
    if "GALILEO" in name:
        return "EU"

    return "OTHER"


@st.cache_data(ttl=600)
def get_active_leo_by_country(limit=10):
    try:
        resp = requests.get(URL, timeout=20)

        if resp.status_code != 200:
            return [], [], f"Fetch failed: {resp.status_code}"

        data = resp.json()

        countries = []

        for obj in data:
            try:
                mm = float(obj.get("MEAN_MOTION", 0))
                name = obj.get("OBJECT_NAME", "")

                if mm > 11:
                    country = infer_country(name)
                    countries.append(country)

            except:
                continue

        if not countries:
            return [], [], "No valid data"

        counter = Counter(countries)
        top = counter.most_common(limit)

        labels = [c[0] for c in top]
        values = [c[1] for c in top]

        return labels, values, None

    except Exception as e:
        return [], [], str(e)