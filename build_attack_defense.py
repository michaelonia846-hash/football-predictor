import pandas as pd
from collections import defaultdict

df = pd.read_csv(
    "data/processed/features_elo.csv"
)

df["match_date"] = pd.to_datetime(
    df["match_date"]
)

df = df.sort_values("match_date")

gf_history = defaultdict(list)
ga_history = defaultdict(list)

rows = []

for _, row in df.iterrows():

    home = row["home_team"]
    away = row["away_team"]

    hg = row["home_goals"]
    ag = row["away_goals"]

    home_gf5 = (
        sum(gf_history[home][-5:])
        / max(1, len(gf_history[home][-5:]))
    )

    home_ga5 = (
        sum(ga_history[home][-5:])
        / max(1, len(ga_history[home][-5:]))
    )

    away_gf5 = (
        sum(gf_history[away][-5:])
        / max(1, len(gf_history[away][-5:]))
    )

    away_ga5 = (
        sum(ga_history[away][-5:])
        / max(1, len(ga_history[away][-5:]))
    )

    attack_home = home_gf5
    defense_home = home_ga5

    attack_away = away_gf5
    defense_away = away_ga5

    rows.append({

        **row.to_dict(),

        "gf_home_5": home_gf5,
        "ga_home_5": home_ga5,

        "gf_away_5": away_gf5,
        "ga_away_5": away_ga5,

        "attack_home": attack_home,
        "defense_home": defense_home,

        "attack_away": attack_away,
        "defense_away": defense_away

    })

    gf_history[home].append(hg)
    ga_history[home].append(ag)

    gf_history[away].append(ag)
    ga_history[away].append(hg)

features = pd.DataFrame(rows)

features.to_csv(
    "data/processed/features_final.csv",
    index=False
)

print(features.shape)

print(features.head())