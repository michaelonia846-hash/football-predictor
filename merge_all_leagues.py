import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")

dfs = []

for csv_file in RAW_DIR.rglob("*.csv"):

    try:

        df = pd.read_csv(csv_file, low_memory=False)

        df["source_file"] = csv_file.name
        df["country"] = csv_file.parent.name

        dfs.append(df)

        print(f"Loaded {csv_file}")

    except Exception as e:

        print(f"Failed {csv_file}: {e}")

master = pd.concat(dfs, ignore_index=True)

print()
print("TOTAL ROWS:", len(master))
print("TOTAL COLS:", len(master.columns))

Path("data/processed").mkdir(parents=True, exist_ok=True)

master.to_csv(
    "data/processed/master_matches.csv",
    index=False
)

print()
print("Saved:")
print("data/processed/master_matches.csv")