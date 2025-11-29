from flask import Flask, request
import requests
import openai
import os

app = Flask(__name__)

# Load environment variables (do NOT put keys in code!)
ULTRA_INSTANCE = os.getenv("ULTRA_INSTANCE")
ULTRA_TOKEN = os.getenv("ULTRA_TOKEN")
CHATGPT_API_KEY = os.getenv("CHATGPT_API_KEY")

openai.api_key = CHATGPT_API_KEY


def send_message(to, text):
    url = f"https://api.ultramsg.com/{ULTRA_INSTANCE}/messages/chat"
    payload = {
        "token": ULTRA_TOKEN,
        "to": to,
        "body": text
    }
    requests.post(url, data=payload)


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    sender = data.get("from")
    message = data.get("body")

    # ChatGPT reply
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message}]
    )
    reply = response["choices"][0]["message"]["content"]

    send_message(sender, reply)
    return "OK", 200


@app.route("/")
def home():
    return "Your WhatsApp Bot is running safely!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

