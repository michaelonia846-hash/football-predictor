import os
import requests

BASE_URL = "https://www.football-data.co.uk/new"

EXTRA_LEAGUES = {
    "brazil": ["BRA"],
    "argentina": ["ARG"],
    "finland": ["FIN"],
    "usa": ["USA"],  # MLS
}

RAW_DIR = "data/raw"

os.makedirs(RAW_DIR, exist_ok=True)

for country, leagues in EXTRA_LEAGUES.items():

    country_dir = os.path.join(RAW_DIR, country)
    os.makedirs(country_dir, exist_ok=True)

    for league in leagues:

        url = f"{BASE_URL}/{league}.csv"

        filename = f"{league}.csv"
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