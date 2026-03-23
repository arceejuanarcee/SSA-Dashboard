import requests
from bs4 import BeautifulSoup

URL = "https://www.spacelaunchschedule.com/category/china-aerospace-science-and-technology-corporation/"

VALID_SITES = [
    "Xichang Satellite Launch Center",
    "Naro Space Center",
    "Wenchang Space Launch Site",
    "Hainan Commercial Space Launch Site",
    "Hainan International Commercial Launch Center",
]

def fetch_china_launches():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        res = requests.get(URL, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")

        launches = []

        cards = soup.find_all("div", class_="launch")

        if not cards:
            return [], "Parser failed: no launch cards found"

        for c in cards:
            try:
                title = c.find("div", class_="mission").get_text(strip=True)
                rocket = c.find("div", class_="rocket").get_text(strip=True)

                date_tag = c.find("div", class_="date")
                date = date_tag.get_text(strip=True) if date_tag else "TBD"

                location_tag = c.find("div", class_="location")
                location = location_tag.get_text(strip=True) if location_tag else ""

                if not any(site in location for site in VALID_SITES):
                    continue

                launches.append({
                    "rocket": rocket,
                    "date": date
                })

                if len(launches) >= 5:
                    break

            except:
                continue

        return launches, None

    except Exception as e:
        return [], str(e)