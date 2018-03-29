#TODO: loaves to loaf, volume measurements to teaspoon, weight to ounces
import json
from sklearn import tree
import pickle
# Importing the necessary modules

volume = ['tablespoon', 'cup', 'pinch', 'quart']
volume_mes = [3, 48, 0.0625, 192]
mes_list = ["N/A", "can", "bag", "bar", "clove", "packet", "ounce", "loaf", "loaves", "package", "teaspoon", "square",
            "container"]
# Arrays containing information for conversions between measurements

features = []
labels = []
# Arrays that will be used in the classifier


ingredients = json.load(open('ingredients_list.json'))['ingredients list']
recipes = json.load(open('recipes.json'))['recipes']    # Creating dictionaries with the necessary data
print(len(recipes))

def recipe_to_data(recipe):
    array = [0] * len(ingredients)*3
    for i in recipe['ingredients']:
            num = list(ingredients.keys()).index(i['name'])
            raw_quant = i['quantity']
            quant = 1 if raw_quant == 'N/A' else raw_quant
            raw_mes = i['measurement']
            if raw_mes == 'loaves':
                raw_mes = 'loaf'
            raw_mes = raw_mes[:-1] if raw_mes.endswith('s') else raw_mes
            if raw_mes in volume:
                mes = 'teaspoon'
                quant = quant*volume_mes[volume.index(raw_mes)]
            elif 'pound' in raw_mes:
                mes = 'ounce'
                quant = quant*16
            else:
                mes = raw_mes
            mes_index = mes_list.index(mes)
            array[num*3] = array[num*3] + quant
            array[num*3+1] = mes_index
            if i['required']:
                array[num*3+2] = 1

    return array


features = []
labels = []
clf = tree.DecisionTreeClassifier()

categories = []


for r in recipes[0:1000]:
    if 'category' in list(r.keys()):
        if r['category'] not in categories:
            categories.append(r['category'].strip())

testA = []
testB = []
def init(n):
    for i in range(0, n):
                features.append(recipe_to_data(recipes[i]))
                labels.append(round(recipes[i]['rating']*10))


init(5000)


clf = clf.fit(features, labels)

s = pickle.dump(clf, open("save.pkl", "wb"), protocol=2)
#clf = pickle.load(open("save.p", "rb"))


print(clf)

for i in range(501,601):
    print(clf.predict([recipe_to_data(recipes[i])]))
