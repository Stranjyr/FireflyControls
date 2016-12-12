#!/usr/bin/env python
from ServoController import *
from BNO_Reader import *
k = 1
br = BNO_Reader(10)
sc = ServoController(4, 50, (-50.0/k, 50.0/k))
sc2 = ServoController(17, 50, (-180, 0))
br.start_bno_thread()
sc.start()
sc2.start()

try:
	while True:
		__, roll, pitch = br.getReadings()[0]
		sc.updateAngle(-roll)
		sc2.updateAngle(pitch)
		print(roll, pitch)
except KeyboardInterrupt:
	sc.close()
