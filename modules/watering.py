import time


def irrigationStart(amount=None, percentage=None):
    if amount != None:
        waterAmount(amount)
    elif percentage != None:
        waterPercentage(percentage)


def waterAmount(amount):

    litersPerSecond = 0.1
    duration = amount / litersPerSecond
    # open Hose
    time.sleep(duration)
    # close Hose
    print(f"Irrigation was on for {duration}seconds. @12:00")


def waterPercentage(percentage):

    print()
