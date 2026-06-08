import pandas as pd

df = pd.read_csv(
    "data/processed/master_matches.csv",
    low_memory=False
)

print("Rows loaded:", len(df))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 20 raw dates:")
print(df["Date"].head(20))

df["Date_parsed"] = pd.to_datetime(
    df["Date"],
    dayfirst=True,
    errors="coerce"
)

print("\nRows with valid dates:", df["Date_parsed"].notna().sum())
print("Rows with bad dates:", df["Date_parsed"].isna().sum())

print("\nEarliest parsed date:")
print(df["Date_parsed"].min())

print("\nLatest parsed date:")
print(df["Date_parsed"].max())

bad = df[df["Date_parsed"].isna()]

if len(bad) > 0:
    print("\nExamples of bad dates:")
    print(bad["Date"].head(20))