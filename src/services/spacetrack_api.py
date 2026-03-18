import requests
from collections import Counter
import streamlit as st

BASE_URL = "https://www.space-track.org"


@st.cache_data(ttl=600)
def get_active_leo_satellites_by_country(identity, password, limit=10):
    try:
        session = requests.Session()

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.space-track.org/auth/login"
        }

        login_resp = session.post(
            BASE_URL + "/ajaxauth/login",
            data={
                "identity": identity,
                "password": password
            },
            headers=headers,
            timeout=30
        )

        if login_resp.status_code != 200:
            return [], [], f"Login failed: {login_resp.status_code}"

        if "failed" in login_resp.text.lower():
            return [], [], "Invalid credentials"

        query_url = (
            BASE_URL +
            "/basicspacedata/query/class/satcat/"
            "CURRENT/Y/"
            "format/json"
        )

        resp = session.get(query_url, headers=headers, timeout=30)

        if resp.status_code != 200:
            return [], [], f"Query failed: {resp.status_code}"

        if "<html" in resp.text.lower():
            return [], [], "Blocked by Space-Track"

        data = resp.json()

        if not isinstance(data, list) or len(data) == 0:
            return [], [], "Empty dataset"

        # 🔥 SIMPLE + ROBUST LEO FILTER
        filtered = []

        for obj in data:
            try:
                mm = float(obj.get("MEAN_MOTION", 0))

                # LEO condition ONLY
                if mm > 11:
                    filtered.append(obj)

            except:
                continue

        if len(filtered) == 0:
            return [], [], "No satellites passed LEO filter (unexpected)"

        countries = [
            obj.get("COUNTRY") or "UNK"
            for obj in filtered
        ]

        counter = Counter(countries)
        top = counter.most_common(limit)

        labels = [c[0] for c in top]
        values = [c[1] for c in top]

        return labels, values, None

    except Exception as e:
        return [], [], str(e)