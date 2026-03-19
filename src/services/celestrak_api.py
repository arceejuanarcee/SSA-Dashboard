import json
from collections import Counter
import streamlit as st


@st.cache_data(ttl=600)
def get_active_leo_by_country(limit=10):
    try:
        with open("data/sat_data.json", "r") as f:
            data = json.load(f)

        countries = []

        for obj in data:
            try:
                mm = float(obj.get("MEAN_MOTION", 0))

                if mm > 11:
                    country = obj.get("COUNTRY") or "UNK"
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

    except Exception as e:
        return [], [], str(e)