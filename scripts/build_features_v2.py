import pandas as pd

print("Loading files...")

features = pd.read_csv(
    "data/processed/features_prematch_clean.csv",
    low_memory=False
)

rolling = pd.read_csv(
    "data/processed/team_rolling_stats.csv",
    low_memory=False
)

features["match_date"] = pd.to_datetime(features["match_date"])
rolling["Date"] = pd.to_datetime(rolling["Date"])

rolling_home = rolling.rename(
    columns={
        "Team": "home_team",
        "Shots_last5": "avg_shots_home_5",
        "SOT_last5": "avg_sot_home_5",
        "Corners_last5": "avg_corners_home_5",
        "Yellow_last5": "avg_yellow_home_5",
        "Red_last5": "avg_red_home_5"
    }
)

rolling_away = rolling.rename(
    columns={
        "Team": "away_team",
        "Shots_last5": "avg_shots_away_5",
        "SOT_last5": "avg_sot_away_5",
        "Corners_last5": "avg_corners_away_5",
        "Yellow_last5": "avg_yellow_away_5",
        "Red_last5": "avg_red_away_5"
    }
)

features = features.merge(
    rolling_home[
        [
            "Date",
            "home_team",
            "avg_shots_home_5",
            "avg_sot_home_5",
            "avg_corners_home_5",
            "avg_yellow_home_5",
            "avg_red_home_5"
        ]
    ],
    left_on=["match_date", "home_team"],
    right_on=["Date", "home_team"],
    how="left"
)

features = features.merge(
    rolling_away[
        [
            "Date",
            "away_team",
            "avg_shots_away_5",
            "avg_sot_away_5",
            "avg_corners_away_5",
            "avg_yellow_away_5",
            "avg_red_away_5"
        ]
    ],
    left_on=["match_date", "away_team"],
    right_on=["Date", "away_team"],
    how="left"
)

features.drop(
    columns=["Date_x", "Date_y"],
    errors="ignore",
    inplace=True
)

print(features.shape)

features.to_csv(
    "data/processed/features_v2.csv",
    index=False
)

print("Saved:")
print("data/processed/features_v2.csv")