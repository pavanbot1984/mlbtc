# ===============================================
# File: test_trend_decision.py
# Purpose: Run ML trend decision using input_data.json
# - Reads input features from local JSON file
# - Calls get_trend_decision() with structured data
# - Prints decision table and sends Telegram alert if needed
# ===============================================

import json
import requests
from trend_decision import get_trend_decision
from tabulate import tabulate

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
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Telegram alert sent.")
        else:
            print(f"❌ Failed to send Telegram alert: {response.text}")
    except Exception as e:
        print(f"❌ Exception during Telegram alert: {e}")

# 🔄 Load input_data from JSON file
with open("input_data.json", "r") as f:
    input_data = json.load(f)

# 🚀 Run trend decision logic
result = get_trend_decision(input_data)

# 📋 Display result
table = tabulate(result.items(), headers=["Field", "Value"], tablefmt="fancy_grid")
print(table)

# 🚨 Alert if confidence ≥ 0.6
msg = (
    f"📊 *ML Trend Alert*\n"
    f"*Trend:* `{result['ml_trend']}`\n"
    f"*Confidence:* `{result['confidence']}`\n"
    f"*Action:* `{result['action']}`\n"
    f"*Whale Signal:* `{result['whale_signal']}`\n"
    f"*Near Liq Zone:* `{result['near_liquidation_zone']}`"
)
send_telegram_alert(msg)
