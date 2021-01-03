import json

with open('conf.json') as f:
    a = json.loads(f.read())

for i,j in a.items():
    print(j)
