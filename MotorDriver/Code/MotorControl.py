#!/usr/bin/env python
import VNH5019 as MDriver
#from scipy import signal
import numpy as np
import time
import RPi.GPIO as gpio
import threading
import BNO_Reader as bno
import gaugette.gpio
import gaugette.rotary_encoder
import math
class PID:
	def __init__(self,P=2.0, I=0.0, D=1.0, derivator=0, integrator=0, integratorMax=500, integratorMin=-500):
		self.Kp = P
		self.Ki = I
		self.Kd = D
		self.derivator = derivator
		self.integrator = integrator
		self.integratorMax = integratorMax
		self.integratorMin = integratorMin
		self.setPoint = 0.0
		self.error = 0.0
		self.output = 0.0

	def update(self,currentValue):
		self.error = self.setPoint - currentValue
		pVal = self.Kp * self.error
		dVal = self.Kd * (self.error - self.derivator)
		self.derivator = self.error
		self.integrator = self.integrator * self.error
		if self.integrator > self.integratorMax:
			self.integrator = self.integratorMax
		if self.integrator < self.integratorMin:
			self.integrator = self.integratorMin

		iVal = self.integrator * self.Ki
		self.output = pVal + iVal + dVal
		
class MotorFunctionControl(object):
	def __init__(self, driver, function = None, frequency = 4, magnitude = 0):
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
		self.totalTurn = 0
		self.function_thread.start()


	'''
	Sample Triangle Wave to use as the function input
	'''
	def Triwave(self, t, m, f):
		return m*(math.sin(2*np.pi*f*t))

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

def dirChange(inV, spd):
	if inV == 0:
		return inV
	return abs(inV)/inV * spd

#print('Start')
if __name__ == '__main__':
	br = bno.BNO_Reader(10000)
	br.start_bno_thread()
	drive = MDriver.VNH5019(17, 18, 13)
	#freq = int(raw_input("Enter a frequency for the motor:  "))
	control = MotorFunctionControl(drive, function = lambda t, m, f : np.sign(m)*math.sqrt(abs(m)))
	control.start()
	p = float(raw_input("Enter P:  "))
	i = float(raw_input("Enter I:  "))
	d = float(raw_input("Enter D:  "))
	div = 1 #float(raw_input("Enter Divider (1) for no change:  "))
	maxAngle = 80 #int(raw_input("Enter The IMU fail angle:   "))
	minAngle = 0  #int(raw_input("Enter a stable:   "))
	pid = PID(p, i, d) #the PID gains. Should be able to set the P gain such that we get occilation, then the D gain to remove the occilation.
	totalTime = 0
	count = 0
	timer = time.time()
	try:
		IMUtime = time.time()
		zero = 0#br.getReadings()[0][1]
		IMUtime = time.time() - IMUtime
		print("{} IMU read time".format(IMUtime))
		while True:
			#IMUtime = time.time()
			roll = br.getReadings()[0][1] - zero
			#IMUtime = time.time() - IMUtime
			#print("{} IMU read time".format(IMUtime))
			print("{} : roll".format(roll))
			if abs(roll) > maxAngle:
				control.magnitude = 0
				print("Max angle exceeded")
			#elif abs(roll) < minAngle:
			#	control.magnitude = 0
			#	print("In a stable position")
			else:
				pid.update(roll)
				print("{} : pid".format(pid.output/div))
				control.magnitude = pid.output/div
				#control.magnitude = dirChange(pid.output/div,50) 
			#prevTime = timer
			#timer = time.time()
			#print("\n{} delta time\n".format(timer - prevTime))
			#time.sleep(.1)
	except KeyboardInterrupt:
		control.magnitude = 0
		control.stopThread = False
		control.driver.close()
		print("Shutting Down")

