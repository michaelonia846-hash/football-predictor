import pandas as pd

matches = pd.read_csv(
    r"C:\Users\PC\football_predictor\data\processed\matches_big.csv"
)

print(matches["League"].value_counts().head(100))