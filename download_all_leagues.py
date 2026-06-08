import pandas as pd
import requests
import time
import os

# Make sure the folder exists
os.makedirs("data/processed", exist_ok=True)

API_KEY = "b503df519c6dec53422dab24653a1164"
headers = {"x-apisports-key": API_KEY}

# Define leagues for each country (excluding Brazil)
countries_leagues = {
    "Argentina": [128,129,131,132,134,130],
    "Colombia": [239,240,241],
    "Chile": [265,266,267],
    "USA": [253,255,256,489],
    "Netherlands": [88],
    "Portugal": [94],
    "Belgium": [144]
}

# Seasons to download
seasons = [2021, 2022, 2023, 2024, 2025]

for country, leagues in countries_leagues.items():
    all_matches = []
    
    for league_id in leagues:
        for season in seasons:
            print(f"Downloading {country} league {league_id}, season {season}...")
            
            url = f"https://v3.football.api-sports.io/fixtures?league={league_id}&season={season}"
            try:
                res = requests.get(url, headers=headers, timeout=30)
                data = res.json()
            except Exception as e:
                print("Request failed:", e)
                continue

            if "response" not in data:
                print(f"No data for league {league_id}, season {season}")
                continue

            for match in data["response"]:
                all_matches.append({
                    "Date": match["fixture"]["date"],
                    "HomeTeam": match["teams"]["home"]["name"],
                    "AwayTeam": match["teams"]["away"]["name"],
                    "HomeGoals": match["goals"]["home"],
                    "AwayGoals": match["goals"]["away"],
                    "League": match["league"]["name"]
                })
            
            time.sleep(1)  # be polite to the API

    # Save each country to its own CSV
    filename = f"data/processed/{country.lower()}_history.csv"
    df = pd.DataFrame(all_matches)
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} {country} matches to {filename}\n")