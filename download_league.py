import pandas as pd
from api_football import APIClient  # or your existing client

API_KEY = "b503df519c6dec53422dab24653a1164"
client = APIClient(API_KEY)

# List of leagues to download
leagues_to_download = [
    71,72,75,76,73,74,      # Brazil
    128,129,131,132,134,130,# Argentina
    239,240,241,             # Colombia
    265,266,267,             # Chile
    253,255,256,489,         # USA
    88,94,144                # Europe
]

all_matches = []

for league_id in leagues_to_download:
    print(f"Downloading league {league_id}...")
    matches = client.get_matches(league=league_id, season="2021")  # loop seasons later
    all_matches.extend(matches)

df = pd.DataFrame(all_matches)
df.to_csv("data/processed/matches_big.csv", index=False)
print("All important leagues downloaded and saved to matches_big.csv")