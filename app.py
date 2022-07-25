# -*- coding: utf-8 -*-
"""
Created on Thu May 21 20:47:53 2020

@author: SEVENDI ELDRIGE RIFKI POLUAN; ERICK HUANG;
"""

import socket
import pickle
from keras.models import load_model
import rpi_send
import random
import pyaudio,wave
import time 
import librosa
import numpy as np
from keras.models import load_model
import os
import threading
from codes.sensor.soundrecorder import AudioRecording
from codes.sensor.ultrasound import Ultrasound 
from codes.test.test import ModelTest
import time
import codes.sensor.servotest

HOST = '192.168.1.100'
PORT = 50
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect((HOST, PORT))

class App(object):
    
    def __init__(self):
        # Initialize ultrasond pin 23
        self.ultrasound_one = Ultrasound(trigger_pin=26, echo_pin=19) 
        self.ultrasound_one.start()
        
        # Initialize ultrasond pin 23
        self.ultrasound_two = Ultrasound(trigger_pin=6, echo_pin=13)
        self.ultrasound_two.start()
    
        # Initialize the model 
        self.test = ModelTest()  
        
        # Initialize the sound recorder 
        self.soundrecorder = AudioRecording()
        self.soundrecorder.start()
        
        self.percentage = 100
        self.foil_pack = 100
        self.paper = 100
        self.can = 100
        self.bottle = 100
        rpi_send.senddata(self.percentage,self.paper,self.bottle,self.can,self.foil_pack)
        
    def percentage_reduce(self):
        while True:
            self.percentage -= random.randint(1,3)
            rpi_send.senddata(self.percentage, self.paper, self.bottle, self.can, self.foil_pack)
            print('percentage thread is start')
            time.sleep(50)
        
    def main(self):
         
        input('Enter to continue ...')
        t = threading.Thread(target = self.percentage_reduce)
        t.start()
        
        while True: 
            print('waitting for a trash....')
            # Maintain the ultrasound sensor
            distance_cm_one, distance_in_one = self.ultrasound_one.get_dis() # > 50 cm default
            distance_cm_two, distance_in_two = self.ultrasound_two.get_dis() # > 50 cm default
            
            if distance_cm_one < 40 or distance_cm_two < 40:
                #servotest.rotate(0)
            
                print('There is a trash!!!!!!!!!')

                # print('Ultrasound one', distance_cm_one, 'cm', distance_in_one, 'inch')
                
                # Recording 
 
                # Make a prediction 
                sound_path = './datasets/dev-test/recorded_file.wav' 
                pred = self.test.predict(sound_path) 
                print(f'Predicted result ({sound_path}):', pred)      
                         
                str_id_x = str(int(pred))
                print('result:',pred)
                # print('datatype:',type(str_id_x), 'typeresult:', str_id_x)
                client.send(str_id_x.encode())

                if str_id_x == '3':
                    print('result:','foilpack')
                    servotest.rotate(1)
                    foilpack -= random.randint(10,15)
                    rpi_send.senddata(self.percentage, self.paper, self.bottle,self.can, self.foil_pack)
                    
                elif str_id_x == '2':
                    print('result:','can')
                    servotest.rotate(2)
                    can -= random.randint(10,15)
                    rpi_send.senddata(self.percentage, self.paper, self.bottle, self.can, self.foil_pack)
                
                elif str_id_x == '1':
                    print('result:', 'bottle')
                    servotest.rotate(0)
                    can -= random.randint(15,25)
                    rpi_send.senddata(self.percentage, self.paper, self.bottle, self.can, self.foil_pack)
                     
                elif str_id_x == '4':
                    print('result:','paper')
                    servotest.rotate(3)
                    paper -= random.randint(10,15)
                    rpi_send.senddata(self.percentage, self.paper, self.bottle, self.can, self.foil_pack)               
                    
                time.sleep(1)
                
            ''' print('Ultrasound one', distance_cm_one, 'cm', distance_in_one, 'inch')
            print('Ultrasound two', distance_cm_two, 'cm', distance_in_two, 'inch') '''
            
            time.sleep(0.1)
 
         
if __name__ == '__main__':
    app = App()
    app.main()