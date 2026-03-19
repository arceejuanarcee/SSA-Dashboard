import json
import os
from collections import Counter
import streamlit as st

LOCAL_PATH = "data/satcat.json"


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
    if not os.path.exists(LOCAL_PATH):
        return [], [], "satcat.json not found in data folder"

    try:
        with open(LOCAL_PATH, "r") as f:
            data = json.load(f)
    except Exception as e:
        return [], [], f"Failed to load satcat.json: {e}"

    if not isinstance(data, list) or len(data) == 0:
        return [], [], "Empty dataset"

    countries = []

    for obj in data:
        try:
            mm = float(obj.get("MEAN_MOTION", 0))
            name = obj.get("OBJECT_NAME", "")

            if mm > 11:
                country = obj.get("COUNTRY")

                if not country or country == "UNK":
                    country = infer_country(name)

                countries.append(country)

        except:
            continue

    if not countries:
        return [], [], "No LEO satellites after filtering"

    counter = Counter(countries)
    top = counter.most_common(limit)

    labels = [c[0] for c in top]
    values = [c[1] for c in top]

    return labels, values, None