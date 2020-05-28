# import libraries
import RPi.GPIO as GPIO
import time
from ADCDevice import *
from math import *

red_pin = 20
green_pin = 12
blue_pin = 26
press_pin = 21

def setup():
    global adc
    adc = PCF8591()

    # setup pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(red_pin, GPIO.OUT)
    GPIO.setup(green_pin, GPIO.OUT)
    GPIO.setup(blue_pin, GPIO.OUT)
    GPIO.setup(press_pin, GPIO.IN, GPIO.PUD_UP)

def loop():
    press_dict = {0: True, 1: False}
    while True:
        pressed = press_dict[GPIO.input(press_pin)]
        if pressed:
            # turn off all lights if pressed down
            turn_all_off([red_pin, blue_pin, green_pin])
        else:
            # get stick positions
            stick_x = adc.analogRead(1)
            stick_y = adc.analogRead(0)

            # get relative stick positions
            pos_x = stick_x - 128
            pos_y = 128 - stick_y

            relative_angle = atan2(pos_y, pos_x)
            if relative_angle < 0:
                relative_angle = 2*pi + relative_angle

            print(relative_angle)

            # get a different colour depending on location of the stick
            if relative_angle <= (pi/6) or relative_angle >= ((11*pi)/6):
                GPIO.output(red_pin, GPIO.HIGH)
                GPIO.output(blue_pin, GPIO.LOW)
                GPIO.output(green_pin, GPIO.LOW)
                print("red")
            elif relative_angle <= (pi/2):
                GPIO.output(blue_pin, GPIO.HIGH)
                GPIO.output(red_pin, GPIO.HIGH)
                GPIO.output(green_pin, GPIO.LOW)
                print("blue red/ magenta")
            elif relative_angle <= ((5*pi)/6):
                GPIO.output(blue_pin, GPIO.HIGH)
                GPIO.output(red_pin, GPIO.LOW)
                GPIO.output(green_pin, GPIO.LOW)
                print("blue")
            elif relative_angle <= ((7*pi)/6):
                GPIO.output(blue_pin, GPIO.HIGH)
                GPIO.output(green_pin, GPIO.HIGH)
                GPIO.output(red_pin, GPIO.LOW)
                print("blue, green/ light blue")
            elif relative_angle <= ((3*pi)/2):
                GPIO.output(green_pin, GPIO.HIGH)
                GPIO.output(blue_pin, GPIO.LOW)
                GPIO.output(red_pin, GPIO.LOW)
                print("green")
            elif relative_angle < ((11*pi)/6):
                GPIO.output(red_pin, GPIO.HIGH)
                GPIO.output(green_pin, GPIO.HIGH)
                GPIO.output(blue_pin, GPIO.LOW)
                print("red, green/ yellow")

            time.sleep(0.01)
                
        
        
        
def turn_all_off(pin_list):
    for pin in pin_list:
        GPIO.output(pin, GPIO.LOW)

    
def stop():
    GPIO.cleanup()
    adc.close()

if __name__ == "__main__":
    print("Starting joystick_light.py")
    setup()

    try:
        loop()
    except KeyboardInterrupt:
        stop()

        
