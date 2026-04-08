import os
import requests
import datetime

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
target = today + datetime.timedelta(days=30)

weekday = target.weekday()

route = None

if weekday in [3,4]:
    route = "東京 → 富山"

if weekday in [6,0]:
    route = "富山 → 東京"

if route:

    message = f"""
🚄トクだ値監視中

対象日
{target}

区間
{route}

優先列車
かがやき / はくたか

👇予約
https://www.eki-net.com/
"""

    send_line(message)