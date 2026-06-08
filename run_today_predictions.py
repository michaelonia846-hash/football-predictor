import pandas as pd
import joblib

print("Loading files...")

# Files from current folder
fixtures = pd.read_csv("fixtures_today.csv")
team_stats = pd.read_csv("team_stats.csv")

model_winner = joblib.load("model_winner.pkl")
le_winner = joblib.load("label_encoder_winner.pkl")

print(f"Fixtures loaded: {len(fixtures)}")
print(f"Teams loaded: {len(team_stats)}")

# Clean names
team_stats["Team"] = team_stats["Team"].astype(str).str.strip()
fixtures["HomeTeam"] = fixtures["HomeTeam"].astype(str).str.strip()
fixtures["AwayTeam"] = fixtures["AwayTeam"].astype(str).str.strip()

print("\nToday's Fixtures\n")

for _, row in fixtures.iterrows():

    home_team = row["HomeTeam"]
    away_team = row["AwayTeam"]

    home_rows = team_stats[team_stats["Team"] == home_team]
    away_rows = team_stats[team_stats["Team"] == away_team]

    if home_rows.empty or away_rows.empty:
        print(f"⚠️ Missing stats for {home_team} or {away_team}")
        print()
        continue

    home = home_rows.iloc[0]
    away = away_rows.iloc[0]

    features = pd.DataFrame([{
        "HomeElo": home["Elo"],
        "AwayElo": away["Elo"],
        "EloDiff": home["Elo"] - away["Elo"],

        "HomeFormPoints": home["FormPoints"],
        "AwayFormPoints": away["FormPoints"],
        "FormDiff": home["FormPoints"] - away["FormPoints"],

        "HomeGF5": home["GF5"],
        "AwayGF5": away["GF5"],

        "HomeGA5": home["GA5"],
        "AwayGA5": away["GA5"],

        "HomeAvgGF": home["AvgGF"],
        "AwayAvgGF": away["AvgGF"],

        "HomeAvgGA": home["AvgGA"],
        "AwayAvgGA": away["AvgGA"],

        "HomeScoredRate": home["ScoredRate"],
        "AwayScoredRate": away["ScoredRate"],

        "HomeCleanSheetRate": home["CleanSheetRate"],
        "AwayCleanSheetRate": away["CleanSheetRate"],

        "HomeBTTSRate": home["BTTSRate"],
        "AwayBTTSRate": away["BTTSRate"],

        "HomeOver15Rate": home["Over15Rate"],
        "AwayOver15Rate": away["Over15Rate"]
    }])

    probs = model_winner.predict_proba(features)[0]

    classes = le_winner.inverse_transform(range(len(probs)))

    result_probs = dict(zip(classes, probs))

    home_prob = result_probs.get("H", 0) * 100
    draw_prob = result_probs.get("D", 0) * 100
    away_prob = result_probs.get("A", 0) * 100

    print(f"{home_team} vs {away_team}")
    print(
        f"🏠 Home Win: {home_prob:.1f}% | "
        f"🤝 Draw: {draw_prob:.1f}% | "
        f"✈️ Away Win: {away_prob:.1f}%"
    )

    markets = {
        "Home Win": home_prob,
        "Draw": draw_prob,
        "Away Win": away_prob,
        "Double Chance Home/Draw": home_prob + draw_prob,
        "Double Chance Away/Draw": away_prob + draw_prob,
        "Double Chance Home/Away": home_prob + away_prob
    }

    best_market = max(markets, key=markets.get)

    print(
        f"✅ Best Bet: {best_market} "
        f"({markets[best_market]:.1f}%)"
    )

    print("-" * 60)