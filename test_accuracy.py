import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv("training_data_v6.csv")

X = df[
[
"HomeElo","AwayElo","EloDiff",
"HomeFormPoints","AwayFormPoints","FormDiff",
"HomeGF5","AwayGF5","HomeGA5","AwayGA5",
"HomeAvgGF","AwayAvgGF","HomeAvgGA","AwayAvgGA",
"HomeScoredRate","AwayScoredRate",
"HomeCleanSheetRate","AwayCleanSheetRate",
"HomeBTTSRate","AwayBTTSRate",
"HomeOver15Rate","AwayOver15Rate"
]
]

y = df["Result"]

X_train, X_test, y_train, y_test = train_test_split(
X,
y,
test_size=0.2,
random_state=42
)

model = RandomForestClassifier(
n_estimators=200,
random_state=42
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))
