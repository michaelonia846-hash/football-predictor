import pandas as pd
from pathlib import Path

csv_path = Path("data/processed/features_full_clean.csv")
if not csv_path.exists():
    raise SystemExit("File not found: " + str(csv_path))

# Read CSV
df = pd.read_csv(csv_path, low_memory=False)
df["match_date"] = pd.to_datetime(df["match_date"], errors="coerce")

print("rows:", len(df))
print("columns:", len(df.columns))
print("min date:", df["match_date"].min(), "max date:", df["match_date"].max())

# features to check (from training script)
features = [
    "elo_home","elo_away",
    "form_home_5","form_away_5",
    "gf_home_5","ga_home_5","gf_away_5","ga_away_5",
    "attack_home","defense_home","attack_away","defense_away",
    "HS","AS","HST","AST","HC","AC","HY","AY","HR","AR"
]

present = {f: (f in df.columns) for f in features}
print("feature presence:", present)

# compute and print missing rates only for features that are present
present_features = [f for f, p in present.items() if p]
if present_features:
    missing_rates = df[present_features].isna().mean().sort_values(ascending=False)
    print("\nMissing rates (present features), sorted desc:")
    print(missing_rates)

# check for teams playing multiple matches same day
if "home_team" in df.columns:
    grouped_home = df.groupby(["match_date", "home_team"]).size()
    same_day_home_multimatch = (grouped_home > 1).sum()
else:
    same_day_home_multimatch = 0
if "away_team" in df.columns:
    grouped_away = df.groupby(["match_date", "away_team"]).size()
    same_day_away_multimatch = (grouped_away > 1).sum()
else:
    same_day_away_multimatch = 0

print("\n(date,home_team) combos with >1 match on same date:", same_day_home_multimatch)
print("(date,away_team) combos with >1 match on same date:", same_day_away_multimatch)

# show sample rows with missing core features or high-missing features
core = ["match_date", "home_team", "away_team", "result"]
if present_features:
    sample_missing = df[df[present_features].isnull().any(axis=1)][core + present_features].head(10)
    print("\nSample rows with any missing model features (first 10):")
    # If dataframe is empty, avoid printing huge output
    if sample_missing.empty:
        print("No sample rows with missing model features found.")
    else:
        print(sample_missing.to_string(index=False))
else:
    print("No present model features to check for missingness.")
