import serial
s = serial.Serial('/dev/ttyAMA0', 9600)
try:
	while True:
		line = s.read(5)
		print line
except KeyboardInterrupt:
	s.close()
