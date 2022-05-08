# -*- coding: utf-8 -*-
"""
Created on Sun May  8 16:47:55 2022

@author: SEVENDI ELDRIGE RIFKI POLUAN
"""

import pyaudio
import wave

class AudioRecording(object):

    def __init__(self):
       
        self.audio = pyaudio.PyAudio() 
        self.RESOLUTION = pyaudio.paInt16 
        self.CHANNEL = 1
        self.RATE = 44100 
        self.CHUNK = 4096 
        self.DURATION = 2 # In seconds
        self.DEVICE_INDEX = self.get_dev_index() 
        self.OUTPUT = './datasets/dev-test/recorded_file.wav'
         
         
    def start(self): 
        self.stream = self.audio.open(format=self.RESOLUTION,
                            rate=self.RATE,
                            channels=self.CHANNEL, 
                            input_device_index=self.DEVICE_INDEX,
                            input=True, 
                            frames_per_buffer=self.CHUNK)
                                      
    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        
    def get_dev_index(self):
        index = -1
        mic_name = 'WordForum USB: Audio'
        for i in range(self.audio.get_device_count()): 
            print(self.audio.get_device_info_by_index(i).get('name'))
            if mic_name in self.audio.get_device_info_by_index(i).get('name'):
                index = i
                break
        print('Found:', index) 
        return index
 
    def record(self):                
        print(f"Recording for {self.DURATION} second(s) ... ")
        frames = []
         
        for ii in range(0, int((self.RATE / self.CHUNK) * self.DURATION)):
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            frames.append(data) 
            
        print("Finish recording!")  
        return frames
         
    def save(self, frames):
        wavefile = wave.open(self.OUTPUT, 'wb')
        wavefile.setnchannels(self.CHANNEL)
        wavefile.setsampwidth(self.audio.get_sample_size(self.RESOLUTION))
        wavefile.setframerate(self.RATE)
        wavefile.writeframes(b'' . join(frames))
        wavefile.close()   

    def app(self):
        self.start()
        
        for x in range(1):
            print('RECORDING at', x)
            frames = self.record()
            self.OUTPUT = f'./datasets/test/recorded_file{x}.wav'
            self.save(frames)
            
        self.stop()
        
if __name__ == '__main__':
    app = AudioRecording()
    app.app()
        
   
 