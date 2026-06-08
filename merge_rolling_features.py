import pandas as pd

# -----------------------------
# LOAD FILES
# -----------------------------

features = pd.read_csv(
    "data/processed/features_full.csv",
    low_memory=False
)

rolling = pd.read_csv(
    "data/processed/rolling_stats_keyed.csv",
    low_memory=False
)

# -----------------------------
# DATE FORMAT
# -----------------------------

features["match_date"] = pd.to_datetime(
    features["match_date"],
    errors="coerce"
)

rolling["match_date"] = pd.to_datetime(
    rolling["match_date"],
    errors="coerce"
)

# -----------------------------
# MERGE
# -----------------------------

merged = features.merge(
    rolling,
    on=[
        "match_date",
        "home_team",
        "away_team"
    ],
    how="left"
)

# -----------------------------
# REMOVE LEAKAGE COLUMNS
# -----------------------------

leakage_cols = [
    "HS", "AS",
    "HST", "AST",
    "HC", "AC",
    "HY", "AY",
    "HR", "AR"
]

merged = merged.drop(
    columns=leakage_cols,
    errors="ignore"
)

# -----------------------------
# SAVE
# -----------------------------

merged.to_csv(
    "data/processed/features_full_clean.csv",
    index=False
)

print("MERGE COMPLETE")
print("Shape:", merged.shape)

print("\nColumns:")
for c in merged.columns:
    print(c)

print("\nMissing rolling values:")
print(
    merged[
        [
            "avg_shots_home_5",
            "avg_shots_away_5"
        ]
    ].isna().sum()
)