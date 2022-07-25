#!/usr/bin/python3
import RPi.GPIO as GPIO
import pigpio
import time


def rotate(type):
    servo = [21,20,16]
    pulse = 1500
    pwm = pigpio.pi()
    for each in servo:
        pwm.set_mode(each, pigpio.OUTPUT)
        pwm.set_PWM_frequency(each, 50)

    if type == 0:
        for pulse in range(1650, 800, -50):
            pwm.set_servo_pulsewidth(servo[0], pulse)
        time.sleep(2)
        for pulse in range(1600, 500, -50):
            pwm.set_servo_pulsewidth(servo[1], pulse)
        time.sleep(1)
        for pulse in range(800, 1700, 50):
            pwm.set_servo_pulsewidth(servo[0], pulse)
            #time.sleep(0.2)
        for pulse in range(500, 1650, 50):
            pwm.set_servo_pulsewidth(servo[1], pulse)
            #time.sleep(0.2)
    elif type == 1:
        for pulse in range(1650, 800, -50):
            pwm.set_servo_pulsewidth(servo[0], pulse)
        time.sleep(2)
        for pulse in range(1600, 2500, 50):
            pwm.set_servo_pulsewidth(servo[1], pulse)
        time.sleep(1)
        for pulse in range(800, 1700, 50):
            pwm.set_servo_pulsewidth(servo[0], pulse)
            #time.sleep(0.1)
        for pulse in range(2500, 1550, -50):
            pwm.set_servo_pulsewidth(servo[1], pulse)
            #time.sleep(0.1)
    elif type == 2:
        for pulse in range(1650, 2400, 50):
            pwm.set_servo_pulsewidth(servo[0], pulse)
        time.sleep(2)
        for pulse in range(1550, 500, -50):
            pwm.set_servo_pulsewidth(servo[2], pulse)
        time.sleep(1)
        for pulse in range(2400, 1600, -50):
            pwm.set_servo_pulsewidth(servo[0], pulse)
            #time.sleep(0.1)
        for pulse in range(500, 1600, 50):
            pwm.set_servo_pulsewidth(servo[2], pulse)
            #time.sleep(0.1)
    elif type == 3:
        for pulse in range(1650, 2400, 50):
            pwm.set_servo_pulsewidth(servo[0], pulse)
        time.sleep(2)
        for pulse in range(1550, 2400, 50):
            pwm.set_servo_pulsewidth(servo[2], pulse)
        time.sleep(1)
        for pulse in range(2400, 1600, -50):
            pwm.set_servo_pulsewidth(servo[0], pulse)
            #time.sleep(0.1)
        for pulse in range(2400, 1500, -50):
            pwm.set_servo_pulsewidth(servo[2], pulse)
            #time.sleep(0.1)
            
'''rotate(0)
time.sleep(5)
rotate(1)
time.sleep(5)
rotate(2)
time.sleep(5)
rotate(3)
time.sleep(5)'''
