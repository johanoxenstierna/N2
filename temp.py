import json

with open('./data.json', 'r') as f:
     raw = json.load(f)

the_json = json.loads(raw[0]['json'])


ff = 5