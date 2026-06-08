import pandas as pd

features = pd.read_csv(
    "data/processed/features_full.csv"
)

rolling = pd.read_csv(
    "data/processed/rolling_stats_keyed.csv"
)

print("Features rows:", len(features))
print("Rolling rows :", len(rolling))

f_teams = set(features["home_team"].unique())
r_teams = set(rolling["home_team"].unique())

missing = sorted(f_teams - r_teams)

print("\nTeams in features but not rolling:")
print("Count:", len(missing))

for t in missing[:100]:
    print(t)