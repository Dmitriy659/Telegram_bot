import json

ar = []

with open('ban_word.txt') as r:
    for i in r.readlines():
        i = i.lower().strip().split()
        if len(i) != 0:
            for j in i:
                ar.append(j)

with open('cenz.json', 'w', encoding='utf-8') as e:
    json.dump(ar, e, indent=4)

