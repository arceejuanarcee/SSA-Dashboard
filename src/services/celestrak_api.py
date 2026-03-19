import requests
from collections import Counter
import streamlit as st

URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=json"


@st.cache_data(ttl=600)
def get_active_leo_by_country(limit=10):
    try:
        resp = requests.get(URL, timeout=20)

        if resp.status_code != 200:
            return [], [], f"Fetch failed: {resp.status_code}"

        data = resp.json()

        if not isinstance(data, list) or len(data) == 0:
            return [], [], "Empty dataset"

        countries = []

        for obj in data:
            try:
                mm = float(obj.get("MEAN_MOTION", 0))

                # LEO filter
                if mm > 11:
                    country = obj.get("COUNTRY") or "UNK"
                    countries.append(country)

            except:
                continue

        if not countries:
            return [], [], "No LEO satellites found"

        counter = Counter(countries)
        top = counter.most_common(limit)

        labels = [c[0] for c in top]
        values = [c[1] for c in top]

        return labels, values, None

    except Exception as e:
        return [], [], str(e)