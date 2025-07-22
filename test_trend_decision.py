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
        if response.status_code != 200:
            print(f"❌ Failed to send Telegram alert: {response.text}")
    except Exception as e:
        print(f"❌ Error sending Telegram alert: {e}")

# Run decision logic
result = get_trend_decision()

if result["confidence"] >= 0.6:
    table = tabulate(result.items(), headers=["Field", "Value"], tablefmt="fancy_grid")
    print(table)

    msg = (
        f"📊 *ML Trend Alert*\n"
        f"*Trend:* `{result['ml_trend']}`\n"
        f"*Confidence:* `{result['confidence']}`\n"
        f"*Action:* `{result['action']}`\n"
        f"*Whale Signal:* `{result['whale_signal']}`\n"
        f"*Near Liq Zone:* `{result['near_liquidation_zone']}`"
    )
    send_telegram_alert(msg)
else:
    print("No strong signal (confidence < 0.6) — skipping alert.")
