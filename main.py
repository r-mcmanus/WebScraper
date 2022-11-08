# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import re
import sys
import io

# finds the link in the all recipes page and saves it as url
# global variable for using to find relevant pages
char1 = '"width":'
char2 = '"ImageObject"'
char3 = '": "'
char4 = '",'
char5 = '"recipeIngredient":'
char6 = '"recipeInstructions":'
char7 = '"mainEntityOfPage": "'
char8 = '"name":'
char9 = '"image":'
char10 = '"url": "https://www.allrecipes.com/recipe/'
# list of urls to scrape recipes from
recipe_link_list = []
drink_link_list = []
alr_catr_links = [
    'https://www.allrecipes.com/recipes/200/meat-and-poultry/beef/',
    'https://www.allrecipes.com/recipes/201/meat-and-poultry/chicken/',
    'https://www.allrecipes.com/recipes/205/meat-and-poultry/pork/',
    'https://www.allrecipes.com/recipes/93/seafood/',
    'https://www.allrecipes.com/recipes/206/meat-and-poultry/turkey/',
    'https://www.allrecipes.com/recipes/225/side-dish/vegetables/',
    'https://www.allrecipes.com/recipes/76/appetizers-and-snacks/',
    'https://www.allrecipes.com/recipes/156/bread/',
    'https://www.allrecipes.com/recipes/78/breakfast-and-brunch/',
    'https://www.allrecipes.com/recipes/249/main-dish/casseroles/',
    'https://www.allrecipes.com/recipes/79/desserts/',
    'https://www.allrecipes.com/recipes/276/desserts/cakes/',
    'https://www.allrecipes.com/recipes/367/desserts/pies/',
    'https://www.allrecipes.com/recipes/362/desserts/cookies/',
    'https://www.allrecipes.com/recipes/17562/dinner/',
    'https://www.allrecipes.com/recipes/17561/lunch/',
    'https://www.allrecipes.com/recipes/80/main-dish/',
    'https://www.allrecipes.com/recipes/95/pasta-and-noodles/',
    'https://www.allrecipes.com/recipes/509/main-dish/pasta/macaroni-and-cheese/',
    'https://www.allrecipes.com/recipes/96/salad/',
    'https://www.allrecipes.com/recipes/215/salad/pasta-salad/',
    'https://www.allrecipes.com/recipes/17031/side-dish/sauces-and-condiments/',
    'https://www.allrecipes.com/recipes/81/side-dish/',
    'https://www.allrecipes.com/recipes/94/soups-stews-and-chili/',
]

alr_catd_links = [
    'https://www.allrecipes.com/recipes/77/drinks/',
    'https://www.allrecipes.com/recipes/133/drinks/cocktails/',
    'https://www.allrecipes.com/recipes/138/drinks/smoothies/'
]

for j in alr_catr_links:
    html_page0 = urllib.request.urlopen(j)
    soup0 = BeautifulSoup(html_page0, features="html.parser")
    json_url = str(soup0)
    json_url_list = json_url.split('\n')
    # use regex to find all recipe urls
    regex_pattern = re.compile(r'https:\/\/www\.allrecipes\.com\/recipe\/[a-zA-Z0-9-\'\/]*\/')
    for match in re.findall(regex_pattern, json_url):
        recipe_link_list.append(match)

# remove duplicates from the list
recipe_link_list = list(set(recipe_link_list))

for j in alr_catd_links:
    html_page0 = urllib.request.urlopen(j)
    soup0 = BeautifulSoup(html_page0, features="html.parser")
    json_url = str(soup0)
    json_url_list = json_url.split('\n')
    # use regex to find all recipe urls
    regex_pattern = re.compile(r'https:\/\/www\.allrecipes\.com\/recipe\/[a-zA-Z0-9-\'\/]*\/')
    for match in re.findall(regex_pattern, json_url):
        drink_link_list.append(match)

# remove duplicates from the list
drink_link_list = list(set(drink_link_list))

# scrape each recipe for the recipe name, url, image link, and ingredients


def scrape_url_soup():
    global url
    global soup
    url = soup.find('link', attrs={'href': re.compile("(^http://)|(^https://)"), 'rel': "canonical"})
    url = url.get('href')
    return url


def scrape_json_image():
    global json_text
    global char1
    global char2
    global char3
    global char4
    json_image = json_text[json_text.find(char2) + len(char2) + 1:json_text.find(char1)]
    json_image = json_image[json_image.find(char3) + len(char3):json_image.find(char4)]
    return json_image


def scrape_json_ingredients():
    global json_text
    global char5
    global char6
    json_ingredients = json_text[json_text.find(char5) + 1:json_text.find(char6)].strip()
    json_ingredients = json_ingredients[json_ingredients.find('[') + 1:json_ingredients.find(']')].strip()
    json_ingredients_list = json_ingredients.split('\n          ')
    json_ingredients_list = [x.rstrip('",') for x in json_ingredients_list]
    json_ingredients_list = [x.lstrip('"') for x in json_ingredients_list]
    return json_ingredients_list


