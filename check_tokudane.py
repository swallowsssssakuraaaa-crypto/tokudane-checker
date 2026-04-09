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

 payload={
  "to":LINE_USER_ID,
  "messages":[
   {
    "type":"text",
    "text":text
   }
  ]
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


def create_key(date,train,route):

 return f"{date}_{route['from']}_{route['to']}_{train}"


def search_url(route,date):

 base="https://www.eki-net.com"

 return f"{base}/"


def check():

 routes=load_routes()

 history=load_history()

 today=datetime.date.today()

 for i in range(30):

  d=today+datetime.timedelta(days=i)

  for r in routes:

   train="はくたか553"
   depart="13:52"

   key=create_key(str(d),train,r)

   if key in history:
    continue

   url=search_url(r,d)

   message=f"""
🚄トクだ値30% 発見

{d}

{r['from']} → {r['to']}

{train}
{depart}発

予約
{url}
"""

   send_line(message)

   history[key]=True

   save_history(history)

   return


def main():

 now=datetime.datetime.now().time()

 start=datetime.time(5,30)
 end=datetime.time(23,50)

 if start<=now<=end:
  check()


if __name__=="__main__":
 main()