
from gpiozero import Servo
from time import sleep

pin=17

maxPW=2/1000
minPW=1/1000

onVal = -1
offVal = 0.7


servo = Servo(pin,min_pulse_width=minPW,max_pulse_width=maxPW)





def openValve():
	servo.value =onVal
	print("Servo opened")


def closeValve():
	servo.value=offVal
	print("Servo closed")
