import requests
import os
from datetime import datetime, timedelta

LINE_TOKEN = os.getenv("LINE_CHANNEL_TOKEN")
LINE_USER = os.getenv("LINE_USER_ID")

DEP = "東京"
ARR = "富山"

CHECK_DAYS = 30


def send_line(message):

    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "to": LINE_USER,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers=headers,
        json=data
    )


def load_last():

    if not os.path.exists("last_sent.txt"):
        return set()

    with open("last_sent.txt") as f:
        return set(f.read().splitlines())


def save_last(keys):

    with open("last_sent.txt", "w") as f:
        for k in keys:
            f.write(k + "\n")


def get_tokudane():

    results = []

    for i in range(CHECK_DAYS):

        date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")

        # 仮データ（実際はえきねっと解析）
        trains = [
            {"name": "かがやき515号", "dep": "18:24", "arr": "20:32", "discount": 30},
            {"name": "はくたか571号", "dep": "19:24", "arr": "21:52", "discount": 30}
        ]

        valid = []

        for t in trains:

            if t["discount"] == 30:
                valid.append(t)

        if valid:

            results.append({
                "date": date,
                "trains": valid
            })

    return results


def format_message(results):

    msg = "🚄トクだ値30% 発見\n\n"

    for r in results:

        d = datetime.strptime(r["date"], "%Y-%m-%d")
        date_text = f"{d.month}/{d.day}"

        msg += f"{date_text}\n"
        msg += f"{DEP}→{ARR}\n\n"

        for t in r["trains"]:

            msg += f"{t['name']}\n"
            msg += f"{t['dep']} → {t['arr']}\n\n"

        msg += "\n"

    msg += "空席照会\nhttps://www.eki-net.com/"

    return msg


def main():

    last = load_last()
    new_last = set(last)

    results = get_tokudane()

    notify = []

    for r in results:

        key = r["date"]

        if key not in last:

            notify.append(r)
            new_last.add(key)

    if notify:

        message = format_message(notify)
        send_line(message)

    save_last(new_last)


if __name__ == "__main__":
    main()