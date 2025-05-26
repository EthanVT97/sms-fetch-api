from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_SECRET = os.getenv("API_SECRET")
DEVICE_ID = os.getenv("DEVICE_ID")
SIM = os.getenv("SIM", 1)
PRIORITY = os.getenv("PRIORITY", 1)

@app.route("/", methods=["GET"])
def home():
    return "SMSChef Webhook Listener is running."

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    phone = data.get("phone")
    message = data.get("message")

    if not phone or not message:
        return jsonify({"error": "Missing phone or message"}), 400

    payload = {
        "secret": API_SECRET,
        "mode": "devices",
        "device": DEVICE_ID,
        "sim": SIM,
        "priority": PRIORITY,
        "phone": phone,
        "message": message
    }

    response = requests.post("https://www.cloud.smschef.com/api/send/sms", data=payload)
    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(debug=True)
