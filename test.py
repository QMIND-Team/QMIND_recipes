import json

recipes = json.load(open('recipes2.json'))    # Creating dictionaries with the necessary data
categories = []


for r in recipes[0:1000]:
    if 'category' in list(r.keys()):
        if r['category'] not in categories:
            categories.append(r['category'].strip())

print(categories)
