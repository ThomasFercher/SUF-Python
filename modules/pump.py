import time
import gpiozero
from gpiozero import OutputDevice


pump =OutputDevice(pin=27,active_high=True, initial_value=False)


def turnOn():

    pump.on()

def turnOff():

    pump.off()