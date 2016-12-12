import RPi.GPIO as gpio

class VNH5019:
	def __init__(self, A, B, PWM):
		self.apin = A
		self.bpin = B
		self.ppin = PWM
		#setup the gpio pins
		gpio.setwarnings(False)
		gpio.setmode (gpio.BCM)
		#outputs
		gpio.setup(self.apin, gpio.OUT)
		gpio.setup(self.bpin, gpio.OUT)
		gpio.setup(self.ppin, gpio.OUT)
		#Setup the pwm channel. pin, frequency(HZ)
		self.pwmSettings = gpio.PWM(self.ppin,20000)
		self.pwmSettings.start(0)
		#Inputs
		#gpio.setup(self.eapin, gpio.IN)
		#gpio.setup(self.ebpin, gpio.IN)


	'''
	If the direction is positive, spin counterclockwise
	if the direction is negitive, spin clockwise
	If zero, brake the motors
	'''
	def setDir(self, d):
		if d > 0:
			gpio.output(self.apin, True)
			gpio.output(self.bpin, False)
		elif d < 0:
			gpio.output(self.apin, False)
			gpio.output(self.bpin, True)
		elif d == 0:
			gpio.output(self.apin, False)
			gpio.output(self.bpin, False)

	'''
	Sets to motors to run at a given speed. 
	Accepts values between -100 and 100
	The absolute value of the input is the percentage
	of on time for the PWM cycle
	'''
	def runMotor(self, speed):
		self.setDir(speed) #spin the motors the proper way
		self.pwmSettings.ChangeDutyCycle(min(abs(speed), 100))
	def close(self):
		self.pwmSettings.stop()
		gpio.cleanup()
if __name__ == "__main__":
	v = VNH5019(17, 18, 13)	
	try:
		while True:
			s = float(input("Enter the motor speed (-100 to 100)"))
			v.runMotor(s)	
	except KeyboardInterrupt:
		v.close()
		print("Done")
