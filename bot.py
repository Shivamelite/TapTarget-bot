import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GAME_URL = "https://taptargetgame.netlify.app/"

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_message(chat_id, text):
    url = f"{TELEGRAM_API}/sendMessage"

    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "🎯 Play TapTarget",
                    "web_app": {
                        "url": GAME_URL
                    }
                }
            ]
        ]
    }

    requests.post(
        url,
        json={
            "chat_id": chat_id,
            "text": text,
            "reply_markup": keyboard
        }
    )


@app.route("/", methods=["GET"])
def home():
    return "TapTarget Bot is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()

    if not update:
        return "OK"

    message = update.get("message")

    if message:
        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        if text.startswith("/start"):
            send_message(
                chat_id,
                "🎯 Welcome to TapTarget!\n\n"
                "Test your speed, accuracy and reflexes.\n"
                "Tap targets, build combos and beat your high score! 🔥"
            )

        elif text.startswith("/play"):
            send_message(
                chat_id,
                "🎯 Ready? Let's play TapTarget!"
            )

    return "OK"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
