
# import libraries
import RPi.GPIO as GPIO
import time
from ADCDevice import *

# define pins connected to L293D (motor input device)
motor_p1 = 22
motor_p2 = 5
motor_enable = 27
# define joystick 'press' pin
press_pin = 21

def setup():
    global adc, pwm

    # adc deivce connected to joystick
    adc = PCF8591()

    GPIO.setmode(GPIO.BCM)

    # setup pins
    GPIO.setup(motor_p1, GPIO.OUT)
    GPIO.setup(motor_p2, GPIO.OUT)
    GPIO.setup(motor_enable, GPIO.OUT)
    GPIO.setup(press_pin, GPIO.IN, GPIO.PUD_UP)
    
    # define PWD
    pwm = GPIO.PWD(motor_enable, 1000)
    pwm.start(0)


def stop():
    GPIO.cleanup()
    adc.close()
    pwm.stop()
    
    
