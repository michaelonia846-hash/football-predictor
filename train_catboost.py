import pandas as pd

from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

df = pd.read_csv(
    "data/processed/features_full.csv"
)

features = [

    "elo_home",
    "elo_away",

    "form_home_5",
    "form_away_5",

    "gf_home_5",
    "ga_home_5",

    "gf_away_5",
    "ga_away_5",

    "attack_home",
    "defense_home",

    "attack_away",
    "defense_away",

    "HS",
    "AS",

    "HST",
    "AST",

    "HC",
    "AC",

    "HY",
    "AY",

    "HR",
    "AR"
]

target_map = {
    "H": 0,
    "D": 1,
    "A": 2
}

df = df.dropna(subset=["result"])

X = df[features]

y = df["result"].map(target_map)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

model = CatBoostClassifier(
    iterations=1000,
    depth=8,
    learning_rate=0.03,
    loss_function="MultiClass",
    eval_metric="Accuracy",
    verbose=100
)

model.fit(
    X_train,
    y_train
)

pred = model.predict(X_test)

acc = accuracy_score(
    y_test,
    pred
)

print("\nAccuracy:", acc)

model.save_model(
    "models/catboost_match_result.cbm"
)

print("Model saved.")