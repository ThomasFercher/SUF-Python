
from gpiozero import Servo
from time import sleep

pin=18

maxPW=2/1000
minPW=1/1000

onVal = -1
offVal = 0.7


servo = Servo(pin,min_pulse_width=minPW,max_pulse_width=maxPW)
#servo =PWMOutputDevice(pin=18,active_high=True, initial_value=0,frequency=50)



def testServo():
	
	
	closeValve()
	sleep(5)
	openValve()


def openValve():
	servo.value =onVal
	print("Servo opened")


def closeValve():
	servo.value=offVal
	print("Servo closed")
