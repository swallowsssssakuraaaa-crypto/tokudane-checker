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

        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for dep, arr in ROUTES:

            for i in range(CHECK_DAYS):

                date = datetime.now() + timedelta(days=i)
                date_str = date.strftime("%Y%m%d")
                label_date = date.strftime("%m/%d")

                # 🔥 直接検索URL（ここが最大の修正）
                url = f"https://www.eki-net.com/top/jrticket/seat/SeatReserveTop.action?departure={dep}&arrival={arr}&departureDate={date_str}"

                await page.goto(url, timeout=60000)

                # ページ安定待ち
                await page.wait_for_timeout(7000)

                items = await page.locator("li").all()

                trains = []

                for item in items:

                    text = await item.inner_text()

                    if ("かがやき" not in text and "はくたか" not in text):
                        continue

                    if "つるぎ" in text:
                        continue

                    if "30%" not in text and "35%" not in text:
                        continue

                    if "空席" not in text:
                        continue

                    lines = [l.strip() for l in text.split("\n") if l.strip()]

                    try:
                        name = lines[0]
                        time = next(l for l in lines if "→" in l)
                        discount = next(l for l in lines if "%" in l)
                    except:
                        continue

                    trains.append({
                        "name": name,
                        "time": time,
                        "discount": discount
                    })

                if trains:
                    results.append({
                        "date": label_date,
                        "route": f"{dep}→{arr}",
                        "trains": trains
                    })

        await browser.close()

    return results

async def main():

    data = await search()

    if not data:
        return

    msg = "🚄トクだ値 発見\n\n"

    for r in data:

        msg += f"{r['date']}\n{r['route']}\n\n"

        for t in r["trains"]:
            msg += f"{t['name']}\n{t['time']}\n{t['discount']}\n\n"

        msg += "\n"

    msg += "空席照会\nhttps://www.eki-net.com/"

    send_line(msg)

asyncio.run(main())