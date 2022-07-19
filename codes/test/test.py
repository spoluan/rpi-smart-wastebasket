# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 20:48:49 2022

@author: SEVENDI ELDRIGE RIFKI POLUAN
"""

import librosa 
import numpy as np
import tensorflow as tf
from pickledump import PickleDumpLoad
import os 
from warnings import simplefilter  
simplefilter(action='ignore', category=FutureWarning)

class ModelTest(object):

    def __init__(self):
        # Test path
        self.TEST_PATH = './datasets/test'

        # Load the saved model
        print('Load the model...')
        MODEL_SAVED_PATH = "./model/weights-improvement-60-0.0184-bigger.hdf5" 
        self.model = self.define_model(CLASSES=4, INPUT_SHAPE=[50, 30])  
        self.model.load_weights(MODEL_SAVED_PATH)   

        # Load the label model 
        pickledump = PickleDumpLoad()
        self.label_model = pickledump.load_config('label.mdl') 
        
    def define_model(self, CLASSES=2, INPUT_SHAPE=[20, 3]):
        
        input = tf.keras.layers.Input(shape=INPUT_SHAPE) 
        m = tf.keras.layers.Conv1D(64, 3, activation='relu')(input)
        m = tf.keras.layers.Conv1D(32, 3, activation='relu')(m) 
        m = tf.keras.layers.MaxPooling1D()(m)    
        m = tf.keras.layers.Conv1D(64, 3, activation='relu')(m)
        m = tf.keras.layers.Conv1D(32, 3, activation='relu')(m) 
        m = tf.keras.layers.MaxPooling1D()(m) 
        m = tf.keras.layers.LSTM(128, return_sequences=True)(m)  
        m = tf.keras.layers.LSTM(128, return_sequences=False)(m)  
        m = tf.keras.layers.Dense(128, activation='relu')(m)   
        m = tf.keras.layers.Dropout(0.25)(m)
        m = tf.keras.layers.Flatten()(m)  
        m = tf.keras.layers.BatchNormalization()(m)
        m = tf.keras.layers.Dense(128, activation='relu', name='dense_1')(m)   
        m = tf.keras.layers.Dense(CLASSES, activation='softmax', name="predicting")(m)  
        model = tf.keras.Model(input, m)  
        model.summary() 
        # tf.keras.utils.plot_model(model) 

        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001), 
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=['mse', 'accuracy'],
        )

        return model  
  
    def load_sound(self, path):

        time_series_x, sampling_rate = librosa.load(path, sr=32000, mono=True)
    
        # Extract mfcc
        mfccs = librosa.feature.mfcc(time_series_x, sr=sampling_rate, n_mfcc=30)
 
        mfccs = np.array(mfccs).swapaxes(0, 1)
        mfccs = np.resize(mfccs, (1, 50, 30))

        return mfccs

    def check_prediction(self, pred):
        # Get the based label
        label_model = self.label_model

        # Get the prediction 
        predicted = np.argmax(np.squeeze(np.array(pred)), axis=0) 

        # Decode the label
        result = None
        try:
            result = label_model[predicted]
        except:
            pass 
 
        return result

    def predict(self, path): 
      
        # Load sound 
        print('Load sound ...')
        x_test = self.load_sound(path)   

        # Make a prediction 
        pred = self.model.predict(x_test)  

        # Check the prediction  
        print('Predicting ...') 
        result = self.check_prediction(pred)

        return result

    def main(self):
          
        results = []
        for root, dirs, files in os.walk(self.TEST_PATH):
            
           for name in files:  
               
                path = os.path.join(root, name)
                
                # Make a prediction
                result = self.predict(path)
                  
                if int(result) == int(root.split("\\")[-1]): 
                    results.append(1)
                else:
                    results.append(0)
    
                # Print result
                print(f'{path} = {result}')  
                
        print('Accuracy', sum(results) / len(results))
  
if __name__ == '__main__':
    app = ModelTest()
    app.main()


