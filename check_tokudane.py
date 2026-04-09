import os
import asyncio
from datetime import datetime, timedelta
from playwright.async_api import async_playwright
import requests

LINE_TOKEN = os.getenv("LINE_CHANNEL_TOKEN")
LINE_USER = os.getenv("LINE_USER_ID")

ROUTES = [
    ("東京","富山"),
    ("上野","富山")
]

CHECK_DAYS = 30


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


async def search():

    results = []

    async with async_playwright() as p:

        browser = await p.chromium.launch()
        page = await browser.new_page()

        for dep,arr in ROUTES:

            for i in range(CHECK_DAYS):

                date = datetime.now()+timedelta(days=i)
                d = date.strftime("%Y-%m-%d")

                url=f"https://www.eki-net.com/top/jrticket/guide/reserve/?from={dep}&to={arr}&date={d}"

                await page.goto(url)

                await page.wait_for_timeout(5000)

                content=await page.content()

                lines=[]

                for l in content.split("\n"):

                    if "かがやき" in l or "はくたか" in l:

                        if "30%" in l or "35%" in l or "40%" in l:

                            lines.append(l.strip())

                if lines:

                    results.append((date.strftime("%m/%d"),dep,arr,lines))

        await browser.close()

    return results


async def main():

    data=await search()

    if not data:
        return

    msg="🚄トクだ値 発見\n\n"

    for d,dep,arr,lines in data:

        msg+=f"{d}\n{dep}→{arr}\n\n"

        for l in lines:

            msg+=l+"\n"

        msg+="\n"

    msg+="空席照会\nhttps://www.eki-net.com/"

    send_line(msg)


asyncio.run(main())