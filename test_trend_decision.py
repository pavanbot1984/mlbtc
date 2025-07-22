import pandas as pd
from trend_decision import get_trend_decision

# Example input_data (static, replace with live values later if needed)
input_data = {
    "features": {
        "return_1h": 0.015,
        "rsi_14": 68.2,
        "macd": 0.45,
        "macd_signal": 0.35,
        "bb_width": 0.055,
        "volume": 210000,
        "volume_ema_20": 190000,
        "roc": 1.02,
        "stoch_rsi": 0.75,
        "supertrend_signal": 1
    },
    "strike_breached": "PUT",
    "current_spot_price": 119200,
    "reentry_done": False,
    "is_within_reentry_window": True,
    "liquidation_zones": [117000, 121000],
    "whale_activity": {
        "signal_strength": 0.6
    }
}

# Run prediction
try:
    decision = get_trend_decision(input_data)
    print("✅ Trend Decision Result:")
    for key, value in decision.items():
        print(f"{key}: {value}")
except Exception as e:
    print("❌ ERROR in trend decision logic:")
    print(str(e))
