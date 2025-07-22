import joblib
import pandas as pd

# Load model
model = joblib.load("trend_model.pkl")

# Print feature names (optional debug)
print("📋 Expected features:")
print(model.feature_names_in_)

def get_trend_decision(input_data):
    features = input_data["features"]
    strike_breached = input_data["strike_breached"]
    current_spot = input_data["current_spot_price"]
    reentry_done = input_data["reentry_done"]
    within_window = input_data["is_within_reentry_window"]
    liquidation_zones = input_data["liquidation_zones"]
    whale_signal = input_data["whale_activity"]["signal_strength"]

    # Predict
    X = pd.DataFrame([features])
    ml_trend = model.predict(X)[0]
    confidence = float(model.predict_proba(X).max())

    # Check if current price is near a liquidation zone
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
    elif ml
