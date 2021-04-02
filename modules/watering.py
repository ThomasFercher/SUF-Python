import time
import gpiozero
from gpiozero import OutputDevice


pump =OutputDevice(pin=17,active_high=True, initial_value=False)
valve =OutputDevice(pin=27,active_high=True, initial_value=False)



def irrigationStart(amount=None, percentage=None):
    if amount != None:
        waterAmount(amount)
    elif percentage != None:
        waterPercentage(percentage)


def waterAmount(amount):

    litersPerSecond = 1
    duration = amount / litersPerSecond
    # open Hose
    pump.on()
    time.sleep(duration)
    pump.off()
    # close Hose
    print(f"Irrigation was on for {duration}seconds. @12:00")


def waterPercentage(percentage):
    
    print()
