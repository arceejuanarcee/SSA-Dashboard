import requests
from collections import Counter
import streamlit as st

BASE_URL = "https://www.space-track.org"


def spacetrack_login(identity, password):
    session = requests.Session()

    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    login_url = BASE_URL + "/ajaxauth/login"

    resp = session.post(
        login_url,
        data={"identity": identity, "password": password},
        headers=headers,
        timeout=20
    )

    if resp.status_code != 200:
        return None, "Login failed"

    if "Login" in resp.text:
        return None, "Invalid credentials or blocked"

    return session, None


@st.cache_data(ttl=600)
def get_active_leo_satellites_by_country(identity, password, limit=10):
    try:
        session, err = spacetrack_login(identity, password)

        if err:
            return [], [], err

        url = (
            BASE_URL +
            "/basicspacedata/query/class/satcat/"
            "DECAY/null/"
            "PERIOD/<225/"
            "format/json"
        )

        resp = session.get(url, timeout=30)

        if resp.status_code != 200:
            return [], [], f"Fetch failed: {resp.status_code}"

        if "<html>" in resp.text.lower():
            return [], [], "Blocked by Space-Track (HTML response)"

        data = resp.json()

        if not isinstance(data, list) or len(data) == 0:
            return [], [], "No data returned"

        countries = [obj.get("COUNTRY") or "UNK" for obj in data]

        counter = Counter(countries)
        top = counter.most_common(limit)

        labels = [c[0] for c in top]
        values = [c[1] for c in top]

        return labels, values, None

    except Exception as e:
        return [], [], str(e)