import pandas as pd

matches = pd.read_csv("data/processed/matches_big.csv")

teams = pd.concat([
    matches["HomeTeam"],
    matches["AwayTeam"]
]).dropna().unique()

stats = []

for team in teams:
    stats.append({
        "Team": team,
        "Elo": 1500,
        "FormPoints": 0,
        "GF5": 0,
        "GA5": 0,
        "AvgGF": 0,
        "AvgGA": 0,
        "ScoredRate": 0,
        "CleanSheetRate": 0,
        "Over15Rate": 0,
        "BTTSRate": 0
    })

pd.DataFrame(stats).to_csv("team_stats.csv", index=False)

print("Created team_stats.csv")
print("Teams:", len(stats))