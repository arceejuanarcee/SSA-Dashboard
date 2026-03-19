import requests
from collections import Counter
import streamlit as st

URL = "https://celestrak.org/pub/satcat.csv"


@st.cache_data(ttl=600)
def get_active_leo_by_country(limit=10):
    try:
        resp = requests.get(URL, timeout=30)

        if resp.status_code != 200:
            return [], [], f"Fetch failed: {resp.status_code}"

        lines = resp.text.splitlines()

        header = lines[0].split(",")

        idx_country = header.index("COUNTRY")
        idx_period = header.index("PERIOD")
        idx_status = header.index("STATUS")

        countries = []

        for row in lines[1:]:
            cols = row.split(",")

            try:
                status = cols[idx_status]
                period = float(cols[idx_period])

                # ACTIVE + LEO filter
                if status == "Active" and period > 0 and period < 225:
                    country = cols[idx_country] or "UNK"
                    countries.append(country)

            except:
                continue

        if not countries:
            return [], [], "No data after filtering"

        counter = Counter(countries)
        top = counter.most_common(limit)

        labels = [c[0] for c in top]
        values = [c[1] for c in top]

        return labels, values, None

    except Exception as e:
        return [], [], str(e)