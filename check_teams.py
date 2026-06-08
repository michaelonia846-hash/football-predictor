import pandas as pd

# Load your historical matches file
matches = pd.read_csv(r"C:\Users\PC\football_predictor\data\processed\matches_big.csv")

# List of teams to check
teams = [
    "Haiti",
    "New Zealand",
    "Fortaleza EC",
    "Vitoria",
    "Atletico Nacional",
    "Portugal U19"
]

# Check how many times each team appears in matches
for team in teams:
    found = ((matches["HomeTeam"] == team) | (matches["AwayTeam"] == team)).sum()
    print(f"{team}: {found}")