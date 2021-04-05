from datetime import datetime
import time
from typing import TYPE_CHECKING
from picamera import PiCamera
#import modules.database as db

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.rotation = 180


fileName = "photo"
path = "../Pictures/"


def takePhoto():
    ts = datetime.now()
    date = ts.strftime("%Y-%m-%d %H:%M:%S")
    name = fileName+"_"+date+".jpg"
  

    # take Image and save it
    time.sleep(0.5)
    camera.capture(path+name)
    time.sleep(0.5)

    #name = "2021-02-20 15.05.32.jpg"
    

    return path, name, date
