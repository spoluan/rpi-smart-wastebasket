# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 09:58:17 2022

@author: SEVENDI ELDRIGE RIFKI POLUAN
"""

import numpy as np 
import tensorflow as tf
import os
from pickledump import PickleDumpLoad

class Datasets(object): 

    def __init__(self):
        self.pickledump = PickleDumpLoad()

    def get_data_paths(self, PATH):  
        x_label, x_path = [], []
        for label in sorted(os.listdir(PATH))[:10]:
            if '.txt' not in label:
                for path in os.listdir(os.path.join(PATH, label))[:50]:
                    x_path.append(os.path.join(PATH, label, path))
                    x_label.append(label)

        # Make a model for the label
        self.save_label_as_model(x_label)

        # Prepare the label for training
        x_label = [list(map(lambda x: int(x) - 1, x_label))]

        return x_path, x_label 

    def save_label_as_model(self, x_label):
        # Generate a model for the label 
        label_model = list(map(lambda x: dict({x[0]: x[1]}), enumerate(np.sort(np.unique(np.squeeze(x_label))))))
        label_model_as_dict = {}
 
        for x in label_model:
            label_model_as_dict[list(x.keys())[0]] = list(x.values())[0]

        # Save the label model
        self.pickledump.save_config(label_model_as_dict, 'label.mdl')

    def one_hot_encoder(self, x_label=[0, 1]):  
        cats = tf.keras.utils.to_categorical(np.sort(np.squeeze(x_label)))
        return cats

