import pandas as pd
import requests
import time

API_KEY = "b503df519c6dec53422dab24653a1164"  # your API key here

headers = {"x-apisports-key": API_KEY}

# Brazil leagues
leagues = [71, 72, 75, 76, 73, 74]

# Seasons you want
seasons = [2026]

all_matches = []

for league_id in leagues:
    for season in seasons:
        print(f"Downloading league {league_id}, season {season}...")
        url = f"https://v3.football.api-sports.io/fixtures?league={league_id}&season={season}"
        res = requests.get(url, headers=headers)
        data = res.json()
        
        if "response" not in data:
            print("No data found for league", league_id, "season", season)
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

df = pd.DataFrame(all_matches)
df.to_csv("brazil_history.csv", index=False)
print("Saved", len(df), "Brazil matches to brazil_history.csv")