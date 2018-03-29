# Created by Joey Tepperman on Febraury 22nd 2018 for QMIND
# This program scrapes allrecipes.com using a proxy rotator and compiles a CSV with data about 11,000 recipes

import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
# importing the necessary modules


def get_meal(soup):
    try:
        tag = soup.findAll('span', attrs = {'class': 'toggle-similar__title', 'itemprop': 'name'})[2]
        return tag.contents[0].strip()
    except AttributeError:
        return "N/A"
    except IndexError:
        tag = soup.findAll('span', attrs = {'class': 'toggle-similar__title', 'itemprop': 'name'})
        return tag[len(tag) - 1].contents[0]




def get_time(soup):
    try:
        tag = soup.find('span', attrs = {'class': 'ready-in-time'})
        return tag.contents[0]
    except AttributeError:
        return "N/A"
# a method that returns the time it takes to cook a recipe


def get_name(soup):
    tag = soup.find('h1', attrs = {'class': 'recipe-summary__h1'})
    return tag.contents[0].replace('�', '')
# a method that returns the name of a recipe


def get_rating(soup):
    tag = soup.find('div', attrs={'class': 'rating-stars'})
    return tag['data-ratingstars']
# a method that returns the rating of a recipe


def get_ingredients(soup):
    lists = soup.find_all('li', attrs = {'class': 'checkList__line'})
    array = []
    for li in lists:
        tag = li.find('span', attrs = {'itemprop': 'ingredients'})
        try:
            array.append(tag.contents[0].replace('�', ''))
        except AttributeError:
            break
    return array
# a method that returns the ingredients of a recipe


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
            create_recipe_test(8000, temp)
            print("It worked!")
            return temp
        except Exception:
            print("Didn't work")
    return ''
# This method scrapes a free proxy website that updates regularly to find a working proxy


def create_recipe_test(num, proxy):
    url = 'http://allrecipes.com/recipe/' + str(num)
    req = requests.get(url, proxies={'http': proxy},
                     headers={'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))})
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    tim = get_time(soup)
    name = get_name(soup)
    rating = get_rating(soup)
    ingredients = get_ingredients(soup)
    text = ''
    text += name+', '
    text += tim+', '
    text += rating+', '
    temp = ''
    for i in ingredients:
        temp+=i+' // '
    text += temp
    return text


def create_recipe(num, proxy, tfile):
    url = 'http://allrecipes.com/recipe/' + str(num)
    req = requests.get(url, proxies={'http': proxy},
                     headers={'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))})
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    tim = get_time(soup)
    name = get_name(soup)
    rating = get_rating(soup)
    ingredients = get_ingredients(soup)
    text = ''
    text += name+', '
    text += tim+', '
    text += rating+', '
    temp = ''
    for i in ingredients:
        temp+=i+' // '
    text += temp
    meal = get_meal(soup)
    tfile.write(meal)
    tfile.write('\n')
    return text
# a method to create a csv formatted text block for a recipe



recipes = []
temp = ''
proxy = ''
attempts = 0
while proxy == '':
    proxy = get_proxy()

print('Using proxy '+proxy)
with open('recipesNew.csv', 'a+') as txtfile:
    with open('meals.csv', 'a+') as tfile:
        i = 18000
        while i < 18027:
            try:
                temp = create_recipe(i, proxy,tfile)

                recipes.append(temp)
                txtfile.write(temp)
                txtfile.write('\n')
                print(str(i - 7999) + ' out of 11000')
                i = i+1
                attempts = 0
                # try to write out the recipe to CSV
            except Exception as e:
                print(e)
                proxy = ''
                while proxy == '':
                    proxy = get_proxy()
                print('Using proxy ' + proxy)
                if attempts == 1:
                    i = i+1
                else:
                    attempts = attempts + 1
                # if an exception is caught, assume that it must be from the proxy and find a new working proxy
        # populating an array of recipes
# writing the recipes to a csv file
