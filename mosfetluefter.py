import RPi.GPIO as GPIO
from time import sleep

ledpin = 11				# PWM pin connected to LED
GPIO.setwarnings(False)			#disable warnings
GPIO.setmode(GPIO.BOARD)		#set pin numbering system
GPIO.setup(ledpin,GPIO.OUT)

GPIO.output(ledpin, GPIO.HIGH)
sleep(1000)
GPIO.output(ledpin, GPIO.LOW)