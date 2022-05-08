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
        MODEL_SAVED_PATH = "./model/model.h5" 
        self.model = self.define_model(CLASSES=3, INPUT_SHAPE=[20, 3])  
        self.model.load_weights(MODEL_SAVED_PATH)   

        # Load the label model 
        pickledump = PickleDumpLoad()
        self.label_model = pickledump.load_config('label.mdl') 
        
    def define_model(self, CLASSES=2, INPUT_SHAPE=[20, 3]):
        input = tf.keras.layers.Input(shape=INPUT_SHAPE) 

        m = tf.keras.layers.Conv1D(32, 3, activation='relu')(input)
        m = tf.keras.layers.Conv1D(64, 3, activation='relu')(m)
        m = tf.keras.layers.MaxPooling1D()(m)
        m = tf.keras.layers.Dropout(0.25)(m)
        m = tf.keras.layers.Dense(128, activation='relu')(m)  
        m = tf.keras.layers.LSTM(128, return_sequences=True)(m)
        m = tf.keras.layers.LSTM(128, return_sequences=False)(m) 
        m = tf.keras.layers.Dense(256, activation='relu')(m) 
        m = tf.keras.layers.Flatten()(m)    
        m = tf.keras.layers.Dense(128, activation='relu', name='dense_128')(m) 
        m = tf.keras.layers.Dense(CLASSES, activation='sigmoid', name="predicting")(m) 
        
        model = tf.keras.Model(input, m)  

        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), 
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=['mse', 'accuracy'],
        )

        return model  
  
    def load_sound(self, path):

        time_series_x, sampling_rate = librosa.load(path, sr=32000, mono=True) 

        # Extract mfcc
        mfccs = librosa.feature.mfcc(time_series_x, sr=sampling_rate, n_mfcc=20) 

        # Extract melspectogram
        mel = librosa.feature.melspectrogram(y=time_series_x, sr=sampling_rate, n_mels=20,
                                    fmax=8000, win_length=1024, hop_length=320) 

        mfccs_scaled_features = np.mean(mfccs.T, axis=0)
        mel_s_scaled_features = np.mean(mel.T, axis=0)

        # Multiply the mfcc and melspectogram: for additional features
        multiply =  np.multiply(mel_s_scaled_features, mfccs_scaled_features)

        # mfccs = tf.convert_to_tensor([mfccs_scaled_features, multiply, mel_s_scaled_features])
        # mfccs = tf.reshape(mfccs, shape=[1, 20, 3])
        
        mfccs = np.array([mfccs_scaled_features, multiply, mel_s_scaled_features]).reshape((1, 20, 3))  

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
        
        test_paths = os.listdir(self.TEST_PATH)
        
        for x in test_paths: 
            path = os.path.join(self.TEST_PATH, x)
            
            # Make a prediction
            result = self.predict(path)

            # Print result
            print(f'{path} = {result}') 
  
if __name__ == '__main__':
    app = ModelTest()
    app.main()


