import os
import requests
import datetime
import json

LINE_CHANNEL_TOKEN = os.environ["LINE_CHANNEL_TOKEN"]
LINE_USER_ID = os.environ["LINE_USER_ID"]

def send_line(message):

    url = "https://api.line.me/v2/bot/message/push"

    headers = {
        "Authorization": "Bearer " + LINE_CHANNEL_TOKEN,
        "Content-Type": "application/json"
    }

    data = {
        "to": LINE_USER_ID,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    requests.post(url, headers=headers, json=data)

today = datetime.date.today()

messages = []

for i in range(1,31):

    target = today + datetime.timedelta(days=i)

    weekday = target.weekday()

    # あなたの移動パターン
    if weekday in [3,4,6,0]:

        messages.append(
f"""
🚄富山チャンス日

日付
{target}

区間
東京 ↔ 富山

優先列車
かがやき
はくたか

👇検索
https://www.eki-net.com/
"""
        )

if messages:

    send_line("\n".join(messages))