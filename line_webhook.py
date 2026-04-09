import os
import json
from flask import Flask, request
import requests

app = Flask(__name__)

LINE_TOKEN = os.environ["LINE_CHANNEL_TOKEN"]

headers = {
 "Authorization": f"Bearer {LINE_TOKEN}",
 "Content-Type": "application/json"
}

def reply(token, text):

 payload = {
  "replyToken": token,
  "messages":[{"type":"text","text":text}]
 }

 requests.post(
  "https://api.line.me/v2/bot/message/reply",
  headers=headers,
  json=payload
 )


@app.route("/callback", methods=["POST"])
def callback():

 data = request.json

 event = data["events"][0]

 token = event["replyToken"]

 msg = event["message"]["text"]

 if "/" in msg:

  date = msg

  text=f"""
🚄えきねっと検索

{date}

東京→富山
https://www.eki-net.com/

上野→富山
https://www.eki-net.com/
"""

  reply(token, text)

 return "ok"


if __name__ == "__main__":
 app.run()