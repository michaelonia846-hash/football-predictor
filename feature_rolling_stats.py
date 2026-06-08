import pandas as pd

# -----------------------------
# LOAD DATA
# -----------------------------

df = pd.read_csv(
    "data/processed/master_matches.csv",
    low_memory=False
)

# -----------------------------
# FIX TEAM NAMES
# -----------------------------

if "HomeTeam" in df.columns and "Home" in df.columns:
    df["HomeTeam"] = df["HomeTeam"].fillna(df["Home"])

if "AwayTeam" in df.columns and "Away" in df.columns:
    df["AwayTeam"] = df["AwayTeam"].fillna(df["Away"])

# -----------------------------
# FIX DATES
# -----------------------------

df["Date"] = df["Date"].astype(str).str.strip()

parsed = pd.to_datetime(
    df["Date"],
    dayfirst=True,
    errors="coerce"
)

mask = parsed.isna()

parsed.loc[mask] = pd.to_datetime(
    df.loc[mask, "Date"],
    format="%d/%m/%y",
    errors="coerce"
)

df["Date"] = parsed

print("Valid dates:", df["Date"].notna().sum())
print("Bad dates:", df["Date"].isna().sum())

# -----------------------------
# CLEAN DATA
# -----------------------------

df = df.dropna(subset=["Date"])
df = df.dropna(subset=["HomeTeam", "AwayTeam"])

df = df.sort_values("Date")

print("Rows after cleaning:", len(df))

# -----------------------------
# TEAM LIST
# -----------------------------

teams = pd.concat(
    [df["HomeTeam"], df["AwayTeam"]]
).dropna().unique()

# -----------------------------
# TEAM HISTORY
# -----------------------------

history = {}

for team in teams:
    history[team] = {
        "shots": [],
        "sot": [],
        "corners": [],
        "yellow": [],
        "red": []
    }

# -----------------------------
# COLUMN MAP
# -----------------------------

pairs = {
    "shots": ("HS", "AS"),
    "sot": ("HST", "AST"),
    "corners": ("HC", "AC"),
    "yellow": ("HY", "AY"),
    "red": ("HR", "AR")
}

# -----------------------------
# BUILD ROLLING FEATURES
# -----------------------------

rows = []

for _, row in df.iterrows():

    home = row["HomeTeam"]
    away = row["AwayTeam"]

    record = {
        "match_date": row["Date"],
        "home_team": home,
        "away_team": away
    }

    for metric in pairs.keys():

        home_hist = history[home][metric][-5:]
        away_hist = history[away][metric][-5:]

        record[f"avg_{metric}_home_5"] = (
            sum(home_hist) / len(home_hist)
            if len(home_hist) > 0 else 0
        )

        record[f"avg_{metric}_away_5"] = (
            sum(away_hist) / len(away_hist)
            if len(away_hist) > 0 else 0
        )

    rows.append(record)

    for metric, (hcol, acol) in pairs.items():

        if hcol in row.index and pd.notna(row[hcol]):
            history[home][metric].append(float(row[hcol]))

        if acol in row.index and pd.notna(row[acol]):
            history[away][metric].append(float(row[acol]))

# -----------------------------
# SAVE
# -----------------------------

rolling = pd.DataFrame(rows)

rolling.to_csv(
    "data/processed/rolling_stats_keyed.csv",
    index=False
)

print("")
print("ROLLING FILE CREATED")
print("Shape:", rolling.shape)
print("First date:", rolling["match_date"].min())
print("Last date:", rolling["match_date"].max())