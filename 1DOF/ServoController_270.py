import RPi.GPIO as GPIO
import time
import threading

class ServoController:
	def __init__(self, pin, speed, r):
		self.pin = pin
		self.speed = speed
		self.min = r[0]
		self.max = r[1]
		self.angle = 0
		self.angleChanged = threading.Condition()

	def start(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pin, GPIO.OUT)
		self.pwm = GPIO.PWM(self.pin, self.speed)
		self.pwm.start(5)
		self.threadChangeAngle()

	def scale(self, value, oldmin, oldmax, newmin, newmax):
		oldr = (oldmax-oldmin)
		newr = (newmax-newmin)
		newv = (((value - oldmin)*newr)/oldr)+newmin
		return newv

	def updateAngle(self, ang):
		with self.angleChanged:
			if ang <= self.max and ang >= self.min:
				self.angle = ang
				self.angleChanged.notifyAll()
			else:
				print("Invalid Angle")
				if ang > self.max:
					self.angle = self.max
				else:
					self.angle = self.min

	def changeAngle(self):
		while True:
			with self.angleChanged:
				self.angleChanged.wait()
				self.pwm.ChangeDutyCycle(self.scale(self.angle, self.min, self.max, 5, 10))

	def threadChangeAngle(self):
	    servo_thread = threading.Thread(target=self.changeAngle)
	    servo_thread.daemon = True  # Don't let the BNO reading thread block exiting.
	    servo_thread.start()

	def close(self):
		print("Done")
		GPIO.cleanup()	

if __name__ == '__main__':
	serv = ServoController(18, 50, (-45, 45))
	serv.start()
	while True:
		newAngle = float(raw_input("Enter the new Angle:: "))
		if newAngle > 90:
			break
		serv.updateAngle(newAngle)
	serv.close()

	
