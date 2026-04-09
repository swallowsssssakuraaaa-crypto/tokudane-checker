import requests
import os
from datetime import datetime, timedelta

LINE_TOKEN = os.getenv("LINE_CHANNEL_TOKEN")
LINE_USER = os.getenv("LINE_USER_ID")

FROM = "東京"
TO = "富山"

CHECK_DAYS = 30

def send_line(msg):

    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }

    body = {
        "to": LINE_USER,
        "messages":[
            {
                "type":"text",
                "text":msg
            }
        ]
    }

    requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers=headers,
        json=body
    )

def load_history():

    if not os.path.exists("last_sent.txt"):
        return set()

    with open("last_sent.txt") as f:
        return set(f.read().splitlines())

def save_history(data):

    with open("last_sent.txt","w") as f:
        for d in data:
            f.write(d+"\n")

def fetch_tokudane():

    results=[]

    for i in range(CHECK_DAYS):

        date=(datetime.now()+timedelta(days=i)).strftime("%Y-%m-%d")

        url="https://www.eki-net.com/"

        # 実際の空席解析はここ
        # 今は簡易構造

        trains=[
            {"name":"かがやき515号","dep":"18:24","arr":"20:32","discount":30},
            {"name":"はくたか571号","dep":"19:24","arr":"21:52","discount":35}
        ]

        valid=[]

        for t in trains:

            if t["discount"]>=30:

                valid.append(t)

        if valid:

            results.append({
                "date":date,
                "trains":valid
            })

    return results

def build_message(data):

    text="🚄トクだ値 発見\n\n"

    for d in data:

        dt=datetime.strptime(d["date"],"%Y-%m-%d")

        text+=f"{dt.month}/{dt.day}\n"
        text+=f"{FROM}→{TO}\n\n"

        for t in d["trains"]:

            text+=f"{t['name']}\n"
            text+=f"{t['dep']} → {t['arr']}\n"
            text+=f"割引：{t['discount']}%\n\n"

        text+="\n"

    text+="空席照会\nhttps://www.eki-net.com/"

    return text

def main():

    history=load_history()

    new=set(history)

    results=fetch_tokudane()

    notify=[]

    for r in results:

        key=r["date"]

        if key not in history:

            notify.append(r)

            new.add(key)

    if notify:

        msg=build_message(notify)

        send_line(msg)

    save_history(new)

if __name__=="__main__":
    main()