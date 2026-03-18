import requests
from collections import Counter

BASE_URL = "https://www.space-track.org"


def spacetrack_login(identity, password):
    session = requests.Session()

    login_url = BASE_URL + "/ajaxauth/login"
    data = {
        "identity": identity,
        "password": password
    }

    resp = session.post(login_url, data=data)

    if resp.status_code != 200:
        raise Exception("Space-Track login failed")

    return session


def get_active_leo_satellites_by_country(identity, password, limit=10):
    session = spacetrack_login(identity, password)

    query = (
        "/basicspacedata/query/class/gp/"
        "decay_date/null-val/"
        "period/<225/"
        "orderby/CURRENT ascending/"
        "format/json"
    )

    url = BASE_URL + query

    resp = session.get(url, timeout=20)

    if resp.status_code != 200:
        raise Exception("Failed to fetch Space-Track data")

    data = resp.json()

    if not data:
        return [], []

    countries = [obj.get("COUNTRY_CODE", "UNK") for obj in data]

    counter = Counter(countries)

    top = counter.most_common(limit)

    labels = [c[0] for c in top]
    values = [c[1] for c in top]

    return labels, values