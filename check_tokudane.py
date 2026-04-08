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

# 今日の日付
today = datetime.date.today()

# 1ヶ月後（予約対象）
target = today + datetime.timedelta(days=30)

weekday = target.weekday()

message = None

# 木曜 or 金曜 → 東京→富山
if weekday == 3 or weekday == 4:
    message = f"""
🚄トクだ値予約チェック日

東京 → 富山
{target}

優先列車
・かがやき
・はくたか

💡本日10:00に
30%OFFが出る可能性
"""

# 日曜 or 月曜 → 富山→東京
elif weekday == 6 or weekday == 0:
    message = f"""
🚄トクだ値予約チェック日

富山 → 東京
{target}

優先列車
・かがやき
・はくたか

💡本日10:00に
30%OFFが出る可能性
"""

if message:
    send_line(message)