# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 10:03:37 2022

@author: SEVENDI ELDRIGE RIFKI POLUAN
"""
 
import tensorflow as tf  
from train_data_without_generator import DataWithoutGenerator 
import numpy as np
from tensorflow.keras.callbacks import ModelCheckpoint
import os

class ModelTrain(object):

    def __init__(self):  
        self.EPOCHS = 100000
        self.BATCH_SIZE = 32
        self.train_without_generator = DataWithoutGenerator()

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
    
    def train(self):
        
        # UNCOMMENT TO REGENERATE AND SAVE THE NEW DATASETS
        self.train_without_generator.main()
           
        x_train, y_train = self.train_without_generator.data_load(file_name='train.pickle')
        x_test, y_test = self.train_without_generator.data_load(file_name='test.pickle')
          
        # Prepare the model
        model = self.define_model(CLASSES=y_train.shape[1], INPUT_SHAPE=x_train.shape[1:])
        
        save = 'weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5'
        filepath = os.path.join("./model", save)
        checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
        callbacks_list = [checkpoint]
        
        # Train the model
        model.fit(
            x_train, y_train,
            epochs=self.EPOCHS,
            batch_size=self.BATCH_SIZE,
            validation_data=(x_test, y_test),
            callbacks=callbacks_list,
        )
  
if __name__ == '__main__':
    app = ModelTrain()
    app.train()
        
