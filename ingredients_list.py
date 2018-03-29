# Created by Joey Tepperman on March 1st 2018
# This program adds an ingredients list to recipes.json
import json
import io
data = json.load(open('recipes.json', 'r', encoding='utf-8'))
ing_list = {}
for recipe in data['recipes']:
    for ing in recipe['ingredients']:
        if not ing['name'] in ing_list:
            ing_list[ing['name']] = [ing['measurement']]
        else:
            if not ing['measurement'] in ing_list[ing['name']]:
                ing_list[ing['name']].append(ing['measurement'])

ing_list_final = {}

for i in sorted(list(ing_list.keys())):
    ing_list_final[i] = ing_list[i]
final_dict = {'ingredients_list':ing_list_final}
with io.open('ingredients_list.json', 'w', encoding='utf-8') as fp:
    json.dump(final_dict, fp)
print(len(ing_list))