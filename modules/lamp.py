from datetime import date, datetime
import gpiozero
from gpiozero import OutputDevice

global on
on = False
light =OutputDevice(pin=15,active_high=True, initial_value=False)


# GPIO.Pin = 8


def sunTimeChanged(suntime, a):
    now = datetime.now()
    suns = suntime.split("-")
    startTime = suns[0].split(":")
    endTime = suns[1].split(":")
    start = datetime.now().replace(
        hour=int(startTime[0]), minute=int(startTime[1]))

    endhour = int(endTime[0])
    endmin = int(endTime[1])
    if(endhour == 24):
        endhour = 23
        endmin = 59

    end = datetime.now().replace(
        hour=endhour, minute=endmin)

    if(now.hour > start.hour and now.hour < end.hour):
        turnOn()
    elif(now.hour == start.hour and now.minute > start.minute):
        turnOn()
    elif(now.hour == end.hour and now.minute < end.minute):
        turnOn()
    else:
        turnOff()


def turnOn():
    print("Turned on Lamp")
    #light.on()


def turnOff():
    print("Turned off Lamp")
    #light.off()
