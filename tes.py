import json

rollno = '163g1a0505'
with open(f"src\\results\\{rollno}.json") as target:
    data = target
    data = json.load(data)
print(data)
print(type(data))