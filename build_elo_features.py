import pandas as pd
from collections import defaultdict
import math
import os

# Config
INPUT = "data/processed/matches_clean.csv"
OUTPUT = "data/processed/features_elo.csv"
K = 20
HOME_ADV = 60  # Elo points advantage for the home team; tuneable

if not os.path.exists(INPUT):
    raise FileNotFoundError(f"{INPUT} not found. Run data preparation scripts first.")

pdf = pd.read_csv(INPUT)
pdf["match_date"] = pd.to_datetime(pdf["match_date"], errors="coerce")
pdf = pdf.sort_values("match_date")

elo = defaultdict(lambda: 1500.0)
history = defaultdict(list)
rows = []

for _, row in pdf.iterrows():

    home = row["home_team"]
    away = row["away_team"]

    hg = int(row.get("home_goals", 0))
    ag = int(row.get("away_goals", 0))

    home_elo = elo[home]
    away_elo = elo[away]

    # Apply home advantage to the home Elo when computing expected result
    adj_home_elo = home_elo + HOME_ADV
    adj_away_elo = away_elo

    expected_home = 1 / (1 + 10 ** ((adj_away_elo - adj_home_elo) / 400.0))
    expected_away = 1.0 - expected_home

    # Actuals (match points style)
    if hg > ag:
        actual_home = 1.0
        actual_away = 0.0
    elif hg < ag:
        actual_home = 0.0
        actual_away = 1.0
    else:
        actual_home = 0.5
        actual_away = 0.5

    # Optional goal-difference scaling: larger margin => larger update
    goal_diff = abs(hg - ag)
    if goal_diff <= 1:
        GD_SCALE = 1.0
    else:
        # small amplification per extra goal (tunable)
        GD_SCALE = 1.0 + 0.1 * (goal_diff - 1)

    # Update Elo values (apply scaling)
    elo[home] = home_elo + K * GD_SCALE * (actual_home - expected_home)
    elo[away] = away_elo + K * GD_SCALE * (actual_away - expected_away)

    # Form: keep last 5 * 3 points (like win=3, draw=1)
    history[home].append(actual_home * 3)
    history[away].append(actual_away * 3)

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
        "result": row.get("result"),
        "country": row.get("country"),
        "elo_home": home_elo,
        "elo_away": away_elo,
        "form_home_5": home_form_pts,
        "form_away_5": away_form_pts
    })

features = pd.DataFrame(rows)

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
features.to_csv(OUTPUT, index=False)
print("Saved Elo features to", OUTPUT)
