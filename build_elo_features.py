import pandas as pd
from collections import defaultdict

# load matches (expects columns: match_date, home_team, away_team, home_goals, away_goals, result, country)
df = pd.read_csv("data/processed/matches_clean.csv", low_memory=False)
df["match_date"] = pd.to_datetime(df["match_date"], errors="coerce")
df = df.sort_values("match_date")

# Elo initial values and history storage
elo = defaultdict(lambda: 1500.0)
history = defaultdict(list)

rows = []
K = 20

# Process matches grouped by date to avoid same-day leakage:
for match_date, group in df.groupby(df["match_date"]):
    # temporary store of elo updates and history updates for this date
    elo_updates = {}
    history_updates = defaultdict(list)

    # iterate matches for this date; compute features using elo/current history BEFORE applying updates
    for _, row in group.iterrows():
        home = row["home_team"]
        away = row["away_team"]

        hg = row["home_goals"]
        ag = row["away_goals"]

        # use current elo snapshot (no updates from same date yet)
        home_elo = elo[home]
        away_elo = elo[away]

        expected_home = 1 / (1 + 10 ** ((away_elo - home_elo) / 400))
        expected_away = 1 - expected_home

        if hg > ag:
            actual_home = 1.0
            actual_away = 0.0
        elif hg < ag:
            actual_home = 0.0
            actual_away = 1.0
        else:
            actual_home = 0.5
            actual_away = 0.5

        # form (last 5 results) taken from history BEFORE today's matches
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
            "result": row.get("result", ""),
            "country": row.get("country", ""),
            "elo_home": home_elo,
            "elo_away": away_elo,
            "form_home_5": home_form_pts,
            "form_away_5": away_form_pts
        })

        # compute elo updates but don't apply until after the day's loop
        new_home_elo = home_elo + K * (actual_home - expected_home)
        new_away_elo = away_elo + K * (actual_away - expected_away)
        # keep the last update for a team on the same day
        elo_updates[home] = new_home_elo
        elo_updates[away] = new_away_elo

        # collect history updates (points) to add after the day's matches
        history_updates[home].append(actual_home * 3.0)
        history_updates[away].append(actual_away * 3.0)

    # apply updates for the entire day
    for team, new_elo in elo_updates.items():
        elo[team] = new_elo

    for team, pts_list in history_updates.items():
        history[team].extend(pts_list)

# write out features
features = pd.DataFrame(rows)
features.to_csv("data/processed/features_elo.csv", index=False)

print("features_elo.csv written:", features.shape)
print(features.head())
