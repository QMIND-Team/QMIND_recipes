import json
ingredients = json.load(open('ingredients_list.json'))
for i in list(ingredients.keys()):
    newKey = i.encode('ascii', 'ignore')
    ingredients[newKey.decode('ascii', 'ignore')] = ingredients.pop(i)

json.dump(ingredients, open('ingredients_list3.json', 'w'))