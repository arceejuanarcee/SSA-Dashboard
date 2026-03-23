import requests
from bs4 import BeautifulSoup

URL = "https://www.spacelaunchschedule.com/category/china-aerospace-science-and-technology-corporation/"

VALID_SITES = [
    "Xichang Satellite Launch Center",
    "Naro Space Center",
    "Wenchang Space Launch Site",
    "Hainan Commercial Space Launch Site",
    "Hainan International Commercial Launch Center",
    "Jiuquan Satellite Launch Center",
]

def fetch_china_launches():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        res = requests.get(URL, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")

        launches = []

        cards = soup.find_all("div", class_="launch-list-thumbnail")

        if not cards:
            return [], "Parser failed: no launch cards found"

        for c in cards:
            try:
                title_block = c.find("h2", class_="entry-title")
                if not title_block:
                    continue

                payload = title_block.contents[0].strip()

                rocket_tag = title_block.find("span")
                rocket = rocket_tag.get_text(strip=True) if rocket_tag else payload

                time_tag = c.find("time", class_="launchDateTime")
                date = time_tag.get_text(strip=True) if time_tag else "TBD"

                location_divs = c.find_all("div", class_="col")
                location = ""
                for div in location_divs:
                    text = div.get_text(strip=True)
                    if "Launch Center" in text:
                        location = text
                        break

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