import pandas as pd

df = pd.read_csv("leagues.csv")

wanted = [
    "Brazil",
    "Argentina",
    "Colombia",
    "Chile",
    "MLS",
    "USL",
    "Netherlands",
    "Portugal",
    "Belgium"
]

for word in wanted:
    print("\n" + "="*50)
    print(word)
    print("="*50)

    matches = df[
        df["name"].astype(str).str.contains(word, case=False, na=False)
    ]

    if len(matches):
        print(matches[["id", "name", "country"]].head(20))