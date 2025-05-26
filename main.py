from flask import Flask, jsonify
import requests
import re

app = Flask(__name__)

API_KEY = "2f6fefcafc7c0f8a0889fc1cbca41b0d92dddaf5"
PHONE_NUMBER = "+959421072418"
API_URL = f"https://api.smschef.com/v1/messages?api_key={API_KEY}&number={PHONE_NUMBER}"

def extract_otp(text):
    match = re.findall(r"\b\d{4,8}\b", text)
    return match[0] if match else None

@app.route("/")
def home():
    return "SMS Fetcher API is running."

@app.route("/check_sms", methods=["GET"])
def check_sms():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        messages = data.get("messages", [])

        if not messages:
            return jsonify({"status": "ok", "message": "No SMS found"})

        latest = messages[0]
        otp = extract_otp(latest["text"])
        return jsonify({
            "from": latest["from"],
            "message": latest["text"],
            "received_at": latest["received_at"],
            "otp": otp or "not found"
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
