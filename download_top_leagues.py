import os
import requests

BASE_URL = "https://www.football-data.co.uk/mmz4281"

TOP_LEAGUES = {
    "england": ["E0"],
    "scotland": ["SC0"],
    "spain": ["SP1"],
    "germany": ["D1"],
    "italy": ["I1"],
    "france": ["F1"],
    "netherlands": ["N1"],
    "belgium": ["B1"],
    "portugal": ["P1"],
}

SEASONS = [
    "1617",
    "1718",
    "1819",
    "1920",
    "2021",
    "2122",
    "2223",
    "2324",
    "2425",
    "2526",
]

RAW_DIR = "data/raw"

os.makedirs(RAW_DIR, exist_ok=True)

for country, leagues in TOP_LEAGUES.items():

    country_dir = os.path.join(RAW_DIR, country)
    os.makedirs(country_dir, exist_ok=True)

    for league in leagues:
        for season in SEASONS:

            url = f"{BASE_URL}/{season}/{league}.csv"

            filename = f"{league}_{season}.csv"
            filepath = os.path.join(country_dir, filename)

            print(f"Downloading {url}")

            try:
                r = requests.get(url, timeout=30)

                if r.status_code == 200 and len(r.text) > 1000:
                    with open(filepath, "wb") as f:
                        f.write(r.content)

                    print(f"Saved {filepath}")

                else:
                    print(f"Missing: {url}")

            except Exception as e:
                print(f"Error: {e}")

print("Finished.")