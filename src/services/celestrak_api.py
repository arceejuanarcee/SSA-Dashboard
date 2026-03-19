import requests
import json
from collections import Counter
import streamlit as st
import os

LOCAL_PATH = "data/sat_data.json"

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

    return "OTHER"


@st.cache_data(ttl=600)
def get_active_leo_by_country(limit=10):
    data = None

    # 🔥 1. LOAD LOCAL FIRST (THIS FIXES YOUR ISSUE)
    if os.path.exists(LOCAL_PATH):
        try:
            with open(LOCAL_PATH, "r") as f:
                data = json.load(f)
        except Exception as e:
            return [], [], f"Local file error: {e}"

    # 🔥 2. ONLY TRY API IF LOCAL NOT AVAILABLE
    if data is None:
        try:
            resp = requests.get(URL, timeout=8)

            if resp.status_code != 200:
                return [], [], f"Fetch failed: {resp.status_code}"

            data = resp.json()

        except Exception as e:
            return [], [], f"API failed and no local fallback: {e}"

    if not isinstance(data, list) or len(data) == 0:
        return [], [], "Dataset empty"

    countries = []

    for obj in data:
        try:
            mm = float(obj.get("MEAN_MOTION", 0))
            name = obj.get("OBJECT_NAME", "")

            if mm > 11:
                country = obj.get("COUNTRY")

                if not country:
                    country = infer_country(name)

                countries.append(country)

        except:
            continue

    if not countries:
        return [], [], "No valid LEO data"

    counter = Counter(countries)
    top = counter.most_common(limit)

    labels = [c[0] for c in top]
    values = [c[1] for c in top]

    return labels, values, None