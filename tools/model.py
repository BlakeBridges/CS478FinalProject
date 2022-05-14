from flask import Flask, jsonify, request
from datetime import datetime
import pandas as pd
import tensorflow as tf
import keras
import numpy as np
from keras.preprocessing import image
from keras.models import load_model
#file location of model, change name later
MODEL_PATH = "./static/models/rps.h5"

# takes the path from the path passed in and
# then loads the image into the array below
# then we must check what it predicted and return it
def imagePredicition(path):
    model = load_model(MODEL_PATH)
    img = image.load_img(path, target_size=(150, 150))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    predition = model.predict(images)
    #change this later when the model gets installed
    if(predition[0][1] == 1.0):
        preditionText = "Rock"
    elif(predition[0][0] == 1.0):
        preditionText = "Paper"
    else:
        preditionText = "Scissors"
    return preditionText
