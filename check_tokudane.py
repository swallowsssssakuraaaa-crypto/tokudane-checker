import json
import requests

print("Tokudane checker running")

with open("conditions.json") as f:
    data = json.load(f)

for route in data["routes"]:
    print(f'Checking {route["from"]} → {route["to"]}')
    
    # 仮チェック（あとでえきねっと検索に変更）
    if route["from"] == "東京" and route["to"] == "富山":
        print("Tokudane 30% chance detected!")