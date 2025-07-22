from trend_decision import get_trend_decision
from tabulate import tabulate
import requests

# Telegram config
BOT_TOKEN = '8046031500:AAGpTEu6uf6-I5fqOQ2h3SqBShZzs1bkSe8'
CHAT_ID = '6614671189'

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            print("✅ Telegram alert sent.")
        else:
            print(f"❌ Failed to send Telegram alert: {r.text}")
    except Exception as e:
        print(f"❌ Error sending alert: {e}")

# Hardcoded input
input_data = {
    "features": {
        "return_1h": 0.0041,
        "rsi_14": 56.8,
        "macd": 0.0152,
        "macd_signal": 0.0127,
        "bb_width": 0.039,
        "volume": 2850000,
        "volume_ema_20": 3100000,
        "roc": -0.0017,
        "stoch_rsi": 0.45,
        "supertrend_signal": 1
    },
    "strike_breached": "CALL",
    "current_spot_price": 118150,
    "reentry_done": False,
    "is_within_reentry_window": True,
    "liquidation_zones": [117000, 116000],
    "whale_activity": {
        "signal_strength": 0.82
    }
}

# Run decision
result = get_trend_decision(input_data)

# Print table
print(tabulate(result.items(), headers=["Field", "Value"], tablefmt="fancy_grid"))

# Always send Telegram alert
confidence_flag = "✅" if result["confidence"] >= 0.6 else "⚠️ Low Confidence"
msg = (
    f"{confidence_flag} *ML Trend Alert*\n"
    f"*Trend:* `{result['ml_trend']}`\n"
    f"*Confidence:* `{result['confidence']}`\n"
    f"*Action:* `{result['action']}`\n"
    f"*Whale Signal:* `{result['whale_signal']}`\n"
    f"*Near Liq Zone:* `{result['near_liquidation_zone']}`"
)
send_telegram_alert(msg)
