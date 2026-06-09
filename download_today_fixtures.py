import requests
import pandas as pd
import time
from datetime import datetime
from pathlib import Path

# Use same API-Football configuration used elsewhere
API_KEY = "b503df519c6dec53422dab24653a1164"
HEADERS = {"x-apisports-key": API_KEY}

# Leagues list (same as download_league.py / other scripts)
leagues_to_download = [
    71,72,75,76,73,74,      # Brazil
    128,129,131,132,134,130,# Argentina
    239,240,241,            # Colombia
    265,266,267,            # Chile
    253,255,256,489,        # USA
    88,94,144               # Europe / others
]

# Target output path (project root as requested)
out_path = Path(r"C:\Users\PC\football_predictor\clean_project\fixtures_today.csv")
out_path.parent.mkdir(parents=True, exist_ok=True)

today = datetime.utcnow().date().isoformat()  # use UTC date to match API 'date' format YYYY-MM-DD

all_fixtures = []

for league_id in leagues_to_download:
    url = f"https://v3.football.api-sports.io/fixtures?league={league_id}&date={today}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        data = resp.json()
    except Exception as e:
        print(f"Request failed for league {league_id}: {e}")
        continue

    if not isinstance(data, dict) or "response" not in data:
        print(f"No response data for league {league_id} on {today}")
        continue

    for match in data["response"]:
        fixture = match.get("fixture", {})
        league = match.get("league", {})
        teams = match.get("teams", {})

        all_fixtures.append({
            "fixture_id": fixture.get("id"),
            "date": fixture.get("date"),
            "league": league.get("name"),
            "home_team": teams.get("home", {}).get("name"),
            "away_team": teams.get("away", {}).get("name")
        })

    # be polite with the API
    time.sleep(1)

# Save to CSV
df = pd.DataFrame(all_fixtures)
# Ensure consistent column order
cols = ["fixture_id", "date", "league", "home_team", "away_team"]
if not df.empty:
    df = df[cols]
else:
    # create empty DataFrame with columns
    df = pd.DataFrame(columns=cols)

df.to_csv(out_path, index=False)

# Print results
print(f"Downloaded {len(df)} fixtures for {today}")
print(f"Saved to: {out_path}")

# Verify file exists before exiting
if out_path.exists():
    print("Verified: file exists.")
else:
    raise SystemExit("Error: file was not saved as expected.")
