import pandas as pd
from collections import defaultdict

df = pd.read_csv(
    "data/processed/matches_clean.csv"
)

df["match_date"] = pd.to_datetime(df["match_date"])

df = df.sort_values("match_date")

elo = defaultdict(lambda: 1500)

history = defaultdict(list)

rows = []

K = 20

for _, row in df.iterrows():

    home = row["home_team"]
    away = row["away_team"]

    hg = row["home_goals"]
    ag = row["away_goals"]

    home_elo = elo[home]
    away_elo = elo[away]

    expected_home = (
        1 / (1 + 10 ** ((away_elo - home_elo) / 400))
    )

    expected_away = 1 - expected_home

    if hg > ag:
        actual_home = 1
        actual_away = 0

    elif hg < ag:
        actual_home = 0
        actual_away = 1

    else:
        actual_home = 0.5
        actual_away = 0.5

    home_form = history[home][-5:]
    away_form = history[away][-5:]

    home_form_pts = sum(home_form)
    away_form_pts = sum(away_form)

    rows.append({

        "match_date": row["match_date"],

        "home_team": home,
        "away_team": away,

        "home_goals": hg,
        "away_goals": ag,

        "result": row["result"],

        "country": row["country"],

        "elo_home": home_elo,
        "elo_away": away_elo,

        "form_home_5": home_form_pts,
        "form_away_5": away_form_pts

    })

    elo[home] = (
        home_elo +
        K * (actual_home - expected_home)
    )

    elo[away] = (
        away_elo +
        K * (actual_away - expected_away)
    )

    history[home].append(actual_home * 3)
    history[away].append(actual_away * 3)

features = pd.DataFrame(rows)

features.to_csv(
    "data/processed/features_elo.csv",
    index=False
)

print(features.shape)

print(features.head())