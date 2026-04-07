import os
import requests

LINE_TOKEN = os.getenv("LINE_CHANNEL_TOKEN")
USER_ID = os.getenv("LINE_USER_ID")

def send_line(message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "to": USER_ID,
        "messages":[
            {
                "type":"text",
                "text": message
            }
        ]
    }

    requests.post(url, headers=headers, json=data)


# テストメッセージ
send_line("🚄 トクだ値監視システムが正常に動いています")
