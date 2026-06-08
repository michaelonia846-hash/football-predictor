import pandas as pd

# Load ALL historical matches
matches = pd.read_csv("data/processed/matches_big.csv")

team_stats = []

teams = sorted(
    set(matches["HomeTeam"].dropna())
    | set(matches["AwayTeam"].dropna())
)

for team in teams:

    home = matches[matches["HomeTeam"] == team]
    away = matches[matches["AwayTeam"] == team]

    played = len(home) + len(away)

    if played == 0:
        continue

    recent_home = home.tail(5)
    recent_away = away.tail(5)

    GF5 = (
        recent_home["HomeGoals"].sum()
        + recent_away["AwayGoals"].sum()
    )

    GA5 = (
        recent_home["AwayGoals"].sum()
        + recent_away["HomeGoals"].sum()
    )

    AvgGF = GF5 / 10
    AvgGA = GA5 / 10

    # Form points
    form_points = 0

    for _, row in recent_home.iterrows():
        if row["HomeGoals"] > row["AwayGoals"]:
            form_points += 3
        elif row["HomeGoals"] == row["AwayGoals"]:
            form_points += 1

    for _, row in recent_away.iterrows():
        if row["AwayGoals"] > row["HomeGoals"]:
            form_points += 3
        elif row["AwayGoals"] == row["HomeGoals"]:
            form_points += 1

    # Goals scored rate
    scored_matches = 0

    for _, row in recent_home.iterrows():
        if row["HomeGoals"] > 0:
            scored_matches += 1

    for _, row in recent_away.iterrows():
        if row["AwayGoals"] > 0:
            scored_matches += 1

    ScoredRate = scored_matches / 10

    # Clean sheet rate
    clean_sheets = 0

    for _, row in recent_home.iterrows():
        if row["AwayGoals"] == 0:
            clean_sheets += 1

    for _, row in recent_away.iterrows():
        if row["HomeGoals"] == 0:
            clean_sheets += 1

    CleanSheetRate = clean_sheets / 10

    # Over 1.5 rate
    over15 = 0

    for _, row in recent_home.iterrows():
        if row["HomeGoals"] + row["AwayGoals"] > 1:
            over15 += 1

    for _, row in recent_away.iterrows():
        if row["HomeGoals"] + row["AwayGoals"] > 1:
            over15 += 1

    Over15Rate = over15 / 10

    # BTTS rate
    btts = 0

    for _, row in recent_home.iterrows():
        if row["HomeGoals"] > 0 and row["AwayGoals"] > 0:
            btts += 1

    for _, row in recent_away.iterrows():
        if row["HomeGoals"] > 0 and row["AwayGoals"] > 0:
            btts += 1

    BTTSRate = btts / 10

    # Elo based on form
    Elo = 1500 + (form_points * 2.5)

    team_stats.append({
        "Team": team,
        "Elo": round(Elo, 2),
        "FormPoints": form_points,
        "GF5": GF5,
        "GA5": GA5,
        "AvgGF": round(AvgGF, 2),
        "AvgGA": round(AvgGA, 2),
        "ScoredRate": round(ScoredRate, 2),
        "CleanSheetRate": round(CleanSheetRate, 2),
        "Over15Rate": round(Over15Rate, 2),
        "BTTSRate": round(BTTSRate, 2)
    })

team_stats_df = pd.DataFrame(team_stats)

team_stats_df.to_csv("team_stats.csv", index=False)

print("Created team_stats.csv")
print("Teams:", len(team_stats_df))