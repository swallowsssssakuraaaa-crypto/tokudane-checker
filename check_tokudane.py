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

candidates = []

for i in range(1,31):

    target = today + datetime.timedelta(days=i)

    weekday = target.weekday()

    if weekday in [3,4,6,0]:

        if weekday in [3,4]:

            route = "東京 → 富山"

        else:

            route = "富山 → 東京"

        candidates.append((target,route))


if candidates:

    message = "🚄富山おすすめランキング\n\n"

    rank = 1

    for d,r in candidates[:5]:

        message += f"""{rank}位
{d}
{r}

"""

        rank += 1

    message += """
👇えきねっと検索
https://www.eki-net.com/
"""

    send_line(message)