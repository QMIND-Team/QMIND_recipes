# Created by Joey Tepperman on February 25th 2018 for QMIND
# This program cleans up the previously collected recipe data
import json

raw_data = []   # An empty array that will be filled with the raw data from the CSV
clean_data = [] # An empty array that will be filled with the cleaned data
mes_list = [" cup", " can ", " cans ", " bag ", " bags ", " bar ", " bars ", " pinch", " quart", " pound",
            " clove", " packet", " ounce", " loaf", " loaves", " package", " teaspoon", " tablespoon", " square", " container"]


def get_mes(name):
    for m in mes_list[::-1]:
        if m in name and not m+")" in name:
            return m.replace(" ", "")
    return "N/A"


def str_to_time(string):
    if 'N/A' in string:
        return "N/A"
    tim = 0
    sp = string.split(' ')
    i = 0
    while i < len(sp):
        if sp[i+1] == "m":
            tim += int(sp[i])
        elif sp[i+1] == "h":
            tim += int(sp[i])*60
        elif sp[i+1] == "d":
            tim += int(sp[i])*60*24
        i += 2
    return tim


def valid_num(num):
    try:
        return float(num)
    except ValueError:
        if "/" in num:
            array = num.split("/")
            try:
                return float(array[0]) / float(array[1])
            except Exception:
                return "N/A"
        else:
            return "N/A"


def contains_num(string):
    for s in string.split(" "):
        if not valid_num(s) == "N/A":
            return True
    return False


with open('recipes.csv') as txtfile:
    line = txtfile.readline()
    while line != '':
        raw_data.append(line)
        line = txtfile.readline()

for line in raw_data:
    l = line.split(" // ")
    l[len(l)-1] = l[len(l)-1][:-4]
    ing = l[1:]
    ingredients = []
    front = l[0].split(", ")
    head = front.pop()
    done = False
    while not done:
        try:
            temp = float(front[len(front)-1])
            done = True
        except Exception:
            head += ", " + front.pop()
    ing.insert(0, head)
    rating = float(front.pop())
    time = front.pop()
    name = ''
    for i in front:
        name += i + ', '
    for i in ing:
        required = True
        splitted = i.split(", ")
        if contains_num(splitted[0]) or len(splitted) == 1:
            ing_name = splitted[0]
        else: ing_name = splitted[1]
        ing_list = ing_name.split(" ")
        ing_name = ''
        add = True
        for j in ing_list:
            if "(" in j and not ")" in j:
                add = False
            if "(" in j or ")" in j:
                if j == "(optional)":
                    required = False
            elif add and valid_num(j) == "N/A" and get_mes(" "+j) == "N/A" and get_mes(" "+j[:-1]):
                ing_name += j+" "
            if ")" in j:
                add = True
        inq_quantity = "N/A"
        ing_mes = "N/A"
        try:
            ing_quantity = valid_num(ing_list[0])
            if not valid_num(ing_list[1]) == "N/A":
                ing_quantity += valid_num(ing_list[1])
        except Exception:
            print("Exception")
        try:
            ing_mes = get_mes(i)
        except Exception:
            print("Exception")
        ingredients.append({"name_raw": i, "name": ing_name[:-1], "quantity": ing_quantity, "measurement": ing_mes, "required": required})
    clean_data.append({"name": name[:-2], "time(mins)":str_to_time(time), "rating": rating, "ingredients": ingredients})

for recipe in clean_data:
    if 'cake compressed ' in recipe['name']:
        recipe['name'] = recipe['name'].replace('cake compressed ', '')
        recipe['measurement'] = 'cake'
    for ing in recipe['ingredients']:
        if 'pinch ' in ing['name']:
            ing['name'] = ing['name'].replace('pinch ', '')
        if ing['name'] == 'ground':
            ing['name'] += ' cloves'
        if 'can ' in ing['name'] or 'cans ' in ing['name'] and not 'ican' in ing['name'] and not 'ecan' in ing['name']:
            if 'cans ' in ing['name']:
                ing['name'] = ing['name'].replace('cans ', '')
            else:
                ing['name'] = ing['name'].replace('can ', '')
        if 'For the' in ing['name']:
            recipe['ingredients'].remove(ing)

final_dict = {"recipes": clean_data}

with open('recipes.json', 'w') as fp:
    json.dump(final_dict, fp)
print('finished')