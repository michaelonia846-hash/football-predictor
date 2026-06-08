import pandas as pd

df = pd.read_csv(
    "data/processed/master_matches.csv",
    low_memory=False
)

# Create unified columns

df["match_date"] = df["Date"]

df["home_team"] = (
    df["HomeTeam"]
    .fillna(df["Home"])
)

df["away_team"] = (
    df["AwayTeam"]
    .fillna(df["Away"])
)

df["home_goals"] = (
    df["FTHG"]
    .fillna(df["HG"])
)

df["away_goals"] = (
    df["FTAG"]
    .fillna(df["AG"])
)

df["result"] = (
    df["FTR"]
    .fillna(df["Res"])
)

# Keep only usable matches

clean = df[
    [
        "match_date",
        "home_team",
        "away_team",
        "home_goals",
        "away_goals",
        "result",
        "country"
    ]
].copy()

clean = clean.dropna()

clean["match_date"] = pd.to_datetime(
    clean["match_date"],
    dayfirst=True,
    errors="coerce"
)

clean = clean.dropna(subset=["match_date"])

clean = clean.sort_values("match_date")

clean.to_csv(
    "data/processed/matches_clean.csv",
    index=False
)

print(clean.shape)

print(clean.head())