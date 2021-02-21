
from array import array
from base64 import encode
from modules.camera import takePhoto
import time
from modules.objects.climate import Climate, LiveData

from os import name

import json
import ctypes
from multiprocessing import shared_memory
import pyrebase


config = {
    "apiKey": "AIzaSyAeTF-VH5vxA0-ssHg4rMcjIodzBnnPvPw",
    "authDomain": "smartgrowsystem-sgs.firebaseapp.com",
    "databaseURL": "https://smartgrowsystem-sgs.firebaseio.com/",
    "storageBucket": "smartgrowsystem-sgs.appspot.com"

}


firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()
global activeClimate


def saveClimateToMemory(json_payload):
    if len(json_payload) == 0:
        return

    json_data = json.dumps(json_payload, indent=4,
                           default=str)
    climate = Climate(json_data)

    global buffer
    size = len(climate.get_buffer())
    # buffer[:] = b'0xff'
    buffer[:size] = climate.get_buffer()

    return climate


def authApp():
    # user = auth.sign_in_with_email_and_password(
    #    email="suf.raspberry.python@gmail.com", password="sufpython")

    user = auth.sign_in_with_email_and_password(
        email="suf.raspberry.python@gmail.com", password="sufpython")
    token = user["idToken"]

    print("Successfully authenticated App")
    return token


def climateListener(response):
    global activeClimate
    data = response["data"]
    path = response["path"]

    if(path == "/growPhase/phase"):
        activeClimate.growPhase.phase = data
        print(
            f"Grow Phase has changed to {data}. Climate:{activeClimate.name} Id:{activeClimate.id} @{12}")
    else:
        activeClimate = saveClimateToMemory(data)
        print(
            f"Active Climate has been loaded. Name:{activeClimate.name} Id:{activeClimate.id} @{12}")


# post to storage
def uploadImage(path, name):
    storage.child('/images/'+name).put(path+name, token=token)
    print("uploaded")


# write to database
def referenceImage(fileName, date):
    db.child("images").child(date).set(fileName, token=token)
    print("referenced")


def photoListener(response):
    global token
    data = response["data"]
    if(data == True):

        path, name, date = takePhoto()
        uploadImage(path, name)
        referenceImage(name, date)
        db.child("photo").set(data=False, token=token)
        print(
            f"{name} has been upladed and referenced")

    else:
        print("nothing")


def firebaseMain(t, args):

    global token
    token = t

    initialData = db.child("activeClimate").get(token=token).val()
    saveClimateToMemory(initialData)

    # Start Eventlisteneers
    clim_list = db.child("activeClimate").stream(
        climateListener, token=token,)

    photo_list = db.child("photo").stream(
        photoListener, token=token,)


def updateLiveData(temperature, humidity, soilMoisture, growProgress, waterTankLevel, lock, token):

    with lock:
        liveData = LiveData(temperature.value,
                            humidity.value, soilMoisture.value, growProgress.value, waterTankLevel.value)
        json = liveData.__dict__

        db.child("liveClimate").set(json, token=token)
        print("Updated Live Data")


if __name__ == "db" or "modules.database":
    global shm
    global buffer

    try:
        shm = shared_memory.SharedMemory(
            create=True, name="activeClimate", size=1000)
        buffer = shm.buf

        print("Created SharedMemory")
    except:
        shm = shared_memory.SharedMemory(name="activeClimate")
        buffer = shm.buf
        print("Reloaded SharedMemory")
