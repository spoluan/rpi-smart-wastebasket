# -*- coding: utf-8 -*-
"""
Created on Mon May  9 00:08:23 2022

@author: SEVENDI ELDRIGE RIFKI POLUAN   
"""
 
from warnings import simplefilter 
from codes.sensor.soundrecorder import AudioRecording
from codes.sensor.ultrasound import Ultrasound 
import time
import os
simplefilter(action='ignore', category=FutureWarning) 

class App(object):

    def __init__(self):

        # Initialize ultrasond pin 23
        self.ultrasound_one = Ultrasound(trigger_pin=23, echo_pin=24) 
        self.ultrasound_one.start()
        
        # Initialize ultrasond pin 23
        # self.ultrasound_two = Ultrasound(trigger_pin=23, echo_pin=24)
        # self.ultrasound_two.start() 
        
        # Initialize the sound recorder 
        self.soundrecorder = AudioRecording()
        self.soundrecorder.start()

        # Set class collection 
        self.class_name = '' 
        self.status = 'train' # train | test

    def main(self):
         
        input('Enter to continue ...') 

        while True: 

            # Maintain the ultrasound sensor
            distance_cm_one, distance_in_one = self.ultrasound_one.get_dis() # > 40 | 50 cm default
            # distance_cm_two, distance_in_two = self.ultrasound_two.get_dis() # > 40 | 50 cm default
            
            if distance_cm_one < 40: # or distance_cm_two < 40:
            
                print('There is a trash!')
                print('Ultrasound one', distance_cm_one, 'cm')
                
                # Recording 
                frames = self.soundrecorder.record()
                file_name = len(os.listdir(f'./datasets/{self.status}/{self.class_name}/'))
                self.soundrecorder.OUTPUT = f'./datasets/{self.status}/{self.class_name}/{file_name}.wav'
                self.soundrecorder.save(frames) 
                
                time.sleep(1) 
                
            # print('Ultrasound one', distance_cm_one, 'cm', distance_in_one, 'inch')
            # print('Ultrasound two', distance_cm_two, 'cm', distance_in_two, 'inch')
            
            # time.sleep(0.1)
          
if __name__ == '__main__':
    app = App()
    app.main()
