import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 50)
pwm.start(5)

def scale(value, oldmin, oldmax, newmin, newmax):
	oldr = (oldmax-oldmin)
	newr = (newmax-newmin)
	newv = (((value - oldmin)*newr)/oldr)+newmin
	return newv

while True:
	newAngle = float(raw_input("Enter the new Angle:: "))
	if newAngle > 90:
		break
	duty = scale(newAngle, -45.0, 45.0, 5.0, 10.0)
	pwm.ChangeDutyCycle(duty)

print("Done")
GPIO.cleanup()		
