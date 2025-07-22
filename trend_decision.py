import sys
import json
import joblib
import pandas as pd

# Debug info (plain text)
print("Using Python:", sys.executable)
print("sys.path:", sys.path)

# Load model
model = joblib.load("trend_model.pkl")

# Read input JSON from stdin
input_json = sys.stdin.read()
input_data = json.loads(input_json)

# Extract features
features = input_data["features"]
strike_breached = input_data["strike_breached"]
current_spot = input_data["current_spot_price"]
reentry_done = input_data["reentry_done"]
within_window = input_data["is_within_reentry_window"]
liquidation_zones = input_data["liquidation_zones"]
whale_signal = input_data["whale_activity"]["signal_strength"]

# Create DataFrame with correct feature names
X = pd.DataFrame([features])

# Predict
ml_trend = model.predict(X)[0]
confidence = float(model.predict_proba(X).max())

# Check if near any liquidation zone
near_liq_zone = any(abs(current_spot - z) <= 300 for z in liquidation_zones)

# Decision logic
action = "none"
reason = ""

if strike_breached == "CALL" and ml_trend == "bearish" and confidence >= 0.7:
    action = "hedge_short"
    reason = "CALL breached, bearish trend confirmed"
elif strike_breached == "PUT" and ml_trend == "bullish" and confidence >= 0.7:
    action = "hedge_long"
    reason = "PUT breached, bullish trend confirmed"
elif ml_trend == "neutral" and not reentry_done and within_window:
    action = "reenter"
    reason = "Neutral trend and reentry window open"

# Output decision
output = {
    "ml_trend": ml_trend,
    "confidence": round(confidence, 3),
    "action": action,
    "reason": reason,
    "whale_signal": whale_signal,
    "near_liquidation_zone": near_liq_zone
}

print(json.dumps(output))
