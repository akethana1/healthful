# FLASK
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
# WEB SCRAPING
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import random
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



# WEB SCRAPING
PATH = "./chromedriver"
veg_fruit = ['cucumber', 'carrot', 'capsicum', 'onion', 'potato', 'tomato', 'beetroot', 'cabbage', 'lettuce', 'spinach', 'cauliflower', 'turnip', 'corn', 'sweetcorn', 'sweet_potato', 'paprika', 'ginger', 'garlic', 'pea', 'banana', 'apple', 'pear', 'grapes', 'orange', 'kiwi', 'watermelon', 'pomegranate', 'pineapple', 'mango']

@app.route('/form', methods=['POST'])
def form():
  message = request.get_json(force=True)
  flag = True
  while flag:
    if message['name'] in veg_fruit:
      bbc_url = 'https://www.bbc.co.uk/food/' + message['name']
      flag = False
    else:
      response = {
        'error': 'Please enter a food in our database'
      }
      return jsonify(response)

  driver = webdriver.Chrome(PATH)
  req = requests.get(bbc_url).text
  soup = BeautifulSoup(req, 'lxml')

  url_list = []
  food = soup.find_all('a', class_="promo")
  for urls in food:
    if '/food/recipes/' in urls['href']:
      url_list.append('https://www.bbc.co.uk' + urls['href'])

  final_url = url_list[random.randint(0, len(url_list))]
  driver.get(final_url)

  div = driver.find_element_by_class_name('recipe-ingredients-wrapper')
  ingredients = div.text
  div2 = driver.find_element_by_class_name('recipe-method-wrapper')
  method = div2.text

  response = {
    'urls': url_list,
    'ingredients': ingredients,
    'method': method
  }
  return jsonify(response)



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