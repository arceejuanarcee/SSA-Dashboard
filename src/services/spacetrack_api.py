import requests
from collections import Counter
import streamlit as st

BASE_URL = "https://www.space-track.org"


def get_active_leo_satellites_by_country(identity, password, limit=10):
    try:
        session = requests.Session()

        # STEP 1: LOGIN
        login_url = BASE_URL + "/ajaxauth/login"

        login_payload = {
            "identity": identity,
            "password": password
        }

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.space-track.org/auth/login"
        }

        login_resp = session.post(
            login_url,
            data=login_payload,
            headers=headers,
            timeout=30
        )

        if login_resp.status_code != 200:
            return [], [], f"Login failed: {login_resp.status_code}"

        # 🚨 CRITICAL CHECK
        if "failed" in login_resp.text.lower():
            return [], [], "Invalid credentials"

        # STEP 2: QUERY (YOUR EXACT FILTER)
        query_url = (
            BASE_URL +
            "/basicspacedata/query/class/satcat/"
            "DECAY/null/"
            "PERIOD/<225/"
            "orderby/COUNTRY%20asc/"
            "format/json"
        )

        resp = session.get(query_url, headers=headers, timeout=30)

        if resp.status_code != 200:
            return [], [], f"Query failed: {resp.status_code}"

        # 🚨 SPACE-TRACK BLOCK DETECTION
        if "<html" in resp.text.lower():
            return [], [], "Blocked by Space-Track (HTML returned)"

        data = resp.json()

        if not isinstance(data, list) or len(data) == 0:
            return [], [], "Empty dataset"

        # STEP 3: PROCESS
        countries = [
            obj.get("COUNTRY") or "UNK"
            for obj in data
        ]

        counter = Counter(countries)
        top = counter.most_common(limit)

        labels = [c[0] for c in top]
        values = [c[1] for c in top]

        return labels, values, None

    except Exception as e:
        return [], [], str(e)