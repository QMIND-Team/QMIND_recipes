import requests
import json
import re,string
from bs4 import BeautifulSoup
from user_agent import generate_user_agent


def get_proxy():
    r = requests.get('https://sslproxies.org/')
    soup = BeautifulSoup(r.text, 'html.parser')
    raw_data = soup.find('tbody')
    raw_rows = raw_data.findAll('tr')
    for i in raw_rows:
        vals = i.findAll('td')
        temp1 = vals[0].text
        temp2 = vals[1].text
        temp = 'http://'+temp1+':'+temp2
        print('trying ' + temp)
        try:
            if temp2 != '3128':
                raise Exception
            get_meal('oooh-baby-chocolate-prune-cake', temp)
            print("It worked!")
            return temp
        except Exception:
            print("Didn't work")
    return ''
# This method scrapes a free proxy website that updates regularly to find a working proxy


def get_name(soup):
    tag = soup.find('h1', attrs = {'class': 'recipe-summary__h1'})
    return tag.contents[0].replace('�', '')


def get_meal(name, proxy):
    url = 'http://allrecipes.com/recipe/' + name
    req = requests.get(url, proxies={'http': proxy},
                     headers={'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))})
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    try:
        tag = soup.findAll('span', attrs = {'class': 'toggle-similar__title', 'itemprop': 'name'})[2]
        return tag.contents[0].strip()
    except AttributeError:
        return "N/A"
    except IndexError:
        tag = soup.findAll('span', attrs = {'class': 'toggle-similar__title', 'itemprop': 'name'})
        return tag[len(tag) - 1].contents[0]

def find_index(key, test):
    counter = 0
    for i in test:
        if i['name'] == key:
            return counter
        else:
            counter = counter + 1
    return -1

recipes = json.load(open('recipes.json'))['recipes']
i = 8000
proxy = get_proxy()
regex = re.compile("['ï¿½?!]")
counter = 0
while i < 13027:
    try:
        url = 'http://allrecipes.com/recipe/' + str(i)
        req = requests.get(url, proxies={'http': proxy},
                           headers={'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))})
        page = req.text
        soup = BeautifulSoup(page, 'html.parser')
        name = get_name(soup)
        try:
            tag = soup.findAll('span', attrs={'class': 'toggle-similar__title', 'itemprop': 'name'})[2]
            meal = tag.contents[0].strip()
        except AttributeError:
            meal =  "N/A"
        except IndexError:
            tag = soup.findAll('span', attrs={'class': 'toggle-similar__title', 'itemprop': 'name'})
            meal =  tag[len(tag) - 1].contents[0]
        index = find_index(name, recipes)
        print(index)
        if index is not -1:
            recipes[index]['category'] = meal
        print(str(i-7999)+' out of 5000')
        i = i + 1
    except Exception as e:
        print(e)
        proxy = ''
        while proxy == '':
            proxy = get_proxy()
        print('Using proxy ' + proxy)
        if counter < 1:
            counter = counter + 1
        else:
            i = i+1
            counter = 0

with open('recipes2.json', 'w') as fp:
    json.dump(recipes, fp)
print('finished')