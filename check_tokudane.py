import os
import datetime
import requests
from playwright.sync_api import sync_playwright

LINE_CHANNEL_TOKEN = os.environ["LINE_CHANNEL_TOKEN"]
LINE_USER_ID = os.environ["LINE_USER_ID"]

EKINET_ID = os.environ["EKINET_ID"]
EKINET_PASS = os.environ["EKINET_PASS"]

LAST_FILE = "last_sent.txt"


def send_line(msg):

    url = "https://api.line.me/v2/bot/message/push"

    headers = {
        "Authorization": "Bearer " + LINE_CHANNEL_TOKEN,
        "Content-Type": "application/json"
    }

    data = {
        "to": LINE_USER_ID,
        "messages": [{"type": "text","text": msg}]
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

    if w in [3,4,6,0]:

        if w in [3,4]:
            targets.append((d,"東京","富山"))
        else:
            targets.append((d,"富山","東京"))


found = []


with sync_playwright() as p:

    browser = p.chromium.launch()
    page = browser.new_page()

    page.goto("https://www.eki-net.com/")

    page.click("text=ログイン")

    page.fill("input[name='id']", EKINET_ID)
    page.fill("input[name='password']", EKINET_PASS)

    page.click("button[type='submit']")

    page.wait_for_timeout(5000)

    for d,fr,to in targets[:10]:

        url = f"https://www.eki-net.com/top/jrticket/guide/reserve/?date={d}"

        page.goto(url)

        html = page.content()

        if "トクだ値" in html and "30%" in html:

            found.append(f"{d} {fr}→{to}")

    browser.close()


if found:

    message = "🚄トクだ値30% 発見！\n\n"

    for f in found:
        message += f + "\n"

    message += "\nえきねっとで予約！"

    last = load_last()

    if message != last:

        send_line(message)
        save_last(message)