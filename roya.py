# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import re

import keras
from IPython.display import display

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os

#from keras.preprocessing import image
import keras.utils as image
import tensorflow as tf

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

#Load models
binrust = keras.models.load_model('./static/modelos/roya.h5')

#models usage
identifier = 511
img_width, img_height = 1024, 1024
def diagnosticar(ruta):
    trl = pd.read_csv('./static/modelos/test_classes.csv')
    ruta="."+ruta
    img = image.load_img(ruta, target_size = (img_width, img_height))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis = 0)
    ruta = re.sub('[.jpg]', '', ruta)
    ruta = re.sub('[a-z]', '', ruta)
    ruta = re.sub('[/]', '', ruta)
    for index,row in trl.iterrows():
        # print(ruta)
        cont="vacio"
        if row["id"] == int(ruta):
            cont=""
            # print('Truth')
            # print('rust') 
            # display( row['rust'])
            
            predictionr = binrust.predict(img)[0][0]
            predictionrs = 0 if predictionr < 0 else 1
            
            
            # print("Prediction", predictionrs)
            # print("Prediction", predictionr)

            if(predictionrs == row['rust'] ):
                cont=cont+'\033[1;30;32m CORRECT\n'
                cont=cont+'\033[0;30;30m --------------------------\n'
                return cont 
            else:
                cont=cont+'\033[1;30;31m WRONG\n'
                cont=cont+'\033[0;30;30m --------------------------\n'
                return cont 
            
            # predictionrs = 0 if predictionr < 0 else 1
            

            # print("Prediction", predictionrs)
            # print("Prediction", predictionr)

            # if(predictionrs == row['rust'] ):
            #     print('\033[1;30;32m CORRECT\n')
            #     print('\033[0;30;30m --------------------------\n')
            # else:
            #     print('\033[1;30;31m WRONG\n')
            #     print('\033[0;30;30m --------------------------\n')
            
                
            
# ruta="./uploads/1104.jpg"

# print(diagnosticar(ruta))