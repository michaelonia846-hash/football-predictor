import pandas as pd

print("Loading master_matches...")

df = pd.read_csv(
    "data/processed/master_matches.csv",
    low_memory=False
)

df["Date"] = pd.to_datetime(
    df["Date"],
    dayfirst=True,
    errors="coerce"
)

df = df.sort_values("Date")

stats = []

for _, row in df.iterrows():

    stats.append({
        "Date": row["Date"],
        "Team": row["HomeTeam"],
        "Shots": row["HS"],
        "SOT": row["HST"],
        "Corners": row["HC"],
        "Yellow": row["HY"],
        "Red": row["HR"]
    })

    stats.append({
        "Date": row["Date"],
        "Team": row["AwayTeam"],
        "Shots": row["AS"],
        "SOT": row["AST"],
        "Corners": row["AC"],
        "Yellow": row["AY"],
        "Red": row["AR"]
    })

team_stats = pd.DataFrame(stats)

team_stats = team_stats.sort_values(["Team", "Date"])

for col in [
    "Shots",
    "SOT",
    "Corners",
    "Yellow",
    "Red"
]:
    team_stats[f"{col}_last5"] = (
        team_stats
        .groupby("Team")[col]
        .transform(
            lambda x:
            x.shift(1)
             .rolling(5, min_periods=1)
             .mean()
        )
    )

print(team_stats.head())

team_stats.to_csv(
    "data/processed/team_rolling_stats.csv",
    index=False
)

print("Saved:")
print("data/processed/team_rolling_stats.csv")