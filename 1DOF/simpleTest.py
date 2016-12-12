# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time
import RPi.GPIO as GPIO
# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    #print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    #print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse = int(pulse)
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

print('Moving servo on channel 0, press Ctrl-C to quit...')
#i = float(raw_input("Enter a numberr between 1 and 2:  "  ))
i = 1.5
set_servo_pulse(0, 1.1)

#LED Testig Light
#GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT)
while True:
    # Move servo on channel O between extremes.
    set_servo_pulse(0, i)
    #time.sleep(.01)
    #raw_input("Reset?")
    #GPIO.output(4, GPIO.LOW)
    i = float(raw_input("Enter a number between 1 and 2:  "  ))
    #GPIO.output(4, GPIO.HIGH) 
    '''i = i+.01
    if i > 2:
        i = 1'''
