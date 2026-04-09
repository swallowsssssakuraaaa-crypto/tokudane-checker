import os
import requests
from datetime import datetime, timedelta

LINE_TOKEN = os.getenv("LINE_CHANNEL_TOKEN")
LINE_USER = os.getenv("LINE_USER_ID")

ROUTES = [
    ("東京","富山"),
    ("上野","富山")
]

CHECK_DAYS = 30

API_URL = "https://www.eki-net.com/ap/api/search"

def send_line(text):

    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }

    body = {
        "to": LINE_USER,
        "messages":[{"type":"text","text":text}]
    }

    requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers=headers,
        json=body
    )

def search_tokudane():

    results = []

    for dep,arr in ROUTES:

        for i in range(CHECK_DAYS):

            date = datetime.now() + timedelta(days=i)

            d = date.strftime("%Y-%m-%d")

            params = {
                "from": dep,
                "to": arr,
                "date": d
            }

            try:

                r = requests.get(API_URL, params=params, timeout=20)

                if r.status_code != 200:
                    continue

                data = r.json()

            except:
                continue

            trains = []

            for t in data.get("trains",[]):

                name = t.get("name","")

                if "かがやき" not in name and "はくたか" not in name:
                    continue

                discount = t.get("discount",0)

                if discount < 30:
                    continue

                if not t.get("available",False):
                    continue

                trains.append({
                    "name": name,
                    "dep": t["dep"],
                    "arr": t["arr"],
                    "discount": discount
                })

            if trains:

                results.append({
                    "date": date.strftime("%m/%d"),
                    "route": f"{dep}→{arr}",
                    "trains": trains
                })

    return results

def build_message(data):

    text = "🚄トクだ値 発見\n\n"

    for r in data:

        text += f"{r['date']}\n"
        text += f"{r['route']}\n\n"

        for t in r["trains"]:

            text += f"{t['name']}\n"
            text += f"{t['dep']} → {t['arr']}\n"
            text += f"割引：{t['discount']}%\n\n"

        text += "\n"

    text += "空席照会\nhttps://www.eki-net.com/"

    return text

def main():

    results = search_tokudane()

    if results:

        msg = build_message(results)

        send_line(msg)

if __name__ == "__main__":
    main()