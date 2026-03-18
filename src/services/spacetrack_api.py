import requests
from collections import Counter
import streamlit as st

BASE_URL = "https://www.space-track.org"


def spacetrack_login(identity, password):
    session = requests.Session()

    headers = {
        "User-Agent": "SSA-Dashboard/1.0",
    }

    login_url = BASE_URL + "/ajaxauth/login"

    resp = session.post(
        login_url,
        data={"identity": identity, "password": password},
        headers=headers,
        timeout=15
    )

    if resp.status_code != 200:
        raise Exception(f"Login failed: {resp.status_code}")

    # VERY IMPORTANT: confirm login worked
    if "You are logged in as" not in resp.text:
        raise Exception("Invalid Space-Track credentials")

    return session


@st.cache_data(ttl=600)
def get_active_leo_satellites_by_country(identity, password, limit=10):
    session = spacetrack_login(identity, password)

    url = (
        BASE_URL +
        "/basicspacedata/query/class/satcat/"
        "DECAY/null/"
        "PERIOD/<225/"
        "format/json"
    )

    resp = session.get(url, timeout=20)

    if resp.status_code != 200:
        raise Exception(f"Fetch failed: {resp.status_code}")

    # 🚨 CRITICAL FIX: HANDLE NON-JSON RESPONSE
    try:
        data = resp.json()
    except Exception:
        raise Exception("Space-Track returned non-JSON (likely blocked or session expired)")

    if not isinstance(data, list):
        raise Exception("Unexpected Space-Track response format")

    if len(data) == 0:
        raise Exception("No satellite data returned")

    countries = [
        obj.get("COUNTRY") or "UNK"
        for obj in data
    ]

    counter = Counter(countries)
    top = counter.most_common(limit)

    labels = [c[0] for c in top]
    values = [c[1] for c in top]

    return labels, values