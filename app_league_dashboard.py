import streamlit as st
import pandas as pd
import joblib
import warnings
warnings.filterwarnings("ignore")

# --- Load models & encoders ---
model_path = "model_winner.pkl"
le_path = "label_encoder_winner.pkl"

model_winner = joblib.load(model_path)
le_winner = joblib.load(le_path)

# --- Load team stats ---
team_stats = pd.read_csv("team_stats.csv")
teams_with_stats = set(team_stats["Team"])

# --- Load today's fixtures ---
fixtures = pd.read_csv("fixtures_today.csv")

st.title("⚽ Football League Dashboard")
st.subheader("Today's Matches")

skipped = 0  # Counter for missing teams

for _, row in fixtures.iterrows():
    home_team = row["HomeTeam"]
    away_team = row["AwayTeam"]

    # Skip matches if either team is missing
    if home_team not in teams_with_stats or away_team not in teams_with_stats:
        skipped += 1
        continue  # Skip this match

    # Get stats
    home = team_stats[team_stats["Team"] == home_team].iloc[0]
    away = team_stats[team_stats["Team"] == away_team].iloc[0]

    # --- Features for prediction ---
    features = pd.DataFrame([{
        "HomeElo": home["Elo"], "AwayElo": away["Elo"], "EloDiff": home["Elo"] - away["Elo"],
        "HomeFormPoints": home["FormPoints"], "AwayFormPoints": away["FormPoints"], "FormDiff": home["FormPoints"] - away["FormPoints"],
        "HomeGF5": home["GF5"], "AwayGF5": away["GF5"], "HomeGA5": home["GA5"], "AwayGA5": away["GA5"],
        "HomeAvgGF": home["AvgGF"], "AwayAvgGF": away["AvgGF"], "HomeAvgGA": home["AvgGA"], "AwayAvgGA": away["AvgGA"],
        "HomeScoredRate": home["ScoredRate"], "AwayScoredRate": away["ScoredRate"],
        "HomeCleanSheetRate": home["CleanSheetRate"], "AwayCleanSheetRate": away["CleanSheetRate"],
        "HomeBTTSRate": home["BTTSRate"], "AwayBTTSRate": away["BTTSRate"],
        "HomeOver15Rate": home["Over15Rate"], "AwayOver15Rate": away["Over15Rate"]
    }])

    # --- Prediction ---
    probs_winner = model_winner.predict_proba(features)[0]
    classes = le_winner.inverse_transform(range(len(probs_winner)))
    results_winner = dict(zip(classes, probs_winner))

    home_prob = results_winner.get("H", 0) * 100
    draw_prob = results_winner.get("D", 0) * 100
    away_prob = results_winner.get("A", 0) * 100

    st.write(f"**{home_team} vs {away_team}**")
    st.write(f"🏠 Home Win: {home_prob:.1f}% | 🤝 Draw: {draw_prob:.1f}% | ✈️ Away Win: {away_prob:.1f}%")

    # --- Best market ---
    market_probs = {
        "Home Win": home_prob,
        "Draw": draw_prob,
        "Away Win": away_prob,
        "Double Chance Home/Draw": home_prob + draw_prob,
        "Double Chance Away/Draw": away_prob + draw_prob,
        "Double Chance Home/Away": home_prob + away_prob
    }
    best_market = max(market_probs, key=market_probs.get)
    best_prob = market_probs[best_market]
    st.success(f"✅ Best Bet: {best_market} ({best_prob:.1f}%)")
    st.write("---")

# Optional: show summary of skipped matches
if skipped > 0:
    st.info(f"⚠️ Skipped {skipped} match(es) with missing stats")