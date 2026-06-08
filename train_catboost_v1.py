import pandas as pd
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load data
df = pd.read_csv("data/processed/features_prematch_clean.csv")

# Target encoding
df["target"] = df["result"].map({
    "H": 0,
    "D": 1,
    "A": 2
})

# Reliable features only
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
    "defense_away"
]

X = df[features]
y = df["target"]

# Train/validation split
X_train, X_valid, y_train, y_valid = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training rows:", len(X_train))
print("Validation rows:", len(X_valid))

# Train CatBoost
model = CatBoostClassifier(
    iterations=1000,
    depth=6,
    learning_rate=0.03,
    loss_function="MultiClass",
    eval_metric="MultiClass",
    verbose=100
)

model.fit(
    X_train,
    y_train,
    eval_set=(X_valid, y_valid),
    use_best_model=True
)

# Predictions
preds = model.predict(X_valid)

acc = accuracy_score(y_valid, preds)

print("\nAccuracy:", acc)

print("\nClassification Report:")
print(classification_report(y_valid, preds))

# Save model
model.save_model("catboost_v1.cbm")

print("\nModel saved:")
print("catboost_v1.cbm")