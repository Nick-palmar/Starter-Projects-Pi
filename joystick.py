# import libraries
from ADCDevice import *
import time
import RPi.GPIO as GPIO


def setup():
    global adc, press_pin
    # define pushing mechanism
    press_pin = 21
    adc = PCF8591()

    GPIO.setmode(GPIO.BCM)
    # set press mechanism on joystick to pull-up mode
    GPIO.setup(press_pin, GPIO.IN, GPIO.PUD_UP)

def loop():
    press_dict = {0: True, 1: False}
    while True:
        # get the joystick x-y values
        pos_x = adc.analogRead(1)
        pos_y = adc.analogRead(0)

        # get 'pushed down' value
        pressed = press_dict[GPIO.input(press_pin)]
        print("X: {}, Y: {}, Pressed: {}".format(pos_x, pos_y, pressed))
        time.sleep(0.01)


def stop():
    adc.close()
    GPIO.cleanup()


if __name__ == "__main__":
    print("Starting joystick.py")
    setup()

    try:
        loop()
    except KeyboardInterrupt:
        stop()
        
