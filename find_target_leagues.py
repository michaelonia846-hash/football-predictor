import pandas as pd

df = pd.read_csv("leagues.csv")

targets = [
    "Brazil",
    "Argentina",
    "Colombia",
    "Chile",
    "Major League Soccer",
    "USL",
    "Eredivisie",
    "Portugal",
    "Belgium"
]

for target in targets:
    print("\n" + "=" * 60)
    print(target)
    print("=" * 60)

    result = df[
        df["name"].astype(str).str.contains(target, case=False, na=False)
        | df["country"].astype(str).str.contains(target, case=False, na=False)
    ]

    if len(result):
        cols = [c for c in ["id", "name", "country"] if c in result.columns]
        print(result[cols].head(20).to_string(index=False))
    else:
        print("No matches found")