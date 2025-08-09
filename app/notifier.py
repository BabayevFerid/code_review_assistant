import requests
from app.config import SLACK_WEBHOOK_URL

def send_slack_message(message: str):
    payload = {
        "text": message
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    response.raise_for_status()
