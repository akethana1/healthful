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


import time
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired


class FieldsRequiredForm(FlaskForm):
    """Require all fields to have content. This works around the bug that WTForms radio
    fields don't honor the `DataRequired` or `InputRequired` validators.
    """

    class Meta:
        def render_field(self, field, render_kw):
            render_kw.setdefault('required', True)
            return super().render_field(field, render_kw)


class Restrictions(FieldsRequiredForm):
    q1 = RadioField('Do you have any dietary restrictions', choices=[("Vegan", "Vegan"), ("Vegetarian", "Vegetarian"),("None", "None")])
    submit = SubmitField('Check you Answers')

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

@app.route('/poll', methods=['POST','GET'])
def poll():
    global form
    form = Restrictions()
    if form.validate_on_submit():
        return redirect(url_for('form'))
    return render_template('poll.html', form=form)



@app.route('/results', methods=['POST','GET'])
def results():
    global answer
    answer = request.form['q1']
    return render_template('results.html', answer=answer)

@app.route('/')
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
                bbc_url = 'https://www.bbc.co.uk/food/search?q='+message['name']+answer
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

  div = driver.find_element_by_class_name('recipe-ingredients-wrapper') # gets the ingredients for the recipe
  print(div.text)
  div2 = driver.find_element_by_class_name('recipe-method-wrapper') # gets the method or steps to make the recipe
  print('\n')
  print(div2.text)

  time.sleep(5)
  driver.close()

  response = {
    'title' = title,
    'image' = image,
    'prep' = prep,
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
