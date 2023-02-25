import pytest
import requests
import base64
import json
import numpy as np
from tensorflow import keras
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Dropout
from tensorflow.keras.models import Sequential
import keras 
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tqdm
import cv2

batch_size=32
ImageDataGenerator(rescale=1/255)
test_generator = ImageDataGenerator(rescale=1/255, validation_split=0.2)  
validation_dataset = test_generator.flow_from_directory(batch_size=32,
                                                 directory='FRUIT-16K-1',
                                                 shuffle=True,
                                                 target_size=(224, 224), 
                                                 subset="validation",
                                                 class_mode='categorical')
validation_dataset.reset()
X_test, y_test = next(validation_dataset)
for i in tqdm.tqdm(range(int(len(validation_dataset)/batch_size)-1)): 
  img, label = next(validation_dataset)
  X_test = np.append(X_test, img, axis=0 )
  y_test = np.append(y_test, label, axis=0)
print(X_test.shape, y_test.shape)

# X_test_gray_copy = X_test[0].copy()
# #print("X_test_grey image data shape =", X_test_gray_copy.shape)
# X_test_gray = cv2.cvtColor(X_test_gray_copy, cv2.COLOR_BGR2GRAY)
# #print("X_test_grey image data shape =", X_test_gray.shape)
# x_test1 = X_test_gray.reshape((X_test_gray.shape[0], X_test_gray.shape[1], 1))
# x_test1 = x_test1.astype('float32') / 255.0

# print("X_train image data shape =", X_test.shape)
# print("X_train_grey image data shape =", X_test_gray.shape)



url = 'http://ca2-2b02-jumanatushita-tf.herokuapp.com/v1/models/img_classifier:predict'
def make_prediction(instances):
  data = json.dumps({"signature_name": "serving_default",
                     "instances": instances.tolist()})
  headers = {"content-type": "application/json"}
  json_response = requests.post(url, data=data, headers=headers)
  predictions = json.loads(json_response.text)['predictions']
  return predictions
    
def test_prediction():
  predictions = make_prediction(X_test[0:4])
  for i, pred in enumerate(predictions):
    return y_test[i] == np.argmax(pred)
      