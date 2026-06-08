import pandas as pd

features = pd.read_csv(
    "data/processed/features_full.csv"
)

rolling = pd.read_csv(
    "data/processed/rolling_stats_keyed.csv"
)

print("\nFEATURES")
print(features[[
    "match_date",
    "home_team",
    "away_team"
]].head(10))

print("\nROLLING")
print(rolling[[
    "match_date",
    "home_team",
    "away_team"
]].head(10))