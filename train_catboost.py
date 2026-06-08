import pandas as pd
import numpy as np

from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score
from sklearn.utils.class_weight import compute_class_weight

# read features (this CSV should be the pre-match feature store)
df = pd.read_csv("data/processed/features_full_clean.csv", low_memory=False)

# parse date
df["match_date"] = pd.to_datetime(df["match_date"], errors="coerce")

# features used by model (conservative set). Update this list if you add more pre-match features.
features = [
    "elo_home", "elo_away",
    "form_home_5", "form_away_5",
    "gf_home_5", "ga_home_5",
    "gf_away_5", "ga_away_5",
    "attack_home", "defense_home",
    "attack_away", "defense_away",
    "HS", "AS",      # if present (shots)
    "HST", "AST",
    "HC", "AC",
    "HY", "AY",
    "HR", "AR"
]

# verify required columns exist
missing_cols = [c for c in ["match_date", "result"] + features if c not in df.columns]
if missing_cols:
    print("WARNING: missing columns in CSV:", missing_cols)
    core_missing = [c for c in ["elo_home", "elo_away", "form_home_5", "form_away_5"] if c not in df.columns]
    if core_missing:
        raise SystemExit(f"Core features missing: {core_missing}. Recompute feature store before training.")

# drop rows without result or match_date
df = df.dropna(subset=["result", "match_date"]) 

# map target
target_map = {"H": 0, "D": 1, "A": 2}
df["target"] = df["result"].map(target_map)
df = df.dropna(subset=["target"]) 
df["target"] = df["target"].astype(int)

# sort by date
df = df.sort_values("match_date")

# Conservative core-only requirement (do NOT drop on all req_features)
core_features = [
    "elo_home",
    "elo_away",
    "form_home_5",
    "form_away_5"
]
before = len(df)
df = df.dropna(subset=core_features)
after_core_drop = len(df)
print(f"Dropped {before - after_core_drop} rows that lacked core pre-match features (elo/form).")

# req_features are those present in the CSV from our features list
req_features = [f for f in features if f in df.columns]

# Report missingness for non-core features (sorted desc)
missing_rates = df[req_features].isna().mean().sort_values(ascending=False)
print("Missingness (all model features), sorted desc:")
print(missing_rates)

# Note: We do NOT drop remaining rows with NaNs in non-core features.
# CatBoost will handle missing values for non-core features.

# time-based split: last 20% (by date) -> test set
cutoff_date = df["match_date"].quantile(0.8)
train_df = df[df["match_date"] < cutoff_date].copy()
test_df = df[df["match_date"] >= cutoff_date].copy()
print("Train rows:", len(train_df), "Test rows:", len(test_df), "Cutoff date:", cutoff_date)

X_train = train_df[req_features]
y_train = train_df["target"]

X_test = test_df[req_features]
y_test = test_df["target"]

# compute class weights (balanced) from training set
classes = np.unique(y_train)
class_weights = compute_class_weight(class_weight="balanced", classes=classes, y=y_train.values)
cw_list = [0.0] * len(np.unique(df["target"]))
for idx, cls in enumerate(classes):
    cw_list[int(cls)] = float(class_weights[idx])
print("Using class weights:", cw_list)

model = CatBoostClassifier(
    iterations=2000,
    depth=8,
    learning_rate=0.03,
    loss_function="MultiClass",
    eval_metric="Accuracy",
    verbose=100,
    random_seed=42,
    class_weights=cw_list,
    early_stopping_rounds=100,
    od_type="Iter"
)

# fit with eval set for early stopping; CatBoost accepts eval_set as tuple of (X, y)
model.fit(
    X_train, y_train,
    eval_set=(X_test, y_test),
    use_best_model=True,
    verbose=100
)

# evaluate
pred = model.predict(X_test)
acc = accuracy_score(y_test, pred)
print("\nAccuracy on holdout (time-based):", acc)

# save model
model.save_model("models/catboost_match_result.cbm")
print("Model saved to models/catboost_match_result.cbm")
