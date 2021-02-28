from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import random
import time

message = {
  'name': 'apple'
}

PATH = "./chromedriver"
veg_fruit = ['apple', 'banana', 'beetroot', 'bell_pepper', 'cabbage', 'capsicum', 'carrot', 'cauliflower', 'chilli_pepper', 'corn', 'cucumber', 'eggplant', 'garlic', 'ginger', 'grapes', 'jalepeno', 'kiwi', 'lemon', 'lettuce', 'mango', 'onion', 'orange', 'paprika', 'pear', 'peas', 'pineapple', 'pomegranate', 'potato', 'raddish', 'soy_beans', 'spinach', 'sweetcorn', 'sweetpotato', 'tomato', 'turnip', 'watermelo']
answer = 'None'

flag = True
while flag:
  if message['name'] in veg_fruit:
    if answer == "None":
      bbc_url = 'https://www.bbc.co.uk/food/' + message['name']
      flag = False
    else:
      bbc_url = 'https://www.bbc.co.uk/food/search?q='+message['name']+answer
  else:
    response = {
      'error': 'Please enter a food in our database'
    }
    print(jsonify(response))

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(PATH, options=options)
req = requests.get(bbc_url).text
soup = BeautifulSoup(req, 'lxml')

url_list = []
food = soup.find_all('a', class_="promo")
for urls in food:
  if '/food/recipes/' in urls['href']:
    url_list.append('https://www.bbc.co.uk' + urls['href'])

# randomizes the recipe that will be picked for that certain ingredient
final_url = url_list[random.randint(0, len(url_list)-1)]
url_list.remove(final_url)
final_url1 = url_list[random.randint(0, len(url_list)-1)]
url_list.remove(final_url1)
final_url2 = url_list[random.randint(0, len(url_list)-1)]
url_list.remove(final_url2)
driver.get(final_url)  # open up the recipe's url for parsing and getting html data


req = requests.get(final_url).text
soup2 = BeautifulSoup(req, 'lxml')
try:
    img = soup2.find("div", {"class": "recipe-media"}).find("img")
    image = img['src']
    print(image + '\n')
except:
    print('There is no image \n')

prep = soup2.find('div', class_="recipe-leading-info")
prep = prep.find_all('div', class_="gel-pica")
print(prep[0].text)
print(prep[1].text)
print(prep[2].text)

title = driver.find_element_by_class_name('gel-trafalgar')
print('Title:' + title.text +'\n')

div = driver.find_element_by_class_name('recipe-ingredients-wrapper') # gets the ingredients for the recipe
print(div.text)
div2 = driver.find_element_by_class_name('recipe-method-wrapper') # gets the method or steps to make the recipe
print('\n')
print(div2.text)
print('------------------------------------------------------------------------------------------\n')


driver.get(final_url1)
req = requests.get(final_url1).text
soup2 = BeautifulSoup(req, 'lxml')
try:
  img = soup2.find("div", {"class": "recipe-media"}).find("img")
  image = img['src']
  print(image + '\n')
except:
  print('There is no image \n')

prep = soup2.find('div', class_="recipe-leading-info")
prep = prep.find_all('div', class_="gel-pica")
print(prep[0].text)
print(prep[1].text)
print(prep[2].text)

title = driver.find_element_by_class_name('gel-trafalgar')
print('Title:' + title.text +'\n')

div = driver.find_element_by_class_name('recipe-ingredients-wrapper') # gets the ingredients for the recipe
print(div.text)
div2 = driver.find_element_by_class_name('recipe-method-wrapper') # gets the method or steps to make the recipe
print('\n')
print(div2.text)
print('------------------------------------------------------------------------------------------\n')

driver.get(final_url2)
req = requests.get(final_url2).text
soup2 = BeautifulSoup(req, 'lxml')
try:
  img = soup2.find("div", {"class": "recipe-media"}).find("img")
  image = img['src']
  print(image + '\n')
except:
  print('There is no image \n')

prep = soup2.find('div', class_="recipe-leading-info")
prep = prep.find_all('div', class_="gel-pica")
print(prep[0].text)
print(prep[1].text)
print(prep[2].text)

title = driver.find_element_by_class_name('gel-trafalgar')
print('Title:' + title.text +'\n')

ingredients = driver.find_element_by_class_name('recipe-ingredients-wrapper') # gets the ingredients for the recipe
print(ingredients.text)
method = driver.find_element_by_class_name('recipe-method-wrapper') # gets the method or steps to make the recipe
print('\n')
print(method.text)

driver.close()

response = {
  'title': title,
  'image': image,
  'prep': prep,
  'urls': url_list,
  'ingredients': ingredients,
  'method': method
}
print(response)