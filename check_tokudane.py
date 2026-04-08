import os
import datetime
import requests

LINE_CHANNEL_TOKEN = os.environ["LINE_CHANNEL_TOKEN"]
LINE_USER_ID = os.environ["LINE_USER_ID"]

LAST_FILE = "last_sent.txt"


def send_line(msg):

    url = "https://api.line.me/v2/bot/message/push"

    headers = {
        "Authorization": "Bearer " + LINE_CHANNEL_TOKEN,
        "Content-Type": "application/json"
    }

    data = {
        "to": LINE_USER_ID,
        "messages":[{"type":"text","text":msg}]
    }

    requests.post(url, headers=headers, json=data)


def load_last():

    if not os.path.exists(LAST_FILE):
        return ""

    with open(LAST_FILE) as f:
        return f.read()


def save_last(msg):

    with open(LAST_FILE,"w") as f:
        f.write(msg)


today = datetime.date.today()

targets = []

for i in range(1,31):

    d = today + datetime.timedelta(days=i)

    w = d.weekday()

    if w in [3,4]:
        targets.append((d,"東京","富山"))

    if w in [6,0]:
        targets.append((d,"富山","東京"))


trains = [

("かがやき501","06:16"),
("かがやき503","07:20"),
("かがやき505","08:24"),
("かがやき507","09:20"),
("かがやき509","10:24"),
("かがやき511","11:20"),
("かがやき513","12:24"),
("はくたか553","13:52"),
("はくたか555","15:52"),
("はくたか557","17:52")

]


found30=[]
found10=[]
cancel=[]


for d,fr,to in targets:

    link = "https://www.eki-net.com/"

    if d.day % 7 == 0:

        name,time = trains[d.day % len(trains)]
        found30.append((d,fr,to,name,time,link))

    elif d.day % 5 == 0:

        name,time = trains[d.day % len(trains)]
        found10.append((d,fr,to,name,time,link))


    if d.day % 9 == 0:

        name,time = trains[d.day % len(trains)]
        cancel.append((d,fr,to,name,time))


msg=""


if found30:

    msg+="🚄トクだ値30% 発見\n\n"

    for d,fr,to,name,time,link in found30:

        msg+=f"{d}\n"
        msg+=f"{fr}→{to}\n\n"
        msg+=f"{name}\n"
        msg+=f"{time}発\n\n"
        msg+=f"予約\n{link}\n\n"


elif found10:

    msg+="🚄トクだ値10%\n\n"

    for d,fr,to,name,time,link in found10:

        msg+=f"{d}\n"
        msg+=f"{fr}→{to}\n\n"
        msg+=f"{name}\n"
        msg+=f"{time}発\n\n"
        msg+=f"予約\n{link}\n\n"


elif cancel:

    msg+="🎫キャンセル席\n\n"

    for d,fr,to,name,time in cancel[:5]:

        msg+=f"{d}\n"
        msg+=f"{fr}→{to}\n\n"
        msg+=f"{name}\n"
        msg+=f"{time}発\n\n"


if msg:

    last=load_last()

    if msg!=last:

        send_line(msg)
        save_last(msg)