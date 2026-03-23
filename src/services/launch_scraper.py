import requests
from bs4 import BeautifulSoup

URL = "https://www.spacelaunchschedule.com/category/china-aerospace-science-and-technology-corporation/"

VALID_SITES = [
    "Xichang Satellite Launch Center",
    "Naro Space Center",
    "Wenchang Space Launch Site",
    "Hainan Commercial Space Launch Site",
    "Hainan International Commercial Launch Center"
]


def fetch_china_launches():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(URL, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        launches = []

        items = soup.select("div.mission")

        for item in items:
            try:
                title = item.select_one("span.mission_name").get_text(strip=True)

                date_el = item.select_one("span.launchdate")
                date = date_el.get_text(strip=True) if date_el else "TBD"

                location_el = item.select_one("span.launchsite")
                location = location_el.get_text(strip=True) if location_el else ""

                if any(site in location for site in VALID_SITES):
                    launches.append({
                        "rocket": title,
                        "date": date
                    })

            except:
                continue

        return launches[:5], None

    except Exception as e:
        return [], str(e)