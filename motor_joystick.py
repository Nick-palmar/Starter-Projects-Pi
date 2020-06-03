
# impot libraries
import RPi.GPIO as GPIO
import time
from ADCDevice import *

# define pins connected to L293D (motor input device)
motor_p1 = 22
motor_p2 = 5
motor_enable = 27
# define joystick 'press' pin
press_pin = 21
GPIO.setwarnings(False)

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
    pwm = GPIO.PWM(motor_enable, 1000)
    pwm.start(0)


class Motor:
    def __init__(self, p1, p2, pwm):
        self.p1 = p1
        self.p2 = p2
        self.pwm = pwm

    def set_relative_input(self, stick_y):
        # set relative y between 0 and 100 by using a factor (for pwm to use)
        relative_y = stick_y * (20/51)
        self.input = relative_y
        print(self.input, stick_y)

    def turn(self, stick_y):
        self.set_relative_input(stick_y)

        if self.input < 48:
            # turn motor fwd
            GPIO.output(self.p1, GPIO.HIGH)
            GPIO.output(self.p2, GPIO.LOW)
        elif self.input >= 48 and self.input <= 52:
            # motor off
            GPIO.output(self.p1, GPIO.LOW)
            GPIO.output(self.p2, GPIO.LOW)
        else:
            # motor backwards
            GPIO.output(self.p1, GPIO.LOW)
            GPIO.output(self.p2, GPIO.HIGH)

        # change motor strength through pwm
        if self.input <= 48:
            dc = (50 - self.input) * 2
        elif self.input >= 52:
            dc = (self.input-50) * 2
        else:
            dc = 0
        self.pwm.ChangeDutyCycle(dc)
        # print('Current pwm: {}'.format(dc))


class Joystick:
    def __init__(self, adc):
        self.set_pos_y(adc)

    def set_pos_y(self, adc):
        self._pos_y = adc.analogRead(0)

    def get_pos_y(self):
        return self._pos_y

def stop():
    GPIO.cleanup()
    adc.close()
    pwm.stop()


if __name__ == '__main__':
    print('starting motor')
    # call setup function to initiate variables
    setup()

    # make joystick and motor objects
    joystick = Joystick(adc)
    motor = Motor(motor_p1, motor_p2, pwm)

    try:
        while True:
            # get new joystick analog value
            joystick.set_pos_y(adc)
            # turn motor
            motor.turn(joystick.get_pos_y())

            time.sleep(0.01)

    except KeyboardInterrupt:
        stop()
      

    
 
    
    