def scrape_json_name():
    global json_text
    global char7
    global char1
    global char8
    global char9
    global char4
    json_name = json_text[json_text.find(char7)+len(char7)+1:json_text.find(char1)].strip()
    json_name = json_name[json_name.find(char8)+len(char8):json_name.find(char9)].strip()
    json_name = json_name.rstrip(char4)
    json_name = json_name.lstrip('"')
    return json_name


def evaluate(x):
    print(x)


ingredients_list = []

for i in recipe_link_list:
    html_page = urllib.request.urlopen(urllib.request.Request(i, headers={'User Agent': 'Edg/86.0.622.63'}))
    soup = BeautifulSoup(html_page, features="html.parser")
    url = scrape_url_soup()
    # finds the stuff in the json section
    # grab the json section and store in text for slicing out data
    json_text = soup.find('script', attrs={'type': 'application/ld+json'})
    json_text = str(json_text)
    json_text = json_text.rstrip('<script type="application/ld+json">')
    json_text = json_text.lstrip('</script>')
    image = scrape_json_image()
    ingredients_list = scrape_json_ingredients()
    # Remove special characters that do not have a UTF-8 representation
    ingredients_list = [x.replace('®', '') for x in ingredients_list]
    ingredients_list = [x.replace('½', '1/2')for x in ingredients_list]
    ingredients_list = [x.replace('⅓', '1/3') for x in ingredients_list]
    ingredients_list = [x.replace('¼', '1/4') for x in ingredients_list]
    ingredients_list = [x.replace('⅛', '1/8') for x in ingredients_list]
    ingredients_list = [x.replace('⅔', '2/3') for x in ingredients_list]
    ingredients_list = [x.replace('¾', '3/4') for x in ingredients_list]
    ingredients_list = [x.replace('\u2009', ' ') for x in ingredients_list]
    name = scrape_json_name()
    name = name.replace('®', '')
    print(url)
    print(name)
    print(image)
    print(ingredients_list)
    # saves the html source code of the url in a text file by redirecting the standard output
    # You must change the filepath in the open method to a filepath of your own choosing
    # I created a folder called ALR's in the same folder as the code and used a relative url
    original_stdout = sys.stdout
    with io.open("C:\\Users\\mcman\\OneDrive\\Desktop\\ALR's\\Recipes.txt", 'a+', encoding="utf-8") as f:
        sys.stdout = f
        print('False')
        print(str(url))
        print(str(name))
        print(str(image))
        print(ingredients_list)
        print()
        sys.stdout = original_stdout
f.close()
for i in drink_link_list:
    html_page = urllib.request.urlopen(urllib.request.Request(i, headers={'User Agent': 'Edg/86.0.622.63'}))
    soup = BeautifulSoup(html_page, features="html.parser")
    url = scrape_url_soup()
    # finds the stuff in the json section
    # grab the json section and store in text for slicing out data
    json_text = soup.find('script', attrs={'type': 'application/ld+json'})
    json_text = str(json_text)
    json_text = json_text.rstrip('<script type="application/ld+json">')
    json_text = json_text.lstrip('</script>')
    image = scrape_json_image()
    ingredients_list = scrape_json_ingredients()
    # Remove special characters that do not have a UTF-8 representation
    ingredients_list = [x.replace('®', '') for x in ingredients_list]
    ingredients_list = [x.replace('½', '1/2') for x in ingredients_list]
    ingredients_list = [x.replace('⅓', '1/3') for x in ingredients_list]
    ingredients_list = [x.replace('¼', '1/4') for x in ingredients_list]
    ingredients_list = [x.replace('⅛', '1/8') for x in ingredients_list]
    ingredients_list = [x.replace('⅔', '2/3') for x in ingredients_list]
    ingredients_list = [x.replace('¾', '3/4') for x in ingredients_list]
    ingredients_list = [x.replace('\u2009', ' ') for x in ingredients_list]
    name = scrape_json_name()
    name = name.replace('®', '')
    print(url)
    print(name)
    print(image)
    print(ingredients_list)
    # saves the html source code of the url in a text file by redirecting the standard output
    # You must change the filepath in the open method to a filepath of your own choosing
    # I created a folder called ALR's in the same folder as the code and used a relative url
    original_stdout = sys.stdout
    with io.open("C:\\Users\\mcman\\OneDrive\\Desktop\\ALR's\\Recipes.txt", 'a+', encoding="utf-8") as f:
        sys.stdout = f
        print('True')
        print(str(url))
        print(str(name))
        print(str(image))
        print(ingredients_list)
        print()
        sys.stdout = original_stdout
    f.close()

