import pandas as pd

# Load historical matches
matches = pd.read_csv("data/processed/matches_big.csv")

# Get unique teams
teams = pd.unique(matches[["HomeTeam", "AwayTeam"]].values.ravel())

team_stats = []

for team in teams:
    # Filter matches where this team played
    home = matches[matches["HomeTeam"] == team]
    away = matches[matches["AwayTeam"] == team]

    # Last 5 matches for form
    last5 = pd.concat([home.tail(5), away.tail(5)], ignore_index=True)
    
    # Form points: Win=3, Draw=1, Loss=0
    points = 0
    for _, row in last5.iterrows():
        if row["HomeTeam"] == team:
            if row["HomeGoals"] > row["AwayGoals"]:
                points += 3
            elif row["HomeGoals"] == row["AwayGoals"]:
                points += 1
        else:
            if row["AwayGoals"] > row["HomeGoals"]:
                points += 3
            elif row["AwayGoals"] == row["HomeGoals"]:
                points += 1

    GF5 = last5.apply(lambda x: x["HomeGoals"] if x["HomeTeam"] == team else x["AwayGoals"], axis=1).sum()
    GA5 = last5.apply(lambda x: x["AwayGoals"] if x["HomeTeam"] == team else x["HomeGoals"], axis=1).sum()
    AvgGF = GF5 / len(last5) if len(last5) > 0 else 0
    AvgGA = GA5 / len(last5) if len(last5) > 0 else 0
    ScoredRate = sum((last5.apply(lambda x: x["HomeGoals"] if x["HomeTeam"] == team else x["AwayGoals"], axis=1) > 0)) / len(last5) if len(last5) > 0 else 0
    CleanSheetRate = sum((last5.apply(lambda x: x["AwayGoals"] if x["HomeTeam"] == team else x["HomeGoals"], axis=1) == 0)) / len(last5) if len(last5) > 0 else 0
    Over15Rate = sum((last5.apply(lambda x: (x["HomeGoals"] + x["AwayGoals"]), axis=1) > 1.5)) / len(last5) if len(last5) > 0 else 0
    BTTSRate = sum((last5.apply(lambda x: (x["HomeGoals"] > 0 and x["AwayGoals"] > 0) if x["HomeTeam"] == team else (x["HomeGoals"] > 0 and x["AwayGoals"] > 0), axis=1))) / len(last5) if len(last5) > 0 else 0

    # Elo placeholder (optional, or use previous Elo if you have)
    Elo = 1500 + (points - 7.5) * 5  # Simple adjustment

    team_stats.append({
        "Team": team,
        "Elo": round(Elo, 2),
        "FormPoints": points,
        "GF5": GF5,
        "GA5": GA5,
        "AvgGF": round(AvgGF,2),
        "AvgGA": round(AvgGA,2),
        "ScoredRate": round(ScoredRate,2),
        "CleanSheetRate": round(CleanSheetRate,2),
        "Over15Rate": round(Over15Rate,2),
        "BTTSRate": round(BTTSRate,2)
    })

# Save proper team stats
pd.DataFrame(team_stats).to_csv("team_stats.csv", index=False)
print("✅ Rebuilt team_stats.csv with real stats for", len(team_stats), "teams")