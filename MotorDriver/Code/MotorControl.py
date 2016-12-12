#!/usr/bin/env python
import VNH5019 as MDriver
#from scipy import signal
import numpy as np
import time
import RPi.GPIO as gpio
import threading
import BNO_Reader as bno
class MotorFunctionControl(object):
	def __init__(self, driver, function = None, frequency = 1, magnitude = 0):
		self.driver = driver
		if function == None:
			self.function = self.Triwave
		else:
			self.function = function
		self.frequency = frequency
		self.magnitude = magnitude
		self.runTime = 0
		self.lastTime = time.clock()
		self.stopThread = True

		#thread stuff
		self.function_thread = None
	def start(self):
		self.runTime = 0
		self.lastTime = time.clock()
		self.function_thread = threading.Thread(target=self.run_function_thread)
		self.function_thread.daemon = True
		self.function_thread.start()
	'''
	Sample Triangle Wave to use as the function input
	'''
	def Triwave(self, t, m, f):
		#return m*(abs(signal.sawtooth(2*np.pi*f*t))-.5)
		return m

	"""
	run a loop that continously updates the motor to 
	give it an acceleration
	"""
	def run_function_thread(self):
		while self.stopThread == True:
			self.runTime += -self.lastTime + time.clock()
			self.lastTime = time.clock()
			newSpeed = self.function(self.runTime, self.magnitude, self.frequency)
			self.driver.runMotor(newSpeed)
			time.sleep(.001)



#print('Start')
if __name__ == '__main__':
	br = bno.BNO_Reader(100)
	br.start_bno_thread()
	drive = MDriver.VNH5019(17, 18, 13)
	control = MotorFunctionControl(drive, function = lambda t, m, f : m)
	control.start()
	try:
		while True:
			r = br.getReadings()
			control.magnitude = r[0][1]
			print(r[0][1])

	except KeyboardInterrupt:
		control.magnitude = 0
		control.stopThread = False
		control.driver.close()
		print("Shutting Down")

