import os
import json
import datetime
import requests

LINE_TOKEN = os.environ["LINE_CHANNEL_TOKEN"]
LINE_USER_ID = os.environ["LINE_USER_ID"]

headers = {
 "Authorization": f"Bearer {LINE_TOKEN}",
 "Content-Type": "application/json"
}

def send_line(text):

 payload = {
  "to": LINE_USER_ID,
  "messages":[{"type":"text","text":text}]
 }

 requests.post(
  "https://api.line.me/v2/bot/message/push",
  headers=headers,
  json=payload
 )


def load_routes():

 with open("routes.json") as f:
  return json.load(f)


def load_history():

 if not os.path.exists("last_sent.json"):
  return {}

 with open("last_sent.json") as f:
  return json.load(f)


def save_history(data):

 with open("last_sent.json","w") as f:
  json.dump(data,f)


def build_key(date, route):

 return f"{date}_{route['from']}_{route['to']}"


def build_link():

 return "https://www.eki-net.com/"


def check_tokudane():

 routes = load_routes()
 history = load_history()

 today = datetime.date.today()

 for i in range(30):

  date = today + datetime.timedelta(days=i)

  for route in routes:

   key = build_key(str(date), route)

   if key in history:
    continue

   message=f"""
🚄トクだ値チェック

{date}

{route['from']} → {route['to']}

空席確認
https://www.eki-net.com/
"""

   send_line(message)

   history[key]=True
   save_history(history)

   return


def main():

 now = datetime.datetime.now().time()

 start = datetime.time(5,30)
 end = datetime.time(23,50)

 if start <= now <= end:
  check_tokudane()


if __name__ == "__main__":
 main()