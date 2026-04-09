import os
import json
import datetime
import requests
import random

LINE_TOKEN=os.environ["LINE_CHANNEL_TOKEN"]
LINE_USER_ID=os.environ["LINE_USER_ID"]

headers={
 "Authorization":f"Bearer {LINE_TOKEN}",
 "Content-Type":"application/json"
}

def send_line(msg):

 payload={
  "to":LINE_USER_ID,
  "messages":[{"type":"text","text":msg}]
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


def create_key(date,route,train):

 return f"{date}_{route['from']}_{route['to']}_{train}"


def build_link(route,date):

 base="https://www.eki-net.com"

 return f"{base}/"


def simulate_train():

 trains=[
  ("かがやき503","06:16"),
  ("かがやき507","08:24"),
  ("かがやき511","10:24"),
  ("はくたか553","13:52"),
  ("はくたか567","18:24"),
  ("かがやき515","19:20"),
 ]

 return random.choice(trains)


def simulate_discount():

 r=random.random()

 if r<0.2:
  return "30%"
 elif r<0.4:
  return "10%"
 else:
  return None


def check():

 routes=load_routes()
 history=load_history()

 today=datetime.date.today()

 for i in range(30):

  d=today+datetime.timedelta(days=i)

  for r in routes:

   train,depart=simulate_train()

   discount=simulate_discount()

   if not discount:
    continue

   key=create_key(str(d),r,train+discount)

   if key in history:
    continue

   link=build_link(r,d)

   msg=f"""
🚄トクだ値{discount} 発見

{d}

{r['from']} → {r['to']}

{train}
{depart}発

空席確認
{link}
"""

   send_line(msg)

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