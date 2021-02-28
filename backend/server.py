# FLASK
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
# WEB SCRAPING
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import random
import time
# MACHINE LEARNING
import base64
import io
import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.densenet import preprocess_input, decode_predictions



# FLASK SERVER
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def preprocess_image(img, target_size):
  if img.mode != 'RGB':
    img = img.convert('RGB')
  img = img.resize(target_size)
  img = image.img_to_array(img)
  img = np.expand_dims(img, axis=0)
  return img

# WEB SCRAPING GLOBAL VARIABLES
PATH = "./chromedriver"
veg_fruit = ['apple', 'banana', 'beetroot', 'bell_pepper', 'cabbage', 'capsicum', 'carrot', 'cauliflower', 'chilli_pepper', 'corn', 'cucumber', 'eggplant', 'garlic', 'ginger', 'grapes', 'jalepeno', 'kiwi', 'lemon', 'lettuce', 'mango', 'onion', 'orange', 'paprika', 'pear', 'peas', 'pineapple', 'pomegranate', 'potato', 'raddish', 'soy_beans', 'spinach', 'sweetcorn', 'sweetpotato', 'tomato', 'turnip', 'watermelo']



@app.route('/form', methods=['POST'])
def form():
  message = request.get_json(force=True)
  flag = True
  while flag:
    if message['name'] in veg_fruit:
      if answer == "None":
        bbc_url = 'https://www.bbc.co.uk/food/' + message['name']
        flag = False
      else:
        bbc_url = 'https://www.bbc.co.uk/food/search?q='+message['name']+"+"+answer
    else:
      response = {
        'error': 'Please enter a food in our database'
      }
      return jsonify(response)

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
  except:
    image = False

  prep = soup2.find('div', class_="recipe-leading-info")
  prep = prep.find_all('div', class_="gel-pica")

  title = driver.find_element_by_class_name('gel-trafalgar').text

  ingredients = driver.find_element_by_class_name('recipe-ingredients-wrapper').text # gets the ingredients for the recipe
  method = driver.find_element_by_class_name('recipe-method-wrapper').text # gets the method or steps to make the recipe

  print(prep[0].text)
  print(prep[1].text)
  print(prep[2].text)
  print(image)
  print(title)
  print(ingredients)
  print(method)


  driver.close()

  response = {
    'prep1': prep[0].text,
    'prep2': prep[1].text,
    'prep3': prep[2].text,
    'image': image,
    'title': title,
    'ingredients': ingredients,
    'method': method
  }
  return jsonify(response)




  # driver.get(final_url1)
  # req = requests.get(final_url1).text
  # soup2 = BeautifulSoup(req, 'lxml')
  # try:
  #   img = soup2.find("div", {"class": "recipe-media"}).find("img")
  #   image = img['src']
  # except:
  #   response = {
  #     'error': 'No img in this website'
  #   }
  #   return jsonify(response)

  # prep = soup2.find('div', class_="recipe-leading-info")
  # prep = prep.find_all('div', class_="gel-pica")

  # title = driver.find_element_by_class_name('gel-trafalgar')

  # ingredients = driver.find_element_by_class_name('recipe-ingredients-wrapper') # gets the ingredients for the recipe
  # method = driver.find_element_by_class_name('recipe-method-wrapper') # gets the method or steps to make the recipe






  # driver.get(final_url2)
  # req = requests.get(final_url2).text
  # soup2 = BeautifulSoup(req, 'lxml')
  # try:
  #   img = soup2.find("div", {"class": "recipe-media"}).find("img")
  #   image = img['src']
  # except:
  #   response = {
  #     'error': 'No img in this website'
  #   }
  #   return jsonify(response)

  # prep = soup2.find('div', class_="recipe-leading-info")
  # prep = prep.find_all('div', class_="gel-pica")

  # title = driver.find_element_by_class_name('gel-trafalgar')

  # ingredients = driver.find_element_by_class_name('recipe-ingredients-wrapper') # gets the ingredients for the recipe
  # method = driver.find_element_by_class_name('recipe-method-wrapper') # gets the method or steps to make the recipe













# MACHINE LEARNING
@app.route('/predict', methods=['POST'])
def predict():
  message = request.get_json(force=True)
  decoded_image = base64.b64decode(message['image'])
  pil_img = Image.open(io.BytesIO(decoded_image))
  processed_image = preprocess_image(pil_img, target_size=(224, 224))

  interpreter = tf.lite.Interpreter(model_path="./model.tflite")
  interpreter.allocate_tensors()
  x = preprocess_input(processed_image)
  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()
  interpreter.set_tensor(input_details[0]['index'], x)
  interpreter.invoke()
  output_data = interpreter.get_tensor(output_details[0]['index'])
  label_array=['apple', 'banana', 'beetroot', 'bell pepper', 'cabbage', 'capsicum', 'carrot', 'cauliflower', 'chilli pepper', 'corn', 'cucumber', 'eggplant', 'garlic', 'ginger', 'grapes', 'jalepeno', 'kiwi', 'lemon', 'lettuce', 'mango', 'onion', 'orange', 'paprika', 'pear', 'peas', 'pineapple', 'pomegranate', 'potato', 'raddish', 'soy beans', 'spinach', 'sweetcorn', 'sweetpotato', 'tomato', 'turnip', 'watermelo']
  max=0
  label_loc=0
  for i in range (0,len(output_data[0])):
    if(output_data[0][i]>max):
      max=output_data[0][i]
      label_loc=i
  prediction = label_array[label_loc]
  response = {
    'prediction': prediction
  }
  return jsonify(response)

if __name__ == "__main__":
  app.run()
