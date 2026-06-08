import pandas as pd
import requests

url = "https://v3.football.api-sports.io/leagues"
headers = {"x-apisports-key": "b503df519c6dec53422dab24653a1164"}  # replace with your API key

res = requests.get(url, headers=headers).json()

data = []

for league in res["response"]:
    league_info = league["league"]
    country = league["country"]["name"]
    data.append({
        "id": league_info["id"],
        "name": league_info["name"],
        "country": country
    })

df = pd.DataFrame(data)
df.to_csv("leagues.csv", index=False)
print("Saved leagues.csv with", len(df), "leagues")