# -*- coding: utf-8 -*-
"""
Created on Sun May  8 18:56:39 2022

@author: SEVENDI ELDRIGE RIFKI POLUAN
"""

import RPi.GPIO as GPIO
import time
import threading 

class Ultrasound(object):

    def __init__(self, trigger_pin=23, echo_pin=24): 
     
        self.distance = 0   
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.distance_cm, self.distance_in = -1, -1
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN) 
        
     
    def send_trigger_pulse(self): 
    
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.001)
        GPIO.output(self.trigger_pin, False)
    
    def wait_for_echo(self, value, timeout):
    
        count = timeout
        while GPIO.input(self.echo_pin) != value and count > 0:
            count = count - 1
    
    def get_distance(self):
    
        self.send_trigger_pulse()
        self.wait_for_echo(True, 5000)
        start = time.time()
        
        self.wait_for_echo(False, 5000)
        finish = time.time()
        
        pulse_len = finish - start
        distance_cm = pulse_len * 340 * 100 / 2
        distance_in = distance_cm / 2.5
        
        return distance_cm, distance_in
        
    def get_dis(self):
        return self.distance_cm, self.distance_in
      
    def start(self): 
        t = threading.Thread(target=self.run)
        t.start() 
        
    def run(self):
        print(f'Starting ultrasound pin {self.trigger_pin} ...')
        self.stop = False
        
        while not self.stop:
            self.distance_cm, self.distance_in = self.get_distance()
            # print("cm=%f\tinches=%f" % self.get_distance()) 
            time.sleep(0)
             
            
        print(f'Stop ultrasound pin {self.trigger_pin}!')
       
if __name__ == '__main__':
    app = Ultrasound()
    app.start()