import pandas as pd

features = pd.read_csv(
    "data/processed/features_final.csv"
)

master = pd.read_csv(
    "data/processed/master_matches.csv",
    low_memory=False
)

master["match_date"] = pd.to_datetime(
    master["Date"],
    errors="coerce"
)

master["home_team"] = (
    master["HomeTeam"]
    .fillna(master.get("Home"))
)

master["away_team"] = (
    master["AwayTeam"]
    .fillna(master.get("Away"))
)

stats = master[
    [
        "match_date",
        "home_team",
        "away_team",

        "HS","AS",
        "HST","AST",

        "HC","AC",

        "HY","AY",

        "HR","AR"
    ]
].copy()

features["match_date"] = pd.to_datetime(
    features["match_date"]
)

df = features.merge(

    stats,

    on=[
        "match_date",
        "home_team",
        "away_team"
    ],

    how="left"
)

stat_cols = [
    "HS","AS",
    "HST","AST",
    "HC","AC",
    "HY","AY",
    "HR","AR"
]

for c in stat_cols:
    df[c] = df[c].fillna(-1)

df.to_csv(
    "data/processed/features_full.csv",
    index=False
)

print(df.shape)

print(df.head())