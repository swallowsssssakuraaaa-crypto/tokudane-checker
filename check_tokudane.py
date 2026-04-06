import json

print("Tokudane checker running")

with open("conditions.json") as f:
    data = json.load(f)

for route in data["routes"]:
    print(route)