import requests
from collections import Counter
import streamlit as st

BASE_URL = "https://www.space-track.org"


def spacetrack_login(identity, password):
    session = requests.Session()

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    login_url = BASE_URL + "/ajaxauth/login"

    resp = session.post(
        login_url,
        data={"identity": identity, "password": password},
        headers=headers,
        timeout=20
    )

    if resp.status_code != 200:
        raise Exception(f"Login failed: {resp.status_code}")

    # 🚨 CRITICAL: detect failed login (Space-Track returns HTML login page)
    if "Login" in resp.text and "password" in resp.text:
        raise Exception("Space-Track login failed (bad credentials or blocked)")

    return session


@st.cache_data(ttl=600)
def get_active_leo_satellites_by_country(identity, password, limit=10):
    try:
        session = spacetrack_login(identity, password)

        url = (
            BASE_URL +
            "/basicspacedata/query/class/satcat/"
            "DECAY/null/"
            "PERIOD/<225/"
            "format/json"
        )

        resp = session.get(url, timeout=30)

        if resp.status_code != 200:
            raise Exception(f"Fetch failed: {resp.status_code}")

        # 🚨 detect if Space-Track returned HTML instead of JSON
        if "<html>" in resp.text.lower():
            raise Exception("Space-Track returned HTML (blocked or session expired)")

        data = resp.json()

        if not isinstance(data, list) or len(data) == 0:
            raise Exception("No valid satellite data")

        countries = [
            obj.get("COUNTRY") or "UNK"
            for obj in data
        ]

        counter = Counter(countries)
        top = counter.most_common(limit)

        labels = [c[0] for c in top]
        values = [c[1] for c in top]

        return labels, values

    except Exception as e:
        # 🔥 DEBUG OUTPUT (VERY IMPORTANT)
        return [], str(e)