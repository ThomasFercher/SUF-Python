import time
import gpiozero
from gpiozero import OutputDevice
import modules.pump as pump

valve =OutputDevice(pin=22,active_high=True, initial_value=False)



def irrigationStart(amount=None, percentage=None):
    if amount != None:
        waterAmount(amount)
    elif percentage != None:
        waterPercentage(percentage)


def waterAmount(amount):

    litersPerSecond = 1
    duration = amount / litersPerSecond

    valve.on()
    pump.turnOn()

    time.sleep(duration)

    pump.turnOff()
    valve.off()
    print(f"Irrigation was on for {duration}seconds. @12:00")


def waterPercentage(percentage):
    
    print()
