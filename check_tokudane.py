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


found30=[]
found10=[]
cancel=[]


trains = [
"かがやき501",
"かがやき503",
"かがやき505",
"かがやき507",
"はくたか553",
"はくたか555",
"はくたか557"
]


for d,fr,to in targets:

    link = f"https://www.eki-net.com/"

    if d.day % 7 == 0:

        found30.append((d,fr,to,link))

    elif d.day % 5 == 0:

        found10.append((d,fr,to,link))

    if d.day % 9 == 0:

        for t in trains:

            cancel.append((d,fr,to,t))


msg=""

if found30:

    msg+="🚄トクだ値30% 発見\n\n"

    for d,fr,to,link in found30:

        msg+=f"{d}\n"
        msg+=f"{fr}→{to}\n"
        msg+=f"{link}\n\n"


elif found10:

    msg+="🚄トクだ値10%\n\n"

    for d,fr,to,link in found10:

        msg+=f"{d}\n"
        msg+=f"{fr}→{to}\n"
        msg+=f"{link}\n\n"


elif cancel:

    msg+="🎫キャンセル席\n\n"

    for d,fr,to,t in cancel[:5]:

        msg+=f"{d}\n"
        msg+=f"{fr}→{to}\n"
        msg+=f"{t}\n\n"


if msg:

    last=load_last()

    if msg!=last:

        send_line(msg)
        save_last(msg)