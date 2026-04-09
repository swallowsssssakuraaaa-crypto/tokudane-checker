import os
import requests
from datetime import datetime,timedelta

LINE_TOKEN=os.getenv("LINE_CHANNEL_TOKEN")
LINE_USER=os.getenv("LINE_USER_ID")

FROM="東京"
TO="富山"

CHECK_DAYS=30

def send_line(text):

    headers={
        "Authorization":f"Bearer {LINE_TOKEN}",
        "Content-Type":"application/json"
    }

    body={
        "to":LINE_USER,
        "messages":[{"type":"text","text":text}]
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

def search_tokudane():

    results=[]

    for i in range(CHECK_DAYS):

        d=datetime.now()+timedelta(days=i)

        date=d.strftime("%Y%m%d")

        url=f"https://traininfo.jreast.co.jp/train_info/shinkansen/seat?date={date}&from=東京&to=富山"

        r=requests.get(url)

        if r.status_code!=200:
            continue

        data=r.text

        trains=[]

        lines=data.split("\n")

        for line in lines:

            if "トクだ値30" in line or "トクだ値35" in line or "トクだ値40" in line:

                parts=line.split(",")

                name=parts[0]
                dep=parts[1]
                arr=parts[2]

                discount="30"

                if "35" in line:
                    discount="35"

                if "40" in line:
                    discount="40"

                trains.append({
                    "name":name,
                    "dep":dep,
                    "arr":arr,
                    "discount":discount
                })

        if trains:

            results.append({
                "date":d.strftime("%m/%d"),
                "trains":trains
            })

    return results

def build_message(data):

    text="🚄トクだ値 発見\n\n"

    for r in data:

        text+=f"{r['date']}\n"
        text+=f"{FROM}→{TO}\n\n"

        for t in r["trains"]:

            text+=f"{t['name']}\n"
            text+=f"{t['dep']} → {t['arr']}\n"
            text+=f"割引：{t['discount']}%\n\n"

        text+="\n"

    text+="空席照会\nhttps://www.eki-net.com/"

    return text

def main():

    history=load_history()

    new=set(history)

    results=search_tokudane()

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