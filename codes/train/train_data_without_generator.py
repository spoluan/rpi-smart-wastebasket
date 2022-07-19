# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 12:36:30 2022

@author: SEVENDI ELDRIGE RIFKI POLUAN
"""
  
import numpy as np
import tensorflow as tf
import librosa
import pickle
from datasets  import Datasets
from pickledump import PickleDumpLoad
import warnings  
warnings.filterwarnings("ignore")
 
class DataWithoutGenerator(tf.keras.utils.Sequence): 
    
    def __init__(self):
        self.datasets = Datasets()
        self.PATH = "./datasets/train"
        self.TEST_PATH = "./datasets/test"
        self.load = PickleDumpLoad()
   
    def data_load(self, file_name='train.pickle'):
        print(f'Load {file_name}')
        return self.load.load_config(f'../datasets/saved_datasets/{file_name}')
     
    def save_datasets(self, x_paths, x_label, file_name='train.pickle'):
        
        x_train = []
        y_train = []
        for index, (path, label) in enumerate(zip(x_paths, x_label)):  
            
            print(f'Process {index + 1} from {len(x_paths)}')
            
            time_series_x, sampling_rate = librosa.load(path, sr=32000, mono=True)
    
            # Extract mfcc
            mfccs = librosa.feature.mfcc(time_series_x, sr=sampling_rate, n_mfcc=30)
     
            mfccs = np.array(mfccs).swapaxes(0, 1)
            mfccs = np.resize(mfccs, (50, 30))
            
            x_train.append(mfccs)
            y_train.append(label)
            
 
        self.load.save_config([np.array(x_train), np.array(y_train)], f'../datasets/saved_datasets/{file_name}')

    def main(self):
        
        # Get all the train data paths
        x_paths, x_label = self.datasets.get_data_paths(self.PATH) 
        
        # Get all the test data paths
        x_test_paths, x_test_label = self.datasets.get_data_paths(self.TEST_PATH)

        # Apply one hot encoder to the data labels
        x_label = self.datasets.one_hot_encoder(x_label=x_label) 
  
        # Apply one hot encoder to the data labels
        x_test_label = self.datasets.one_hot_encoder(x_label=x_test_label)
        
        self.save_datasets(x_paths, x_label, file_name='train.pickle')
        self.save_datasets(x_test_paths, x_test_label, file_name='test.pickle')
        
# app = DataWithoutGenerator()
# app.main()