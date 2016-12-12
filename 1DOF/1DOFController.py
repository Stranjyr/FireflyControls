from __future__ import division
from PID import *
from BNO_Reader import *

import time

# Import the PCA9685 module.
import Adafruit_PCA9685



#Servo Control Functions
#------------------------------------------
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
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, int(pulse))

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)


#Helper Scaling Function
#takes a number to scale, the range of that number, and the range to scale to
def scale(num, org, new, act):
    i = (((num-org[0]) * (new[1] - new[0]))/(org[1]-org[0])) + new[0]
    if i > act[1]:
        return act[1]
    elif i < act[0]:
        return act[0]
    return i
#-------------------------------
#Functions for translating the rotation of servo to rotation of gimbal
def gimToServo(input):
	return input/2.0

#Filtering Functions
class Filter:
	def __init__(self, length):
		self.length = length
		self.saved = []
	def put(self, i):
		if(len(self.saved) >= self.length):
			self.saved = self.saved[1:self.length]
		self.saved.append(i)
	def get(self):
		return self.saved[self.length-1]
	def getAve(self):
		return sum(self.saved)/len(self.saved)


#-------------------------
#Main Control
if __name__ == '__main__':
	bno = BNO_Reader(10)
	bno.start_bno_thread()
        div = int(raw_input("Enter the pow of ten divisor:  "))
	p = int(raw_input("Enter P:  "))
	i = int(raw_input("Enter I:  "))
	d = int(raw_input("Enter D:  "))
	pid = PID(p, i, d) #the PID gains. Should be able to set the P gain such that we get occilation, then the D gain to remove the occilation.
	try:
		set_servo_pulse(1, 1.57)
		zero = bno.getReadings()[0][1]
		while True:
			roll = bno.getReadings()[0][1] - zero
			print(roll)
			pid.update(roll)
			print(pid.output)
			i = scale(-pid.output/div, [-180.0, 180.0], [1.07, 2.07], [1.45, 1.7])
			print(i)
			set_servo_pulse(0, i)
			#time.sleep(.1)
	except KeyboardInterrupt:
		set_servo_pulse(0, 1.57)
		print("Shutting Down")
